# Input schema / 输入格式

Python 3.9+, standard library only. JSON array, an object with `observations` array, or UTF-8 CSV. Legacy `templates/geo-observations.csv` is supported. Blank values stay unknown. CSV `cited_urls` accepts JSON arrays or semicolon-separated URLs.

Core: run_id, observed_at (ISO timestamp), product_entry, visible_version, search_mode, language, region, session_conditions, question_group, question, target_entity, answer_status, answer_text, mentioned, identity_verdict, cited_urls, claim_source_support, reviewer_notes.

`answer_status`: answered / not_run / blocked / error; retain other supplied status names. `answer_text`: exact full answer, not a generated summary. `answer_record` may point to a local original but is preserved without being opened. `target_aliases`: optional JSON array. `mentioned`: true / false / unknown from supplied review. `identity_verdict`: accurate / inaccurate / mixed / contradictory / not_applicable / unknown.

`claim_source_support`: unknown or supplied review such as [{claim, url, verdict, evidence_quote, reviewed_at, reviewer}]. The tool retains this review but does not validate it. Use supported / unsupported / contradictory / unknown for per-claim verdicts. URLs and answer mentions are separate evidence categories.

输出保留 raw 全字段与完整 answer_text；SHA-256 用于核对正文是否变化。literal_mention_candidate 仅为大小写不敏感字面匹配，不会覆盖人工 mentioned。矛盾项写入 warnings。未采样不记为 0；不自动给提及率，不宣布身份准确或引用有效。不要在公开仓库提交私人原文、后台截图或本地路径。

Optional supplied tri-state fields search_triggered and target_entity_correctly_identified are normalized separately. A named search mode does not prove search occurred, and a literal name match does not prove correct entity identification. Original fields remain in raw.
