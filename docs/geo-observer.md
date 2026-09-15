# GEO observation assistant

[中文](geo-observer.zh-CN.md) · [Skill](../skills/bbq-geo-observer/SKILL.md) · [Schema](../skills/bbq-geo-observer/references/schema.md)

This is an offline organizer for manually exported answers. It does not connect to ChatGPT, Doubao, DeepSeek or other models. Run with Python 3.9+:

```sh
python3 skills/bbq-geo-observer/scripts/observe.py examples/geo-fixture.json --output geo-report.json --dataset-kind fixture
```

For real exports, provide JSON or CSV following the schema, put the full answer in `answer_text`, and change the flag to `--dataset-kind real_manual_export`. Missing answers remain unknown. The supplied raw record and exact answer are retained, with an answer hash for integrity checks. The old CSV's `answer_record` field is preserved but not read as a file path; explicitly add the permitted answer text first.

[Fixture input](../examples/geo-fixture.json) and [output](../examples/geo-fixture-report.json) are synthetic. They show a contradictory identity, a not-run product and an answer without a reviewed mention. Nothing here represents a real model or customer result.

A literal name match is only a candidate. Supplied mention/identity/source-support reviews are retained separately. A source URL is not proof of a claim. The tool does not calculate visibility rates or trends without comparable sampling conditions. Review raw data before sharing: local exports may contain private information; processing does not grant publication permission.
