---
name: reposlide
description: Research a repository and its public site, then write one self-contained prompt to paste into Claude in PowerPoint that builds a single slide about the project. Use for an explicit reposlide invocation or a request for a one-slide prompt about a repo. Writes the prompt only; does not create or edit a deck.
argument-hint: "[repo path or GitHub URL] [audience or angle]"
---

# RepoSlide

Invoke as `/reposlide` (Claude Code, GitHub Copilot) or `$reposlide` (Codex). With no argument, the subject is the repository you are working in. An argument may name another repo (path or GitHub URL) and an audience or angle to favor. This package runs unchanged in every host; use whichever file, shell, and web tools the host gives you.

The owner pastes your output into Claude in PowerPoint to build ONE slide about this project for their presentation. Claude in PowerPoint cannot see the repo, so every word and URL the slide needs must be in the prompt.

## 1. Research

Repo first, then the public site and GitHub page. Read, do not change anything.

- **Repo:** `README`, manifests (`package.json`, `pyproject.toml`, `*.csproj`, `Package.swift`, `pubspec.yaml`), `LICENSE`, changelog or tags, deployment config (workflows, `azure.yaml`, `staticwebapp.config.json`, Bicep, Terraform, Dockerfiles), and `git remote -v`.
- **Public:** the GitHub page (`gh repo view --json name,description,homepageUrl,licenseInfo,stargazerCount,visibility,defaultBranchRef,latestRelease`; contributors from `gh api repos/<owner>/<repo>/contributors`) and the live site or homepage if one exists.

Collect:

- Name, one-line tagline, the problem it solves, and who it is for.
- 3–4 key features or highlights.
- Tech stack and where it runs (for example, the Azure services).
- Concrete facts worth showing: version, license, stars or contributors, live URL, repo URL.
- Usable visuals: screenshot or logo files in the repo.

## 2. Verify

- Use only facts you can trace to a file or a page you fetched. Leave out anything with no source.
- Put `[VERIFY]` directly after any value you found but could not confirm (a URL that did not load, a version that disagrees between files, a count you could not fetch) so the owner fixes it before pasting.
- Stars and contributors come only from a live lookup, never from memory or a badge image.
- **Images:** never invent, draw, or describe a stand-in logo. Give a URL only for a file committed on the default branch of a public repo: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>`, and confirm it loads. Prefer a product screenshot over a logo. For a private repo, an unpushed file, or no remote, give no URL; name the repo-relative file for the owner to add manually. With no usable image, the placeholder says which screen to capture.

## 3. Write the prompt

Fill this shape with literal content. Count the words against each limit before you output.

```text
Add ONE new slide to this presentation about <Name>. Use only the content below; do not add facts.

Title (≤6 words): <title>
Subtitle (≤12 words): <tagline>

Bullets (3–4, ≤10 words each):
- <highlight>

Layout:
- Text on the left; screenshot or logo on the right.
- Image: insert <raw GitHub URL>. If you cannot insert it, leave a placeholder labeled "<image to add manually>".
- Footer, small: <tech stack and where it runs>
- Bottom corner, small: <repo URL>

Speaker notes (2–3 sentences to say aloud): <notes>

Style: match the deck's existing theme, fonts, and colors. Minimal text. No emoji, clip art, or made-up icons or logos.
```

When there is no image URL, the Image line is only the placeholder telling the owner which image to add. Put version, license, stars, and live URL where they earn their place: a bullet, the footer, or the speaker notes.

## 4. Output

Reply with a single fenced code block containing the PowerPoint prompt, and nothing else: no preamble, no summary, no notes after it, no file written.
