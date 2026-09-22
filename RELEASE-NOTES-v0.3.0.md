# v0.3.0 — traceable content repurposing (experimental)

从 BBQ 官网文章提炼一个可执行 Skill 更新：在用户请求时生成主张卡、渠道制作卡、草稿、来源映射和修订影响清单。普通草稿请求保持简洁。新增中英文指南、安装升级说明、三场景双端实测记录和固定版本下载。

Derived from the website article, this update adds an optional traceable content package and source-revision workflow. It includes bilingual guides, upgrade instructions and separate Codex/WorkBuddy observations.

- Codex CLI: three cases passed agent review using explicit Skill-file reads.
- WorkBuddy AI desktop 5.5.2 / Auto: all three valid cases exercised; only the insufficient-source boundary passed overall. Normal and corrected-source drafts still added unsupported reader assumptions. Source correction and fictional attribution worked in the third case. No revision retry was run.
- Experimental prerelease; human sign-off pending. Review every draft, including its opening. No growth or discovery guarantees.
- Only `bbq-content-repurposing` changes to v0.3.0; GEO and multilingual SEO remain v0.2.0, and are not repackaged as new versions.

[中文使用指南](guides/traceable-content-repurposing.zh-CN.md) · [English guide](guides/traceable-content-repurposing.md) · [完整实测记录 / full record](validation/content-repurposing/v0.3.0/REVIEW.md)

Release assets: the individual Skill ZIP, repository source ZIP and SHA256SUMS. GitHub-generated source archives are also available. The repository and website are intended to link to the fixed tag rather than a moving branch.
