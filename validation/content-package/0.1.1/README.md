# Content package checker 0.1.1: actual verification / 实际验证

By BBQ / BBQ Growth Lab. Executed 2026-10-16. AI implementation and independent AI code review; no human or target-reader sign-off.

A real input-validation gap in 0.1.0 accepted a space/newline as a quotation if present in source bytes. Before fixing it, 41 content-checker test methods produced eight failures (seven whitespace subcases plus the CLI regression). The patch only changes the version and enables the existing nonblank check for claim quotes; it returns the original meaningful string without stripping.

The complete suite passed 52 tests: 41 content-checker methods (three added), and 11 unchanged GEO/SEO fixture methods. Seven whitespace variants were tested with exact bytes present in the temporary source. A meaningful quotation with surrounding whitespace passed only when its original bytes matched; absent trailing whitespace still blocked. Sources and drafts were not modified by the checker. These are program tests, not seven real customers or Skill-host tests.

[RUN.json](RUN.json) binds the tested checker/tests and complete example reports. Only its recorded Python 3.9.6/macOS environment was exercised. The measured suite duration is test execution time, not authoring efficiency or a comparison with a person.

| Actual input | Result | Output |
|---|---|---|
| Complete mappings | exit 0 / structure_ready | [package.report.json](package.report.json) |
| Omitted opening | exit 2 / DRAFT_COVERAGE_MISMATCH | [missing-opening.report.json](missing-opening.report.json) |
| Withdrawn C1 used in both drafts | exit 2 / INACTIVE_CLAIM | [withdrawn-claim.report.json](withdrawn-claim.report.json) |
| Newline-only C1 quote | exit 2 / EMPTY_STRING at $.claims[0].quote | [whitespace-quote.report.json](whitespace-quote.report.json) |

本次仅拒绝按 Python 字符串定义判定的纯空白引文，不裁剪有内容引文，不声称识别所有不可见或无意义文本。旧版本和原验证记录保留；schema_version 仍为1。Codex/WorkBuddy Skill没有重测，Skill仍是v0.3.0实验版。所有输出保持 semantic_review=NOT_PERFORMED、publication_ready=false，不证明来源真实、改写成立、权限完备或SEO/GEO效果。

From the repository root, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/check_content_package.py examples/content-package/package.json
python3 scripts/check_content_package.py examples/content-package/whitespace-quote.json
```

The last command deliberately exits 2; inspect its JSON rather than treating it as an installation failure. Full usage: [English](../../../docs/content-package-check.md) / [中文](../../../docs/content-package-check.zh-CN.md).
