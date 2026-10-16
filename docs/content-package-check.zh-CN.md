# 在编辑审阅前检查内容包

作者：BBQ / BBQ Growth Lab。[English](content-package-check.md)

这个离线工具适合把一份来源改编为多个草稿时使用：发现来源映射漏掉开头、来源快照已经变化，或撤回的主张仍出现在多个版本中。它核对你声明的结构，最终仍需编辑判断每段改写是否受来源支持。

## 运行完整演示

需要 Python 3.9 或更高版本，只用标准库。在仓库根目录运行：

```sh
python3 scripts/check_content_package.py examples/content-package/package.json
python3 scripts/check_content_package.py examples/content-package/missing-opening.json
python3 scripts/check_content_package.py examples/content-package/withdrawn-claim.json
python3 scripts/check_content_package.py examples/content-package/whitespace-quote.json
```

第一项退出码 0。另三项退出码 2：分别漏映射开头、两个稿件仍依赖撤回主张、引文只有空白。JSON 报告输出到 stdout，输入文件不会被修改。工具不联网、不调用模型，也不发布内容；报告含用户提供的 ID 和文件位置，公开前请审阅。

演示来自[内容地图原文](https://bbqgrowthlab.com/zh-cn/articles/content-repurposing-map-seo-llm-visibility/)的两段方法建议，改编为英文专业社交草稿和中文邮件草稿。两稿都没有实际发布或发送，没有效果数据或平台长度合规结论。[演示说明](../examples/content-package/README.md)记录任务、选择与逐段复核。

## 输入自己的材料

1. 在同一个目录放 UTF-8 原稿快照、完整草稿和 JSON。保留空白与换行；无关私有材料放在目录之外。
2. 给来源原始字节计算 SHA256。工具检查本地快照，不查询线上最新版本；原稿变化后要更新 hash 并重新审阅。
3. 每张主张卡有 ID、来源 ID、至少含一个非空白字符的精确引文和状态：`active`、`withdrawn` 或 `unresolved`。active 是声明的使用状态，不等于独立核验。
4. 按顺序映射整篇草稿，包括标题、开头、连接句、结尾行动与换行。全部 `segments.text` 拼接必须严格等于草稿文件。
5. `sourced` 段须有可用主张 ID。`editorial`、`synthetic`、`disclosure` 段须用 `review_note` 说明其建议、演示或披露用途，不能据此把事实免除审阅。
6. 运行检查，修复结构错误，再检查归属、含义、条件、授权、假设标识与渠道任务。

## 格式与输出

完整输入见 [package.json](../examples/content-package/package.json)。`schema_version` 为整数 1；sources、claims、drafts 及每稿 segments 均为非空列表，集合内 ID 唯一。来源须有 `id/path/sha256`；主张须有 `id/source_id/quote/status`；稿件须有 `id/path/segments`。段落必填 `text/kind`；sourced 段另填非空 `claim_ids`，其余段另填非空 `review_note`，不放主张 ID。

路径相对 JSON 目录，只能在这个目录内，绝对路径、目录逃逸、符号链接逃逸均被拒绝。UTF-8 不带 BOM；非法编码、JSON 重复键和字段类型错误均报错。0.1.1 起，只有空白的引文即使存在于原文也会被拒绝，在 quote 字段报告 EMPTY_STRING。判断使用 Python 字符串的空白定义，不检测所有无意义或视觉不可见的文本。有实际内容的引文不会被裁剪或改写，前后空白及换行仍需精确匹配。

不做空白或 Unicode 规范化，CRLF 与 LF 是不同文本。

退出码 0 表示 `structure_ready`，退出码 2 表示 `blocked`。报告给出错误代码和字段位置、稿件长度、段数及依赖主张，方便定位变更影响。

所有报告仍写 `semantic_review=NOT_PERFORMED`、`publication_ready=false`。精确引文存在不能证明改写含义成立，hash 相同不能证明来源正确，段落分类也可能填错。把整篇错误标成 editorial 仍可能通过，编辑必须审阅分类与含义。

已有 Skill 保持 v0.3.0 实验状态，本轮 Python 测试不算 Codex/WorkBuddy 重新运行或市场审核通过。实际环境与测试见[验证记录](../validation/content-package/0.1.1/README.md)。
