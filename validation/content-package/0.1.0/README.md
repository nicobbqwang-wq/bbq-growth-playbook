# Content package checker: actual verification

Date: 2026-10-10. By BBQ / BBQ Growth Lab. Review type: AI implementation and independent AI review; no human or target-reader sign-off claimed.

This record concerns the offline Python checker 0.1.0. The content Skill remains experimental v0.3.0. Codex and WorkBuddy Skill runs were not repeated; historical WorkBuddy unsupported-opening failures remain documented in [v0.3.0](../../content-repurposing/v0.3.0/REVIEW.md).

## Run evidence

[RUN.json](RUN.json) records the actual environment, test count, test execution duration and checker hash. The duration is the measured unittest run, not content-authoring time, a human comparison or a productivity result. Only the recorded Python/macOS environment was exercised; other interpreter versions and operating systems are not claimed tested.

The suite covers normal two-draft packages; omitted opening/end; exact Unicode and CRLF; source bytes/hash changes; absent quotes; inactive/unknown claims; duplicate IDs and JSON keys; malformed input and wrong types; invalid Unicode/BOM; absolute paths, directory traversal and symlink escape; network entry points disabled; CLI exit codes; and unchanged input bytes.

The historical gap class is exercised by removing a mapped opening while retaining the complete draft. This demonstrates structural completeness checking, not semantic detection of unsupported claims and not a new WorkBuddy run.

| Actual example | Expected/observed result | Stored output |
|---|---|---|
| Two drafts with complete mappings | exit 0, `structure_ready` | [package.report.json](package.report.json) |
| English opening omitted from map | exit 2, `DRAFT_COVERAGE_MISMATCH` | [missing-opening.report.json](missing-opening.report.json) |
| C1 withdrawn but used in both drafts | exit 2, `INACTIVE_CLAIM` with affected draft/segment | [withdrawn-claim.report.json](withdrawn-claim.report.json) |

Every report retains `semantic_review=NOT_PERFORMED` and `publication_ready=false`. Source reliability, semantic entailment, honest classification, permissions and real reader usefulness require review beyond this tool. Incorrectly classifying a whole fact-filled draft as editorial can pass: that is a declared limitation, not proof of support.

## Reproduce

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_content_package.py -v
python3 scripts/check_content_package.py examples/content-package/package.json
python3 scripts/check_content_package.py examples/content-package/missing-opening.json
python3 scripts/check_content_package.py examples/content-package/withdrawn-claim.json
```

The three input manifests and local files are checked in; no network, credentials or model access is needed for those commands. The final two commands intentionally return a nonzero status. Tests are supplied separately from the Skill's installation and marketplace records.
