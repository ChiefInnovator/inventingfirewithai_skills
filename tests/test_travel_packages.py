"""Validate shipped travel artifacts, not whether instructions repeat a phrase.

These checks reject known machine paths and unexpected state files; they cannot
identify every kind of personal information in otherwise valid Markdown.
Run with the dependencies declared in tests/requirements.txt.
"""

from collections import Counter
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

import yaml


ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ("codex", "claude", "copilot")
FAMILY = "travel-like-a-local"
ARCHIVE = ROOT / "assets" / "distributions" / (FAMILY + ".zip")
MACHINE_PATH = re.compile(
    r"file://|/(?:Users|home)/[^\s/]+|[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]|~/",
    re.IGNORECASE,
)
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+['\"][^\n]*?['\"])?\s*\)")
REFERENCE_LINK = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))", re.MULTILINE)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def package(root, client):
    return root / "skills" / client / FAMILY


def package_files(folder):
    """Allow reusable instructions, UI metadata, and image assets, never state."""
    result = {}
    require(not folder.is_symlink(), f"Bundled symlink: {folder.name}")
    require(folder.is_dir(), f"Missing package: {folder}")
    for path in sorted(folder.rglob("*")):
        name = path.relative_to(folder).as_posix()
        require(not path.is_symlink(), f"Bundled symlink: {name}")
        if not path.is_file():
            continue
        allowed = (name == "SKILL.md" or name == "agents/openai.yaml"
                   or (name.startswith("references/") and path.suffix == ".md")
                   or (name.startswith("assets/") and path.suffix.lower()
                       in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}))
        require(allowed, f"Unexpected package/state file: {name}")
        content = path.read_bytes()
        if path.suffix in {".md", ".yaml", ".svg"}:
            require(not MACHINE_PATH.search(content.decode("utf-8")),
                    f"Machine-specific path in {name}")
        result[name] = content
    require("SKILL.md" in result, f"Missing SKILL.md: {folder}")
    return result


def frontmatter(content, label):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
    require(match is not None, f"Missing or incomplete frontmatter: {label}")
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML: {label}") from error
    require(isinstance(metadata, dict), f"Frontmatter must be a mapping: {label}")
    require(metadata.get("name") == FAMILY, f"Invalid skill name: {label}")
    description = metadata.get("description")
    require(isinstance(description, str) and bool(description.strip()),
            f"Missing nonempty description: {label}")
    return metadata


def heading_anchors(content):
    counts = Counter()
    anchors = set()
    for heading in re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", content, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        suffix = counts[slug]
        anchors.add(slug + (f"-{suffix}" if suffix else ""))
        counts[slug] += 1
    return anchors


def local_target(folder, document, link):
    require(not MACHINE_PATH.search(link), f"Machine-specific link in {document.name}: {link}")
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        require(parsed.scheme in {"https", "http", "mailto"},
                f"Unsupported link in {document.name}: {link}")
        return None
    path = unquote(parsed.path)
    require(not path.startswith(("/", "\\")), f"Absolute link in {document.name}: {link}")
    target = (document.parent / path).resolve() if path else document.resolve()
    require(target.is_relative_to(folder.resolve()), f"Link escapes package: {link}")
    require(target.is_file(), f"Broken local link in {document.name}: {link}")
    if parsed.fragment:
        require(target.suffix == ".md" and unquote(parsed.fragment) in heading_anchors(target.read_text()),
                f"Broken heading anchor in {document.name}: {link}")
    return target


def check_links(folder):
    for document in folder.rglob("*.md"):
        content = document.read_text(encoding="utf-8")
        for pattern in (INLINE_LINK, REFERENCE_LINK):
            for match in pattern.finditer(content):
                local_target(folder, document, match.group(1) or match.group(2))


