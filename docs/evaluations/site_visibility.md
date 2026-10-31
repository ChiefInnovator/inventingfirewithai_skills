---
title: Site discovery and validation
description: SEO, GEO, and AEO maintenance for the Inventing Fire with AI Skills site, including crawlable content, metadata, structured data, and deployment checks.
---

# Site discovery and validation

The public site presents five reusable skills for Codex, Claude Code, and GitHub Copilot. SEO, generative engine optimization (GEO), and answer engine optimization (AEO) maintenance keeps that information accessible, factual, and consistent. It does not establish search rankings, indexing, recommendations, or AI citations.

## What is maintained

- The homepage identifies the complete library in its title, description, heading, canonical URL, and social metadata. Skill descriptions, installation answers, validation coverage, and source links are available in the HTML without executing JavaScript.
- JSON-LD describes the site, author, and visible skill collection. It contains no invented reviews, ratings, prices, awards, or performance claims. Keep machine-readable facts aligned with the visible page.
- Jekyll renders the Markdown documentation with site metadata from `_config.yml`. Important documentation has its own description. Sitemap entries use canonical rendered `.html` URLs; source links remain available separately.
- `sitemap.xml` lists public pages. The optional `llms.txt` is a factual reading index, not an access-control file, an instruction to assistants, or proof of support by a search or AI provider.
- Public documentation links to repository files outside the Pages publish directory use GitHub source URLs. Local paths outside the repository and private profile/trip state do not belong in published content.

Google's [AI search guidance](https://developers.google.com/search/docs/appearance/ai-features) applies the usual SEO fundamentals: accessible text, useful links, a good page experience, and structured data matching the page. It does not require special AI files or promise that an eligible page will be indexed or cited. Schema types are selected for the actual content, including [SoftwareSourceCode](https://schema.org/SoftwareSourceCode) for the skill collection.

## Hosting and crawler scope

The canonical site is `https://chiefinnovator.github.io/inventingfirewithai_skills/`, served from `main:/docs`. This is a GitHub Pages project site, not the domain root. Preserve Jekyll: existing rendered documentation URLs depend on it. See [GitHub's Pages and Jekyll documentation](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll).

Crawler directives are read from `https://chiefinnovator.github.io/robots.txt`. A file under the project subpath would not control those crawlers. During the October 31, 2026 baseline check, the host-root file returned HTTP 404, so there were no published root directives at that time. Google's [robots specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec) documents root scope and ordinary 4xx handling. Recheck the actual host response rather than inferring policy from a file in this project. Changes to domain-root crawler policy are separate from this repository's deployment.

## Regression and deployment checks

Run the repository test suite from its root:

```sh
uv run --no-project --python 3.14 --with-requirements tests/requirements.txt python -m unittest discover -s tests
```

[Site regression tests](https://github.com/ChiefInnovator/inventingfirewithai_skills/blob/main/tests/test_pages_visibility.py) check the actual metadata, crawlable content, structured data, links, sitemap, and reading index. [Travel tests and smoke evidence](travel_like_a_local_evaluation.md) distinguish deterministic package verification from agent behavior and live-service acceptance.

The `Skills and site checks` GitHub Actions workflow runs the root suite for pull requests into `develop` and `main` and for pushes to those branches. Its package and visibility checks report failures before publishing; the separate main-source guard enforces the `develop`-to-`main` route.

After deployment, fetch the canonical homepage, sitemap, reading index, representative rendered documentation, source links, and social image. Verify the published text and metadata against the merged source, check HTTP status and the Pages build commit, and inspect desktop and narrow-screen rendering. Account for CDN cache headers before diagnosing stale content. Record source checks, deployment, and indexing/citation observations separately; a successful Pages build is not evidence that a search or AI service has indexed the update.
