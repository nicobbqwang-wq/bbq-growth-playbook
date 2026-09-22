# 安装与调用

[English](installation.md) · [真实测试与限制](../validation/content-repurposing/REVIEW.md)


## v0.3.0 升级记录（2026-09-22）

本版内容 Skill 的[使用指南](../guides/traceable-content-repurposing.zh-CN.md)和[实测结果](../validation/content-repurposing/v0.3.0/REVIEW.md)以新记录为准；下方旧版行为结果仅代表 v0.2.0。

WorkBuddy AI 国际桌面版 5.5.2 的 ZIP 安全扫描通过，但同名 Skill 导入被拒绝，不能把这次操作算作成功升级。实际升级路径：在已安装 Skill 的菜单选择 Open in Folder，备份文件夹，用本版 ZIP 中的 SKILL.md 和 assets 覆盖对应文件，保留应用自己的元数据文件，然后重启应用并在新任务中从 / 菜单选择 Skill。测试前已核对三个文件的 SHA-256 与发布源文件一致。不要把个人元数据放进公开 ZIP。

Codex 本版测试通过显式读取仓库里的 Skill 文件执行；自动发现未单独验证。已有项目安装时先备份同名目录，再替换该 Skill 的文件。

## Codex：最短可用方式

下载 v0.2.0 源码包并解压，或运行：

```sh
git clone --branch v0.3.0 --depth 1 https://github.com/nicobbqwang-wq/bbq-growth-playbook.git
cd bbq-growth-playbook
```

在该目录启动 Codex，输入：“读取 skills/bbq-content-repurposing/SKILL.md，按 examples/content-repurposing-input.md 生成一篇英文 LinkedIn 草稿及事实核查记录。”本轮验证的是显式读取指令模式。

需要项目自动发现时，将完整技能文件夹复制到项目 `.agents/skills/`；先检查目标不存在，避免覆盖既有版本。新对话使用 `$bbq-content-repurposing`，附正文、读者、渠道、语言与希望读者采取的行动。未显示时重启或改用显式路径。目录规则来自 [OpenAI 文档](https://learn.chatgpt.com/docs/build-skills)，自动选择尚未实测。

保留技能中的 scripts/references/assets 子目录。内容分发无脚本依赖；GEO 和 SEO 脚本要求 Python 3.9+。可在仓库根目录照各指南运行，也可按安装后的技能目录调整脚本路径。

## WorkBuddy AI：需逐稿复核

登录官方 WorkBuddy，进入技能 → 添加技能 → 上传技能，选择本版本对应单个技能 ZIP。检查已安装与启用状态，在新对话选中技能，分别提交三种测试输入。导入入口参照 [WorkBuddy 官方说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。本轮在 WorkBuddy AI 国际桌面版 5.5.2 完成了导入和三场景调用。首次 1 项通过、2 项未通过，按明确复核意见修订后通过。请逐句核对正文的事实、开头判断、演示标签与编辑备注，不把模型自己的核查表当作验收。国内网页版仍未实测。

若无法导入，可把 SKILL.md 与正文直接交给对话，但必须记录为手动指令模式。保存完整输入输出、产品/版本、时间和评审结果。无需向维护者提供密码；也无需为验证自行购买套餐。

## 最短真实素材输入

“请用 bbq-content-repurposing 将以下正文改成一篇面向独立顾问的中文短文，行动是让读者选一个客户问题。正文：复用专业文章时，先选一条能回答客户问题的观点，保留证据、适用条件和出处，按读者场景重写。本文没有测量传播或收入效果。请附事实与链接检查记录。”

## 失败边界

只有标题、打不开的链接：补正文或笔记；可给建议提纲，但不能当原文改写。第三方结果不得变成本人业绩；演示、计划与未知不能变成实绩。未检查链接就标未核查。脚本测试/三次生成不证明提效、获客或排名。这里只准备草稿，发布和账号操作按用户另行明确的任务执行。