def check_metadata(folder, client):
    frontmatter((folder / "SKILL.md").read_text(encoding="utf-8"), client)
    if client != "codex":
        return
    try:
        ui = yaml.safe_load((folder / "agents" / "openai.yaml").read_text())
    except yaml.YAMLError as error:
        raise ValueError("Invalid Codex UI YAML") from error
    require(isinstance(ui, dict) and isinstance(ui.get("interface"), dict), "Missing Codex interface metadata")
    interface = ui["interface"]
    for key in ("display_name", "short_description", "default_prompt"):
        require(isinstance(interface.get(key), str) and bool(interface[key].strip()),
                f"Missing Codex interface {key}")
    for key in ("icon_small", "icon_large"):
        if key not in interface:
            continue
        require(isinstance(interface[key], str), f"Invalid Codex interface {key}")
        target = local_target(folder, folder / "SKILL.md", interface[key])
        require(target is not None and target.is_relative_to((folder / "assets").resolve())
                and target.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"},
                f"Codex {key} must reference a bundled image under assets/")
    if "policy" in ui:
        require(isinstance(ui["policy"], dict), "Invalid Codex invocation policy")
        if "allow_implicit_invocation" in ui["policy"]:
            require(type(ui["policy"]["allow_implicit_invocation"]) is bool, "Invalid Codex invocation flag")


def check_parity(root):
    reference_sets = {}
    for client in CLIENTS:
        files = package_files(package(root, client))
        reference_sets[client] = {name: data for name, data in files.items() if name.startswith("references/")}
        require(bool(reference_sets[client]), f"No shared references: {client}")
    expected = reference_sets["codex"]
    for client in CLIENTS[1:]:
        actual = reference_sets[client]
        differences = sorted(name for name in expected.keys() | actual.keys() if expected.get(name) != actual.get(name))
        require(not differences, f"Shared reference mismatch for {client}: {differences}")


def check_archive(folder, archive_path):
    expected = {FAMILY + "/" + name: data for name, data in package_files(folder).items()}
    with ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP member")
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in info.filename,
                    f"Unsafe ZIP member: {info.filename}")
            require(stat.S_IFMT(info.external_attr >> 16) != stat.S_IFLNK,
                    f"Symlink ZIP member: {info.filename}")
        files = {info.filename for info in archive.infolist() if not info.is_dir()}
        require(files == set(expected), f"ZIP file set differs: {sorted(files ^ set(expected))}")
        for name, content in expected.items():
            require(archive.read(name) == content, f"Stale ZIP content: {name}")


