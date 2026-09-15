---
name: bbq-multilingual-seo-check
description: Run a bounded read-only HTTP sample of multilingual pages for status, canonical, hreflang declarations, return links, target language labels and sitemap membership. Use for technical localization checks, not ranking or translation-quality claims.
---

# Multilingual SEO sample

Collect a small set of user-owned or authorized public page URLs and sitemap URLs. Prefer representative locale pairs and high-intent pages; do not expand to a full crawl without scope. See [usage and limitations](references/usage.md).

With Python 3.9+, run `scripts/check.py --url URL --url LOCALIZED_URL --sitemap SITEMAP_URL --output report.json`, resolving script path from this Skill directory. Default budget is 70 requests, maximum 20 seed pages; fetches are read-only and stay within seed/sitemap origins. Do not pass credentials or private URLs. No account access is required.

Read the report before drawing conclusions. Treat `review` as a candidate for manual inspection, not a confirmed site defect. Missing HTML annotations may be supplied by HTTP headers or sitemap extensions. HTML lang is a declaration, not proof of body language. Intentional canonical choices and regional fallbacks need context. `unknown` includes unfetched targets, budget/timeouts and x-default language checks.

Return the sample URLs, observation date, evidence, meaningful candidates and limitations. A clean sample is not a full-site audit, indexation, traffic, or GEO outcome. Do not deploy changes; hand concrete findings to the site's owner.
