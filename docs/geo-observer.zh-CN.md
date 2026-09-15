# GEO 人工观察整理助手

[English](geo-observer.md) · [Skill 入口](../skills/bbq-geo-observer/SKILL.md) · [字段说明](../skills/bbq-geo-observer/references/schema.md)

它整理已经导出的真实回答，当前没有接通任何模型。需要 Python 3.9+，无需安装依赖：

```sh
python3 skills/bbq-geo-observer/scripts/observe.py examples/geo-fixture.json --output geo-report.json --dataset-kind fixture
```

真实采样换为自己的 JSON/CSV，并使用 `--dataset-kind real_manual_export`。保留完整 answer_text、问题、时间、产品/模式、语言和来源。旧版 CSV 中只有 answer_record 路径时，要明确读取获准的原文并填入 answer_text；程序不会自动打开输入中的任意文件路径。

[测试输入](../examples/geo-fixture.json)和[输出](../examples/geo-fixture-report.json)全部是虚构夹具，覆盖身份矛盾、未执行、未判定提及三个情况，不代表 BBQ、客户或任何真实模型的成绩。

输出分别记录：人工报告的 mentioned、字面匹配候选、身份判断、引用 URL、人工主张支持记录，以及 unknown。未登录/未采样不算未提及。提到名字不证明身份正确；列出链接不证明来源支持主张。原始记录完整保留，正文计算 SHA-256 便于核对。程序不自动产生可见度评分或跨条件趋势。公开输出前需核对原文的公开权限。