class TravelPackageTests(unittest.TestCase):
    def test_shared_references_match_without_erasing_host_entrypoints(self):
        check_parity(ROOT)

    def test_archive_matches_complete_codex_package(self):
        check_archive(package(ROOT, "codex"), ARCHIVE)

    def test_all_clients_have_valid_metadata_and_bundled_ui_assets(self):
        for client in CLIENTS:
            with self.subTest(client=client):
                folder = package(ROOT, client)
                package_files(folder)
                check_metadata(folder, client)

    def test_all_local_links_and_anchors_resolve_within_the_package(self):
        for client in CLIENTS:
            with self.subTest(client=client):
                check_links(package(ROOT, client))

    def test_all_clients_exclude_known_machine_paths_and_state_files(self):
        for client in CLIENTS:
            with self.subTest(client=client):
                package_files(package(ROOT, client))

    def copy_package(self, destination, client="codex"):
        folder = destination / "skills" / client / FAMILY
        shutil.copytree(package(ROOT, client), folder)
        return folder

    def test_checks_reject_missing_or_changed_shared_references(self):
        for mutation in ("missing", "changed"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for client in CLIENTS:
                    self.copy_package(root, client)
                reference = next((package(root, "claude") / "references").glob("*.md"))
                if mutation == "missing":
                    reference.unlink()
                else:
                    reference.write_text(reference.read_text() + "\nChanged fixture.\n")
                with self.assertRaisesRegex(ValueError, "reference mismatch"):
                    check_parity(root)

    def test_checks_reject_invalid_metadata_and_missing_ui_assets(self):
        def point_icon_at_document(folder):
            path = folder / "agents" / "openai.yaml"
            metadata = yaml.safe_load(path.read_text())
            metadata["interface"]["icon_small"] = "./SKILL.md"
            path.write_text(yaml.safe_dump(metadata))

        mutations = {
            "invalid YAML": lambda folder: (folder / "SKILL.md").write_text("---\nname: [broken\n---\n"),
            "wrong name": lambda folder: (folder / "SKILL.md").write_text("---\nname: wrong\ndescription: valid\n---\n"),
            "missing description": lambda folder: (folder / "SKILL.md").write_text("---\nname: travel-like-a-local\n---\n"),
            "missing icon": lambda folder: (folder / "assets" / "icon.svg").unlink(),
            "non-image icon": point_icon_at_document,
        }
        for label, mutate in mutations.items():
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                folder = self.copy_package(Path(directory))
                mutate(folder)
                with self.assertRaises(ValueError):
                    check_metadata(folder, "codex")

    def test_optional_icon_metadata_can_be_omitted(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.copy_package(Path(directory))
            path = folder / "agents" / "openai.yaml"
            metadata = yaml.safe_load(path.read_text())
            for key in ("icon_small", "icon_large"):
                metadata["interface"].pop(key, None)
            path.write_text(yaml.safe_dump(metadata))
            check_metadata(folder, "codex")

    def test_checks_reject_broken_links_anchors_and_package_escapes(self):
        links = ("missing.md", "references/traveler-profile.md#missing-heading", "../outside.md", "file:///private/menu.md")
        for link in links:
            with self.subTest(link=link), tempfile.TemporaryDirectory() as directory:
                folder = self.copy_package(Path(directory))
                (folder.parent / "outside.md").write_text("outside")
                with (folder / "SKILL.md").open("a") as stream:
                    stream.write(f"\n[fixture]({link})\n")
                with self.assertRaises(ValueError):
                    check_links(folder)

    def test_checks_accept_valid_heading_links_and_offline_external_links(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.copy_package(Path(directory))
            with (folder / "SKILL.md").open("a") as stream:
                stream.write("\n[profile](references/traveler-profile.md#private-persistence)\n")
                stream.write("[external](https://example.invalid/never-fetched)\n")
            check_links(folder)

    def test_checks_reject_bundled_private_state_machine_paths_and_symlinks(self):
        for mutation in ("profile", "trip", "machine path", "symlink"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                folder = self.copy_package(Path(directory))
                if mutation in ("profile", "trip"):
                    (folder / (mutation + ".json")).write_text("{}")
                elif mutation == "machine path":
                    with (folder / "SKILL.md").open("a") as stream:
                        stream.write("\n/Users/fixture/private-profile.json\n")
                else:
                    (folder / "assets" / "outside.svg").symlink_to(Path(directory) / "outside.svg")
                with self.assertRaises(ValueError):
                    package_files(folder)

    def test_checks_reject_stale_extra_duplicate_and_unsafe_zip_members(self):
        for mutation in ("stale", "extra", "duplicate", "escape"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                folder = self.copy_package(root)
                archive_path = root / "travel.zip"
                contents = {FAMILY + "/" + name: data for name, data in package_files(folder).items()}
                with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
                    for name, content in contents.items():
                        archive.writestr(name, b"stale" if mutation == "stale" and name.endswith("SKILL.md") else content)
                    if mutation == "extra":
                        archive.writestr(FAMILY + "/profile.json", "{}")
                    elif mutation == "duplicate":
                        with self.assertWarns(UserWarning):
                            archive.writestr(FAMILY + "/SKILL.md", contents[FAMILY + "/SKILL.md"])
                    elif mutation == "escape":
                        archive.writestr("../outside.md", "escape")
                with self.assertRaises(ValueError):
                    check_archive(folder, archive_path)


if __name__ == "__main__":
    unittest.main()
