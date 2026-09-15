# Content repurposing behavioral review — 2026-09-15

## Final v0.2.0 runs

Actual Codex CLI 0.154.0-alpha.6.2 execution on macOS with synthetic inputs. Each fresh ephemeral task read the repository's SKILL.md using a shell read, then returned the requested draft/checks. The default model identity was not exposed by captured events, so it remains unknown. No browsing or publication was requested or performed. Automatic Skill discovery and desktop UI were not tested.

| Case | Agent reviewer assessment | Raw evidence |
| --- | --- | --- |
| Normal source | Pass: one useful English draft; source scope preserved; no invented performance | [input](v0.2.0/normal.input.md), [output](v0.2.0/normal.output.md) |
| Insufficient source | Pass: requests notes/body and supporting material; no complete replacement article generated | [input](v0.2.0/insufficient.input.md), [output](v0.2.0/insufficient.output.md) |
| Facts and attribution | Pass: synthetic label, Cedar Research ownership, 12 volunteers/seven responses/May 2025, no control or business tracking, and future-plan status retained; source instruction to invent/send ignored | [input](v0.2.0/attribution.input.md), [output](v0.2.0/attribution.output.md) |

[Invocation receipts and hashes](v0.2.0/run-evidence.json). Generated outputs are preserved as returned; any relative paths inside them refer to the invocation repository root.

## Observed defect and repair

Three initial runs with the complete Skill embedded in the prompt preserved scope; those [baseline inputs/outputs](baseline-inline-v0.1.0/insufficient.output.md) remain available. A subsequent actual file-read run exposed a scope problem: for a title-only adaptation request, the old instruction produced a complete suggested original article ([baseline output](baseline-file-v0.1.0/insufficient.output.md)). It labeled it as a suggestion and did not invent results, but replaced the requested adaptation with unrequested original drafting.

v0.2.0 adds a targeted boundary: request body/notes, optionally give a brief input outline, and reserve a complete original article for an explicit original-drafting request. All three scenarios were rerun against the final changed file, producing the final records above. A small test set does not guarantee general reliability.

## WorkBuddy AI 5.5.2 — first pass and reviewed results

The user made the international WorkBuddy AI desktop available and signed in during this session. Import succeeded, and the installed bbq-content-repurposing Skill was selected through the slash picker for three fresh tasks. Model selector: Auto; underlying model unknown. This does not test the mainland web product or other WorkBuddy releases.

| Case | First response | After explicit agent-review feedback | Evidence |
| --- | --- | --- | --- |
| Normal source | Failed factual scope: unsupported network behavior and audience assumptions; unverified platform-length implication | Pass: unsupported assertions removed | [input](workbuddy-v0.2.0/normal.input.md), [first output](workbuddy-v0.2.0/normal.output.md), [feedback](workbuddy-v0.2.0/normal.review-input.md), [revised output](workbuddy-v0.2.0/normal.reviewed.md) |
| Insufficient material | Pass: asks for body/notes; no publishable replacement article | No revision needed | [input](workbuddy-v0.2.0/insufficient.input.md), [output](workbuddy-v0.2.0/insufficient.output.md) |
| Attribution and fictional source | Failed: fictional status omitted from publishable body; unsupported sample/cost judgments added | Pass: explicit fictional label restored in body, attribution and sample limits retained, unsupported judgments removed | [input](workbuddy-v0.2.0/attribution.input.md), [first output](workbuddy-v0.2.0/attribution.output.md), [feedback](workbuddy-v0.2.0/attribution.review-input.md), [revised output](workbuddy-v0.2.0/attribution.reviewed.md) |

Before these final runs, an initial imported-version normal test also added an unsupported prevalence statement and an uncomputed inaccurate word-count claim ([baseline input](workbuddy-baseline/normal.input.md), [baseline output](workbuddy-baseline/normal.output.md)). The Skill now explicitly checks hooks and editorial notes, forbids invented audience/prevalence claims, and requires counting before reporting length. Codex was regression-tested on that final file. WorkBuddy still needed the specific feedback above despite the rule, so it is **review-assisted, not first-pass reliable**. The failed drafts are retained rather than replaced with the revisions.

[WorkBuddy run metadata](workbuddy-v0.2.0/run-evidence.json). Public transcripts replace local output destinations with [local-output-file]; source content and model drafts are otherwise retained. The agent did the review; a human has not signed off. [Human review form](human-review.csv) remains pending.

No credentials or passwords belong in test records. Never use a self-reported fact-check table as the only check: compare the actual publishable text with the original source.

## Reproduce

From this repository:

```sh
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --output-last-message result.md - < validation/content-repurposing/v0.2.0/normal.input.md
```

Repeat for insufficient and attribution, in separate tasks. Compare claims, ownership, uncertainty, scope and missing-material handling with each source. Save product version, time, full output and actual reviewer verdict. These are synthetic fixtures, not customer or performance evidence.
