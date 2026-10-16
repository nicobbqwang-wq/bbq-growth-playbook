# One source, two draft tasks / 同一来源，两种任务

By BBQ / BBQ Growth Lab. Created and AI-reviewed on 2026-10-10. No human sign-off, posting, recipient response or outcome measurement is claimed.

The input is two short method recommendations from [BBQ's content map](https://bbqgrowthlab.com/zh-cn/articles/content-repurposing-map-seo-llm-visibility/), saved in [source.md](source.md). The public article was checked on 2026-10-10 and both exact excerpts were present. C1 describes retaining source and boundaries; C2 describes reviewing derived versions after an update. `active` is a declared editorial use state, not independent verification of the method's effectiveness.

| Draft | Reader task | Choice |
|---|---|---|
| [English professional-network draft](linkedin-en.md) | Review what must accompany a reused claim | Gives the source method and a small checking action within the draft; no claims about what most readers do |
| [Chinese newsletter draft](newsletter-zh-CN.md) | Locate still-used versions affected by a changed claim | Uses an update-oriented task and suggests a local inventory; not a translation of the first post |

The two tasks share C1 and C2 but use different openings and actions. Advice from the article stays advice. New action suggestions are marked `editorial` in the separate map; source URLs and demonstration limitations are `disclosure`. Mapping IDs stay out of the channel drafts.

人工语义判断仍需要逐段比较原文、改写、条件与分类。此处逐段 AI 复核发现：归属保留、没有客户成绩/效率承诺/虚构数字，建议仍为建议；开头和结尾均在映射内。但 AI 复核不等于真人审校或目标读者验收。

## Reproduce / 复现

From the repository root:

```sh
python3 scripts/check_content_package.py examples/content-package/package.json
python3 scripts/check_content_package.py examples/content-package/missing-opening.json
python3 scripts/check_content_package.py examples/content-package/withdrawn-claim.json
python3 scripts/check_content_package.py examples/content-package/whitespace-quote.json
```

1. `package.json` must return exit 0, `structure_ready`, two mapped drafts. `semantic_review=NOT_PERFORMED` and `publication_ready=false` are retained.
2. `missing-opening.json` keeps the same English draft but deliberately omits its first segment. It returns exit 2 and `DRAFT_COVERAGE_MISMATCH` for that draft. This reproduces the mapping gap class, not a new WorkBuddy run or a semantic detector of unsupported hooks.
3. `withdrawn-claim.json` marks C1 withdrawn while both drafts still reference it. It returns exit 2 with `INACTIVE_CLAIM` errors identifying the affected drafts and segments. No posted content is edited automatically.
4. Change a byte in a copied source snapshot while preserving its old hash: the report must block. Restoring the file restores the original check; updating only the hash still requires new semantic review.

Full actual reports are in [the validation directory](../../validation/content-package/0.1.0/). They record what was checked, not semantic approval, Skill compatibility or effectiveness. No platform length limits were asserted or tested.

## 0.1.1 whitespace-only quote regression / 空白引文回归

`whitespace-quote.json` keeps the same source and drafts but sets C1’s quotation to a newline. In 0.1.0 it incorrectly exited 0 because that newline exists in the source. In 0.1.1 it exits 2 with EMPTY_STRING at $.claims[0].quote. This is an intentionally malformed demonstration, not an allegation about a customer package. Meaningful quotes retain their exact whitespace.

Updated run evidence: [0.1.1](../../validation/content-package/0.1.1/README.md). The 0.1.0 evidence above remains historical. The source method excerpts were rechecked on 2026-10-16; neither this input fix nor the examples establish semantic truth, host Skill compatibility or SEO/GEO effects.
