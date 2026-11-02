---
title: Travel Like a Local tests
description: Automated package checks and offline behavioral smoke evidence for Travel Like a Local, including privacy, pickup confirmations, menu translation, and venue closures.
---

# Travel Like a Local Tests

## Automated package checks

Run from the repository root:

```sh
uv run --no-project --python 3.14 --with-requirements tests/requirements.txt python -m unittest discover -s tests
```

[Travel package tests](https://github.com/ChiefInnovator/inventingfirewithai_skills/blob/main/tests/test_travel_packages.py) check shared reference parity across Codex, Claude, and Copilot; actual YAML metadata and referenced Codex images; local links and heading anchors; and the complete Codex ZIP's file set and bytes. Host entrypoints and optional UI fields may differ.

Disposable corrupted packages verify that the checks catch missing or changed references, invalid YAML, missing images, non-image icon targets, broken links and anchors, package escapes, machine-specific paths, unexpected state files, symlinks, and stale, extra, duplicate, or unsafe ZIP members. External links are not fetched. These checks reject known artifact hazards; they cannot identify all personal information embedded in otherwise valid prose or images.

On October 31, 2026, all 12 Travel tests passed, and the complete root test suite passed 110 tests with the command above. Figma and client-specific MCP helper suites are separate from that root-suite count.

## Behavioral smoke protocol

Use a fresh agent context for each [fictional fixture](https://github.com/ChiefInnovator/inventingfirewithai_skills/tree/main/tests/fixtures/travel/), with an unchanged copy of the skill and only that case's prompt and evidence. Keep the acceptance criteria below with the assessor, not the executing agent. Do not provide the expected answer or earlier results. Disable live browsing, account access, real memory, communications, and bookings. The fixtures supply captured evidence; they do not establish live venue or travel facts.

Record the actual response and assess its meaning and actions, rather than checking whether it repeats instruction wording. For the preference case, seed a disposable private profile from `profile_seed`, capture its bytes, and execute only `prompt`. After verifying that the profile is unchanged, provide this separate user turn:

> Please now remember these fictional preferences in the authorized test profile at private-store/preferences.json: I prefer quiet cafes and walking between nearby stops. Preserve the profile's other fields.

Verify the resulting file, preservation of existing preferences, unchanged input fixtures and skill files, and absence of writes outside the authorized case folder. Harness response artifacts are separate from user-profile persistence. Never use the real user's preferences or a production memory store.

| Case | Observable acceptance criteria |
|---|---|
| Menu translation | Translate all three dishes correctly, explain unfamiliar terms briefly, and answer without destination/date onboarding. |
| Confirmed pickup | Use Traveler A's latest supplier amendment: November 5 at 08:15 local, Lark Hotel lobby, Terminal 2, EUR 65. Distinguish the 07:45 planning suggestion, superseded 09:00 booking, and Traveler B's transfer. |
| Closed venue | Respect the user's closure report and ten-minute walking limit. Select the five-minute bakery from supplied evidence, state the source limitation, and avoid inventing confirmed seating, a second qualifying option, or live verification. |
| Private preferences | Without consent, acknowledge conversation-only preferences and leave the profile unchanged. After explicit consent, save only to the disposable private store and preserve its existing map preference. |

## October 31, 2026 Run

Four fresh Codex subagents executed the four cases; the preference case had two user turns. The assessor reviewed all five responses and checked the actual profile and file mutations. All four cases passed. Exact responses, fixture hashes, profile evidence, and case assessments are recorded in [the smoke results](travel_like_a_local_smoke_results.json).

The tested Codex skill's eight-file content hash was `ad4dceaf30205e7a7bc6222c4fef815cfb7ac9e7bfc6c06b13ab8e90a79f768b`. The results file defines the hash method. The same model and reasoning settings were inherited from this session; their exact identifiers were not separately exported by the harness.

These are single-run, offline behavioral smoke checks, not comparative benchmarks, live booking acceptance, or proof of Claude/Copilot runtime behavior. Shared-resource tests establish package consistency across those clients. Rerun the behavioral cases when relevant instructions change; ordinary unit-test execution does not launch agents or repeat these smoke runs.
