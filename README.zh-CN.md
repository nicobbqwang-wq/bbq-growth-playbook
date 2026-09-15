# BBQ Growth Playbook

让真实专业积累更容易被理解和使用：内容分发、人工 AI 回答观察、多语言 SEO 小样本检查。

作者 [BBQ](https://github.com/nicobbqwang-wq) · [BBQ Growth Lab](https://bbqgrowthlab.com/zh-cn/) · [English](README.md)

## 选择一个任务开始

| 你要完成的事 | 入口 | 得到什么 |
| --- | --- | --- |
| 把文章改为另一渠道的有用内容 | [中文安装与调用](docs/installation.zh-CN.md) · [Skill](skills/bbq-content-repurposing/SKILL.md) | 一份按要求生成的草稿、出处和检查记录 |
| 整理人工导出的 AI 回答 | [GEO 观察助手](docs/geo-observer.zh-CN.md) | 完整原文、提及候选、身份与引用人工记录、unknown |
| 检查少数语言版本 | [SEO 脚本与说明](skills/bbq-multilingual-seo-check/references/usage.md) | 状态码、canonical、hreflang、返回链接、sitemap 证据 |
| 统一公开个人资料 | [事实表](templates/personal-ip-fact-sheet.md) | 主张、来源、适用范围和核实状态 |
| 理解个人 IP 的 AI 可见性 | [方法指南](guides/personal-ip-ai-visibility.zh-CN.md) | 可重复的观察步骤与问题 |
| 查官方参考资料 | [资源索引](resources/README.zh-CN.md) | 按用途分类的来源 |

## v0.2.0 实际验证到哪里

内容分发：Codex CLI 0.154.0-alpha.6.2 已真实执行正常输入、资料不足、事实归属与局限三个场景，实际读取 Skill 文件的显式调用模式通过代理逐项评审。真人复核、自动发现、链接抓取与发布尚未验证。WorkBuddy AI 国际桌面版 5.5.2（Auto）已安装 Skill 并运行三场景：1 项首次通过，2 项在明确复核意见后修订通过。只能称“需要逐稿复核的可用流程”，不能称无人复核全通过；国内网页版未实测。

GEO：Python 3.9.6 下，测试夹具和六项行为测试通过；只整理人工导出，没有自动接通模型。SEO：同环境五项本地 HTTP 夹具测试通过，并检查了官网中英文服务/关于页四个起始 URL。这不是全站审计，不证明收录、排名或转化。

GEO/SEO Skill 文件格式有效，但其代理端调用未单独实测；脚本可直接用 Python 运行。详见 [兼容矩阵](validation/compatibility.json)、[内容分发输入输出](validation/content-repurposing/REVIEW.md)和[官网小样本证据](validation/seo/README.md)。示例是明确演示，人工评审表待用户填写。

文件读取测试发现旧版面对只有标题的改写请求会给出整篇原创建议稿；本版修复这一范围问题并重跑三场景，补齐使用证据，新增两个范围有限的助手。发布页提供单技能 ZIP 和完整源码。

## 最短使用

让 Codex 读取 `skills/bbq-content-repurposing/SKILL.md`，按 `examples/content-repurposing-input.md` 输出一篇英文 LinkedIn 草稿及事实检查。真实任务请附正文、读者、渠道、语言和行动。只有标题时先补素材，不能编造原文或业绩。

资源发布、被发现、AI 提及、来源支持与有效咨询分别记录。工具不承诺提效、排名、模型收录或客户收益，也不会自动发帖。脚本只依赖 Python 标准库；处理私人样本不代表获准公开样本。

[完整内容分发文章](https://bbqgrowthlab.com/zh-cn/articles/content-repurposing-map-seo-llm-visibility/) · [贡献说明](CONTRIBUTING.md) · [MIT 许可](LICENSE)。外部材料保留原许可。
