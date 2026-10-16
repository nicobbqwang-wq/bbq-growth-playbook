# Check a content package before editorial review

By BBQ / BBQ Growth Lab. [简体中文](content-package-check.zh-CN.md)

Use this offline helper when adapting a source into several drafts. It can catch an opening omitted from the evidence map, an altered source snapshot, or a withdrawn claim still used in a draft. It checks the package's declared structure; an editor still needs to judge whether the source supports each passage.

## Start with the included demonstration

Python 3.9 or later; standard library only. Run from the repository root:

```sh
python3 scripts/check_content_package.py examples/content-package/package.json
python3 scripts/check_content_package.py examples/content-package/missing-opening.json
python3 scripts/check_content_package.py examples/content-package/withdrawn-claim.json
python3 scripts/check_content_package.py examples/content-package/whitespace-quote.json
```

The first exits 0. The other three exit 2: an omitted opening, a withdrawn claim used in both drafts, and a whitespace-only quotation. JSON goes to stdout; the command does not fetch URLs, call an AI model, publish content or modify its inputs. Redirect the report to a local file if needed. Reports can contain user-supplied IDs and file locations; review them before sharing.

The demonstration adapts two short method excerpts from [BBQ's content map](https://bbqgrowthlab.com/zh-cn/articles/content-repurposing-map-seo-llm-visibility/) into an English professional-network draft and a Chinese newsletter draft. Both are unposted demonstrations, with no measured performance or platform-limit compliance claim. The [example notes](../examples/content-package/README.md) explain the choices and manual checks.

## Prepare your own package

1. Put local UTF-8 source snapshots and complete draft files in one folder, preserving exact whitespace. The tool reads files inside that folder; keep unrelated private material elsewhere.
2. Record SHA256 for each source's bytes. The checked snapshot is not a live website check. Updating a source requires a new hash and a fresh editorial review.
3. Give each claim an ID, source ID, an exact quotation containing at least one non-whitespace character and a status: `active`, `withdrawn` or `unresolved`.
4. Map the entire draft, including titles, openings, transitions, closing actions and line endings. The ordered segment texts must concatenate to exactly the draft file.
5. Classify each segment. `sourced` requires active claim IDs. `editorial`, `synthetic` and `disclosure` require an explanatory `review_note`; they do not establish factual support. A wrong classification can pass this checker and needs editorial review.
6. Run the checker. Fix structural errors, then review meaning, attribution, conditions, permissions, hypothetical labels and channel usefulness.

## Input contract

See [package.json](../examples/content-package/package.json) for the complete input. `schema_version` must be the integer 1. `sources`, `claims`, `drafts` and each draft's `segments` must be nonempty arrays. IDs must be nonempty and unique within their collection. Paths are relative to the manifest folder; absolute paths, traversal outside it and symlink escape are rejected.

| Object | Required fields | Meaning |
|---|---|---|
| source | `id`, `path`, `sha256` | Local snapshot and expected 64-hex byte hash |
| claim | `id`, `source_id`, `quote`, `status` | Exact excerpt and declared use state; active is not independently verified |
| draft | `id`, `path`, `segments` | Complete local draft, with ordered mapping |
| sourced segment | `text`, `kind: "sourced"`, `claim_ids` | Nonempty passage and active dependencies |
| other segment | `text`, `kind`, `review_note` | Editorial proposal, synthetic material or disclosure; no claim IDs |

Since 0.1.1 a quotation containing only whitespace is rejected with EMPTY_STRING at its quote field, even if those bytes occur in the source. The nonblank check uses Python string whitespace detection; it is not a detector of meaningless or visually invisible text. Meaningful quotations are not stripped or rewritten: leading/trailing whitespace and line endings must still match.

No whitespace or Unicode normalization is applied. BOM, malformed UTF-8, invalid/duplicate JSON keys and invalid types are rejected. Use UTF-8 without a BOM. CRLF and LF remain distinct. When exporting JSON, preserve the intended text and newline characters.

## Read the result

Exit 0 means `structure_ready`; exit 2 means `blocked`. Errors include a code and a location. Each draft lists its length, segment count and claim dependencies, which helps locate the drafts affected by a withdrawn claim. A matching hash and quotation only verify the supplied bytes and exact text.

Every report retains `semantic_review: "NOT_PERFORMED"` and `publication_ready: false`. The checker cannot prove that a paraphrase follows from its citation, that classifications are honest, that permissions are valid, or that a current source is trustworthy. A full file could be incorrectly labelled editorial and pass: review classification as well as the report.

The content Skill remains experimental v0.3.0. Python validation is a separate tool result; Codex and WorkBuddy Skill runs were not repeated for this tool release. Actual tested environments are recorded in [the test record](../validation/content-package/0.1.1/README.md).
