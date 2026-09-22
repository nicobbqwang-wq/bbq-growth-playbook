# v0.3.0 behavioral review — 2026-09-22

This experimental update turns the website article's method into an optional traceable content package. It does **not** resolve every factual-fidelity failure. Three synthetic cases ran once per environment. Review was by an AI agent; human sign-off remains pending.

| Case | Codex CLI 0.155.0-alpha.9.2 | WorkBuddy AI international desktop 5.5.2 / Auto |
| --- | --- | --- |
| Normal adaptation + cards | Pass: source locators, limitations and one draft retained | Fail: cards and map generated, but the opening generalizes reader experience and adds a speed implication |
| Title only, no material | Pass: no finished adaptation or doubling claim; offered original drafting as a separate path | Pass boundary: requests source material; test ends at Pending Confirmation |
| Corrected fictional source | Pass: C2 7→5, IDs, ownership, fictional status and limits retained | Fail overall: revision and attribution correct, but opening adds an unsupported reader assumption |

There was no review-assisted retry in this release. Do not present these results as full WorkBuddy compatibility or a model comparison. The Auto model is unknown; Codex's default model was not exposed in captured logs. Cases differ from the historical v0.2.0 suite, so aggregate scores are not a before/after benchmark.

## Evidence

| Case | Input | Codex output | WorkBuddy UI observation |
| --- | --- | --- | --- |
| Normal | [input](normal.input.md) | [output](normal.codex.output.md) | [draft excerpt and findings](normal.workbuddy.observation.md) |
| Insufficient | [input](insufficient.input.md) | [output](insufficient.codex.output.md) | [request for materials](insufficient.workbuddy.observation.md) |
| Attribution/revision | [input](attribution.input.md) | [output](attribution.codex.output.md) | [draft excerpt and findings](attribution.workbuddy.observation.md) |

Codex explicitly read the repository SKILL.md and linked template in ephemeral read-only runs. Automatic discovery was not tested. WorkBuddy used the installed Skill selected from the slash menu. Its same-name ZIP upgrade was rejected after a successful security scan; the installed folder was backed up and the three Skill files replaced, preserving private app metadata, then the app was restarted. Installed file hashes matched the repository. See [installation](../../../docs/installation.md).

One earlier UI-harness attempt submitted garbled text and was stopped; it is excluded because it did not contain a valid fixture. The three valid inputs above were verified in the UI before sending. WorkBuddy observations are transcriptions/excerpts, not complete raw execution logs; account information is excluded.

No generated test drafts were posted externally. No URL-fetch, mainland WorkBuddy, other app versions, measured growth outcome or human review is claimed. The public synthetic fixture is a behavior test, not a customer success story.

## Editorial action before using a generated draft

Check the opening and connective sentences as carefully as figures and citations. Remove unsupported assumptions about readers and unmeasured speed claims. Keep necessary fictional labels and limitations in the draft itself; a correct claim table cannot repair unsupported prose. Recheck any revisions before publication.
