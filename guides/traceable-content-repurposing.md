# Repurpose an article with traceable claim cards

[简体中文](traceable-content-repurposing.zh-CN.md) · By [BBQ](https://bbqgrowthlab.com/en/about/) · Resource v0.3.0

For consultants and editors adapting an existing article or evidence-backed brief. Supply the source body, reader, channel and desired reader action. Request a traceable package to receive claim cards, one channel production card, a draft and a separate editorial source map. A title alone is insufficient.

The method comes from BBQ's [content repurposing article](https://bbqgrowthlab.com/en/articles/content-repurposing-map-seo-llm-visibility/), particularly its claim cards, channel production cards and change-impact workflow. The article explains the method; this resource applies it to your material.

## Workflow

1. Name the source and its supplied revision/date. Preserve paragraph or record references, attribution and uncertainty.
2. Give material claims stable IDs. Record support, scope and limits; appearing in a source does not establish independent verification.
3. Define one reader task and action per requested channel. Select claims and essential qualifications; leave missing owners, dates and platform limits unspecified.
4. Draft, then map meaningful passages to claim IDs separately. Essential qualifications and hypothetical labels must remain in the publishable draft.

## Try it

Read `skills/bbq-content-repurposing/SKILL.md` and request:

```text
Create a traceable package: claim cards, one channel production card,
one English LinkedIn draft and a separate editorial source map.
Reader: independent consultants. Action: select one old article and mark a claim, source and limit.
Source S1, revision 2026-09-22:
Paragraph 1: When reusing a professional article, choose one idea that answers a reader question,
retain evidence, attribution and scope, then rewrite for the channel.
Paragraph 2: We suggest separately recording each material draft claim's source paragraph,
so later revisions can identify affected versions. This is a proposed workflow;
time savings, traffic and inquiries have not been measured.
Do not browse or publish. Produce only the requested channel version.
```

This English prompt is an illustrative translation. The actual recorded v0.3.0 cases use Chinese requests: [input](../validation/content-repurposing/v0.3.0/normal.input.md), [Codex output](../validation/content-repurposing/v0.3.0/normal.codex.output.md). They are method fixtures, not customer or business results.

## Install, update and review

[Installation](../docs/installation.md) · [中文安装](../docs/installation.zh-CN.md) · [Card template](../skills/bbq-content-repurposing/assets/traceable-package.md) · [Download v0.3.0](https://github.com/nicobbqwang-wq/bbq-growth-playbook/releases/tag/v0.3.0)

Codex and WorkBuddy use the same core Skill. Draft-only requests stay concise. When a source changes, supply its old IDs and corrected version, and request an impact list; this does not automatically update published channels.

Compare the actual draft with its source: attribution, numbers, fictional labels, qualifications and requested scope must survive. See [recorded behavior and limits](../validation/content-repurposing/v0.3.0/REVIEW.md). Small tests do not guarantee general reliability; review every draft. No automatic publishing, traffic or AI-citation promises.
