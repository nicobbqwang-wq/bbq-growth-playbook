# Content package checker 0.1.1

By BBQ / BBQ Growth Lab. Maintenance of the offline helper; the experimental content Skill stays v0.3.0.

Fix: a claim quote containing only spaces, tabs, line endings or other Python-recognized whitespace now returns blocked / exit 2 with EMPTY_STRING. Previously, a space or newline found in the source could be accepted as an excerpt. Nonblank quotes are never stripped: exact whitespace, Unicode and line-ending matching remain required.

Includes a reproducible whitespace-quote.json negative example and three regression methods. The full suite runs 52 tests in the recorded Python 3.9.6 environment. Other Python versions/operating systems and Codex/WorkBuddy Skill execution were not retested.

Every report retains semantic_review=NOT_PERFORMED and publication_ready=false. The fix does not detect all visually invisible text, validate a paraphrase, approve publication or establish search/AI visibility.

[English usage](docs/content-package-check.md) · [中文用法](docs/content-package-check.zh-CN.md) · [Actual verification](validation/content-package/0.1.1/README.md)

Source method: https://bbqgrowthlab.com/zh-cn/articles/content-repurposing-map-seo-llm-visibility/
