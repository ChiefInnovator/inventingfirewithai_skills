# Travel Like a Local: ChatGPT web migration

Web setup status recorded September 25, 2026. Export refreshed October 29, 2026 to match the current repository source.

## Source and export

The canonical source for this export is [the Codex travel skill](../../skills/codex/travel-like-a-local/SKILL.md). The [downloadable ZIP](../../assets/distributions/travel-like-a-local.zip) preserves its complete folder, including `agents/openai.yaml`, `assets/icon.svg`, `references/traveler-profile.md`, and `references/trip-operations.md`, plus venue research, day planning, and experience references. The traveler-profile reference defines onboarding and storage rules only; no personal profile is bundled. Keep changes in the source folder and regenerate the archive when those files change.

This is a skill source archive, not an installable plugin package. Installing a local Codex skill does not establish that it is available in ChatGPT on the web.

## Proposed web setup

Where the account supports skill creation, open a Work chat, attach the ZIP, select `@skill-creator`, and use:

> Create a personal skill named Travel Like a Local from the attached package. Preserve its instructions and supporting reference files. Make it available for my future travel chats.

Complete the creation flow exposed by that account. Then start a new chat and look for the saved skill in the `@` selector. Workspace skills, local filesystem skills, and plugin installations have separate controls. A plugin is another distribution path, but this archive does not include a plugin manifest or marketplace setup.

The creator workflow is documented; importing this particular ZIP and persisting its references in a web account have not been tested. Account availability and exact UI steps remain to be verified. Source documentation is cataloged in [references.md](../../references.md#docsmigrationstravel_chatgpt_webmd).

## Acceptance checklist

- [x] Export the existing skill with all supporting files.
- [x] Verify that archive contents match the repository source byte for byte.
- [ ] Verify the web account exposes the skill creation flow.
- [ ] Create and enable the personal skill in that account.
- [ ] Confirm it appears in a fresh chat and can read its supporting references.
- [ ] Test city exploration and remote-property relaxation requests; confirm it asks only for missing trip context and researches current practical details.

## Regenerate the archive

Run from the repository root with Python 3:

```python
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

source = Path("skills/codex/travel-like-a-local")
output = Path("assets/distributions/travel-like-a-local.zip")
output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(output, "w", ZIP_DEFLATED) as archive:
    for file in sorted(source.rglob("*")):
        if file.is_file():
            archive.write(file, Path(source.name) / file.relative_to(source))
```
