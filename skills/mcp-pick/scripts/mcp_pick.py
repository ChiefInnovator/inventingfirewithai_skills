#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["tomlkit==0.13.3"]
# ///
"""Select project-local Codex MCP servers and installed app integrations without exposing secrets."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tomllib


class PickerError(Exception):
    pass


class Codex:
    """Short-lived metadata/config client; never creates a model thread or runs MCP tools."""

    def __init__(self, project: Path, profile: str | None = None):
        self.project = project
        command = ["codex"]
        if profile:
            command += ["--profile", profile]
        self.command = command.copy()
        command += ["app-server", "--stdio"]
        self.process = subprocess.Popen(
            command, cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
        )
        self.messages: queue.Queue = queue.Queue()
        self.sequence = 0
        threading.Thread(target=self._read, daemon=True).start()
        try:
            self.call("initialize", {
                "clientInfo": {"name": "mcp-pick", "version": "1.0"},
                "capabilities": {"experimentalApi": True},
            })
            self.send({"method": "initialized"})
        except Exception:
            self.close()
            raise

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                continue
        self.messages.put(None)

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def call(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self.send({"id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + 45
        while True:
            try:
                message = self.messages.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty:
                raise PickerError(f"Codex timed out during {method}; no success is assumed.") from None
            if message is None:
                raise PickerError(f"Codex exited during {method}.")
            if message.get("id") != request_id:
                continue
            if "error" in message:
                # Error payloads can contain configuration values. Never print them.
                code = message["error"].get("code", "unknown")
                label = " for " + repr(params["pluginName"]) if method == "plugin/read" else ""
                raise PickerError(f"Codex rejected {method}{label} (code {code}); check CLI compatibility/configuration.")
            return message["result"]

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        for stream in (self.process.stdin, self.process.stdout):
            stream.close()

    def installed_plugins(self):
        result = subprocess.run(self.command + ["plugin", "list", "--json"], cwd=self.project,
                                capture_output=True, text=True, timeout=45)
        if result.returncode:
            raise PickerError("Installed plugin discovery failed; no selection is applied.")
        return json.loads(result.stdout)["installed"]


def project_path(value: str | None) -> Path:
    if value:
        project = Path(value).expanduser().resolve()
    else:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
        ) if shutil.which("git") else None
        project = Path(result.stdout.strip()).resolve() if result and result.returncode == 0 else Path.cwd().resolve()
    if not project.is_dir():
        raise PickerError("The project directory does not exist.")
    return project


def setting(config, parts, default=None):
    value = config
    for part in parts:
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def local_layer(response, target):
    for layer in response.get("layers") or []:
        source = layer["name"]
        if source.get("type") == "project" and Path(source["dotCodexFolder"]) / "config.toml" == target:
            return layer
    return None


def discover(client, project, scope):
    response = client.call("config/read", {"cwd": str(project), "includeLayers": True})
    config = response["config"]
    entries = {}
    installed_apps = {}

    def add(selector, name, parts, enabled, blocked=None):
        entries[selector] = {
            "id": selector, "name": name, "path": parts,
            "enabled": bool(enabled), "blocked": blocked,
        }

    def register_plugin(plugin_id, enabled, details):
        for name in details["mcpServers"]:
            parts = ["plugins", plugin_id, "mcp_servers", name, "enabled"]
            parent_enabled = setting(config, ["plugins", plugin_id, "enabled"], enabled)
            blocked = "shadowed by explicit MCP definition" if name in (config.get("mcp_servers") or {}) else (
                None if parent_enabled else "parent plugin disabled")
            add("plugin:" + plugin_id + "/" + name, name + " (" + plugin_id + ")", parts,
                not blocked and setting(config, parts, True), blocked)
        for app in details["apps"]:
            installed_apps[app["id"]] = app["name"]

    for name, server in (config.get("mcp_servers") or {}).items():
        add("mcp:" + name, name, ["mcp_servers", name, "enabled"], server.get("enabled", True))

    plugins = client.call("plugin/list", {
        "cwds": [str(project)], "forceRefetch": False, "marketplaceKinds": ["local"],
    })
    if plugins.get("marketplaceLoadErrors"):
        raise PickerError("Plugin inventory is incomplete; fix marketplace discovery before selecting servers.")
    seen_plugins = set()
    for marketplace in plugins["marketplaces"]:
        for plugin in marketplace["plugins"]:
            if not plugin["installed"]:
                continue
            plugin_id = plugin["id"]
            seen_plugins.add(plugin_id)
            details = client.call("plugin/read", {
                "pluginName": plugin["name"], "marketplacePath": marketplace.get("path"),
                "remoteMarketplaceName": None if marketplace.get("path") else marketplace["name"],
            })["plugin"]
            register_plugin(plugin_id, plugin["enabled"], details)
    # The installed-only CLI inventory includes remote plugins. app/list is a
    # public catalog (potentially huge), not a connected-account inventory.
    for plugin in client.installed_plugins():
        plugin_id = plugin["pluginId"]
        if plugin_id in seen_plugins:
            continue
        details = client.call("plugin/read", {
            "pluginName": plugin.get("source", {}).get("id", plugin["name"]),
            "remoteMarketplaceName": plugin["marketplaceName"],
        })["plugin"]
        seen_plugins.add(plugin_id)
        register_plugin(plugin_id, plugin["enabled"], details)
    for plugin_id, plugin in (config.get("plugins") or {}).items():
        if plugin.get("mcp_servers") and plugin_id not in seen_plugins:
            raise PickerError("A configured plugin's MCP servers could not be discovered; no selection is applied.")

    if scope == "all":
        for app_id, name in installed_apps.items():
            parts = ["apps", app_id, "enabled"]
            add("app:" + app_id, name, parts, setting(config, parts, True))
        for app_id, app in (config.get("apps") or {}).items():
            if app_id == "_default" or app_id in installed_apps:
                continue
            add("app:" + app_id, app_id, ["apps", app_id, "enabled"], app.get("enabled", True),
                "configured app not provided by an installed plugin")

    ordered = sorted(entries.values(), key=lambda entry: entry["id"])
    # Bind a menu to this exact project, scope, inventory, and effective config layers.
    fingerprint = {"project": str(project), "scope": scope, "entries": ordered,
                   "layers": [{k: v for k, v in layer.items() if k != "config"}
                              for layer in response.get("layers") or []]}
    version = hashlib.sha256(json.dumps(fingerprint, sort_keys=True).encode()).hexdigest()
    layer = local_layer(response, project / ".codex" / "config.toml")
    return {"project": str(project), "scope": scope, "inventory_version": version,
            "entries": ordered, "project_config_ignored": bool(layer and layer.get("disabledReason"))}, response


def selected_entries(inventory, mode, selected):
    by_id = {entry["id"]: entry for entry in inventory["entries"]}
    if mode == "keep":
        unknown = set(selected) - by_id.keys()
        if unknown:
            raise PickerError("Unknown selection IDs; refresh the menu before applying.")
        keep = set(selected)
    elif mode == "all":
        keep = {key for key, entry in by_id.items() if not entry["blocked"]}
    else:
        keep = set()
    if any(by_id[key]["blocked"] for key in keep):
        raise PickerError("A selected entry is blocked by its parent plugin or app access; the picker does not change those controls.")
    return keep


def safe_target(project):
    target = project / ".codex" / "config.toml"
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser().resolve()
    if target.parent.is_symlink() or target.is_symlink():
        raise PickerError("Refusing a symlinked project .codex directory or config file.")
    if target.resolve() == codex_home / "config.toml" or project == Path.home():
        raise PickerError("Refusing to use global Codex configuration as a project target.")
    return target, codex_home


def atomic_write(target, contents, mode):
    descriptor, temporary = tempfile.mkstemp(prefix=".mcp-pick-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def apply_selection(client, project, inventory, response, keep):
    # The installed Codex config/write API only permits user-global writes.
    # Use a formatting-preserving TOML editor for the project layer instead.
    try:
        import tomlkit
    except ImportError:
        raise PickerError("Run this helper with uv run --script to load its pinned TOML dependency.") from None
    target, codex_home = safe_target(project)
    if inventory["project_config_ignored"]:
        raise PickerError("Codex ignores this untrusted project's config. Trust the project in Codex before applying.")
    if not inventory["entries"]:
        return {"changed": False, "backup": None, "config_path": str(target)}
    original = target.read_bytes() if target.exists() else None
    # Check syntax before creating backups or requesting any changes.
    existing = tomllib.loads(original.decode()) if original is not None else {}
    if all(setting(existing, entry["path"]) == (entry["id"] in keep) for entry in inventory["entries"]):
        return {"changed": False, "backup": None, "config_path": str(target)}

    document = tomlkit.parse(original.decode() if original is not None else "")
    for entry in inventory["entries"]:
        table = document
        for part in entry["path"][:-1]:
            if part not in table:
                table[part] = tomlkit.table()
            table = table[part]
        table[entry["path"][-1]] = entry["id"] in keep
    proposed = tomlkit.dumps(document).encode()
    tomllib.loads(proposed.decode())

    created = False
    backup = None
    written = False
    mode = target.stat().st_mode & 0o777 if original is not None else 0o600
    backup_dir = codex_home / "backups" / "mcp-pick" / hashlib.sha256(str(project).encode()).hexdigest()[:16]
    backup_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock = open(backup_dir / "write.lock", "a")
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        safe_target(project)
        if (target.read_bytes() if target.exists() else None) != original:
            raise PickerError("Project configuration changed while preparing the update; refresh the menu.")
        if original is None:
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with target.open("xb"):
                pass
            target.chmod(0o600)
            created = True
        current = client.call("config/read", {"cwd": str(project), "includeLayers": True})
        layer = local_layer(current, target)
        if layer is None or layer.get("disabledReason"):
            raise PickerError("Codex is not loading this project's config. Trust the project in Codex; no trust setting was changed.")
        previous_layer = local_layer(response, target)
        if original is not None and (previous_layer is None or previous_layer["version"] != layer["version"]):
            raise PickerError("Project configuration changed after discovery; refresh the menu.")
        def other_layers(snapshot):
            target_layer = local_layer(snapshot, target)
            return [{k: v for k, v in item.items() if k != "config"}
                    for item in snapshot.get("layers") or [] if item is not target_layer]
        if other_layers(current) != other_layers(response):
            raise PickerError("Inherited configuration changed after discovery; refresh the menu.")
        if target.read_bytes() != (original if original is not None else b""):
            raise PickerError("Project configuration changed while preparing the update; refresh the menu.")
        if original is not None:
            backup = backup_dir / (str(time.time_ns()) + ".toml")
            with os.fdopen(os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
                stream.write(original)
        safe_target(project)
        if target.read_bytes() != (original if original is not None else b""):
            raise PickerError("Project configuration changed before writing; refresh the menu.")
        atomic_write(target, proposed, mode)
        written = True
        read_back = tomllib.loads(target.read_text())
        for entry in inventory["entries"]:
            if setting(read_back, entry["path"]) != (entry["id"] in keep):
                raise PickerError("A project setting failed read-back verification; inspect the backup and config.")
        refreshed = client.call("config/read", {"cwd": str(project), "includeLayers": True})
        if not local_layer(refreshed, target) or local_layer(refreshed, target).get("disabledReason"):
            raise PickerError("The written project layer is not active in Codex; no effective change is claimed.")
        for entry in inventory["entries"]:
            if setting(refreshed["config"], entry["path"]) != (entry["id"] in keep):
                raise PickerError("A higher-priority configuration overrides the selection; no effective success is claimed.")
        return {"changed": True, "backup": str(backup) if backup else None, "config_path": str(target)}
    except Exception:
        if written and target.exists() and not target.is_symlink() and target.read_bytes() == proposed:
            if original is None:
                target.unlink()
            else:
                atomic_write(target, original, mode)
        # Remove only our untouched empty placeholder, never a concurrent/user edit.
        if created and target.exists() and target.read_bytes() == b"":
            target.unlink()
        raise
    finally:
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        lock.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["list", "keep", "all", "none"])
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--project", help="Project directory; defaults to Git root, or cwd outside Git")
    parser.add_argument("--profile", help="Match an explicitly selected Codex profile")
    parser.add_argument("--scope", choices=["all", "servers"], default="all",
                        help="all includes installed app integrations; servers limits the operation to MCP servers")
    parser.add_argument("--expect", help="Inventory version returned by the reviewed list")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_intermixed_args()
    if args.mode != "keep" and args.ids:
        parser.error("Selection IDs are valid only with keep.")
    if args.mode != "list" and not args.dry_run and not args.expect:
        parser.error("Writes require --expect from the reviewed list.")
    client = None
    try:
        project = project_path(args.project)
        safe_target(project)
        client = Codex(project, args.profile)
        inventory, response = discover(client, project, args.scope)
        if args.expect and args.expect != inventory["inventory_version"]:
            raise PickerError("Inventory or configuration changed since review. Refresh the list before applying.")
        if args.mode == "list":
            if args.json:
                print(json.dumps(inventory, indent=2))
            else:
                print("MCP choices for " + str(project) + " (scope: " + args.scope + ")")
                for number, entry in enumerate(inventory["entries"], 1):
                    note = " [" + entry["blocked"] + "]" if entry["blocked"] else ""
                    print(f"{number}. [{'x' if entry['enabled'] else ' '}] {entry['name']} — {entry['id']}{note}")
                print("Inventory: " + inventory["inventory_version"])
                if inventory["project_config_ignored"]:
                    print("Project config is ignored by Codex until the project is trusted.")
            return 0
        keep = selected_entries(inventory, args.mode, args.ids)
        result = {"enabled": sorted(keep), "disabled": sorted(entry["id"] for entry in inventory["entries"] if entry["id"] not in keep),
                  "dry_run": args.dry_run, "scope": args.scope}
        if not args.dry_run:
            result.update(apply_selection(client, project, inventory, response, keep))
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("enabled : " + (", ".join(result["enabled"]) or "(none)"))
            print("disabled: " + (", ".join(result["disabled"]) or "(none)"))
            if args.dry_run:
                print("Preview only; no project settings written.")
            else:
                print("Config: " + result["config_path"])
                if result["backup"]:
                    print("Backup: " + result["backup"])
                print("Start a new Codex session in this trusted project to load the selection. Existing tool/approval policies still apply.")
        return 0
    except (PickerError, OSError, ValueError, subprocess.SubprocessError) as error:
        # Only controlled PickerError messages are safe to display verbatim.
        print(str(error) if isinstance(error, PickerError) else
              f"Picker failed ({type(error).__name__}); no successful selection is claimed.", file=sys.stderr)
        return 1
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    sys.exit(main())
