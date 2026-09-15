# BBQ Growth Playbook

Practical resources for making professional expertise understandable and useful: content adaptation, manual AI-answer observations, and small multilingual SEO checks.

By [BBQ](https://github.com/nicobbqwang-wq) · [BBQ Growth Lab](https://bbqgrowthlab.com/en/) · [简体中文](README.zh-CN.md)

## Start with one task

| Task | Start here | Result |
| --- | --- | --- |
| Adapt one article without losing its evidence | [Install and invoke](docs/installation.md) · [Content Skill](skills/bbq-content-repurposing/SKILL.md) | One requested draft, source attribution and editorial checks |
| Organize exported AI answers | [GEO assistant](docs/geo-observer.md) | Original answers, mention candidates, supplied identity/source reviews and unknowns |
| Check a few language variants | [SEO checker](skills/bbq-multilingual-seo-check/references/usage.md) | HTTP, canonical, hreflang, return-link and sitemap evidence |
| Establish consistent public author facts | [Fact sheet](templates/personal-ip-fact-sheet.en.md) | Claims, source links, scope and review status |
| Understand personal-brand AI visibility | [Guide](guides/personal-ip-ai-visibility.md) | Questions and an observation workflow |
| Find supporting references | [Curated resources](resources/README.md) | Official sources grouped by reader task |

## What is verified in v0.2.0?

| Resource / environment | Actual verification | Remaining limits |
| --- | --- | --- |
| Content / Codex CLI 0.154.0-alpha.6.2 | Three recorded explicit Skill-file reads and runs: normal input, insufficient material, attribution/factual limits | Agent review; human sign-off and automatic discovery pending; no URL-fetch/publication test |
| Content / WorkBuddy AI desktop 5.5.2 (Auto) | Three installed-Skill cases run; one passed first response, two passed after explicit review feedback | Review-assisted only; initial failures retained; mainland web product untested |
| GEO / Python 3.9.6 | Offline synthetic fixtures and six behavior tests | No automatic model integration; real sampling belongs to a separate collection step |
| SEO / Python 3.9.6 | Five local HTTP fixture tests and four live seed pages | Bounded HTML sample, not a full audit or proof of indexing |
| GEO and SEO / Codex or WorkBuddy Skill invocation | Package format checked | Agent invocation not separately tested; scripts run directly in Python |

See [behavioral inputs/outputs](validation/content-repurposing/REVIEW.md), [compatibility data](validation/compatibility.json), and [SEO live evidence](validation/seo/README.md). Synthetic examples are demonstrations, not customer results. Human review forms are intentionally unfilled.

A file-read test exposed an overbroad response to a title-only adaptation request. v0.2.0 narrows that behavior, reruns the three scenarios, and adds installation, evidence and two bounded helpers. Each release provides individual Skill ZIPs and source code.

## Smallest useful content example

Ask Codex to read `skills/bbq-content-repurposing/SKILL.md` and use `examples/content-repurposing-input.md`. Request one English LinkedIn draft and factual checks. For your own material, supply the body, intended reader, channel, language and reader action. A title alone is insufficient for faithful adaptation.

## Boundaries

Published resources, search discovery, AI mentions, supported citations and qualified inquiries are different outcomes. This repository does not promise rankings, revenue, model inclusion, or automatic posting. Scripts use the Python standard library; read the relevant guide before running on your data. No private samples or account credentials are needed for the bundled examples.

## Learn more and contribute

[Content repurposing article](https://bbqgrowthlab.com/en/articles/content-repurposing-map-seo-llm-visibility/) · [Cross-platform AI advice](https://bbqgrowthlab.com/en/articles/ai-optimization-advice-not-portable-cross-platform/) · [AI-assisted workflows](https://bbqgrowthlab.com/en/articles/ai-assisted-seo-geo-ppc-workflow-field-notes/)

[Contributing](CONTRIBUTING.md) · [MIT License](LICENSE). Linked third-party material retains its own license.
