# Install and run

[简体中文](installation.zh-CN.md) · [Evidence and limits](../validation/content-repurposing/REVIEW.md)

## Codex

Get this repository using Git, or download the release source archive and extract it. With Git:

```sh
git clone --branch v0.2.0 --depth 1 https://github.com/nicobbqwang-wq/bbq-growth-playbook.git
cd bbq-growth-playbook
```

The shortest route needs no installation: ask Codex to read `skills/bbq-content-repurposing/SKILL.md` and adapt `examples/content-repurposing-input.md`. Request one English LinkedIn draft plus factual checks. This explicit-read mode is the tested mode.

For project discovery, copy the desired Skill directory to your project's `.agents/skills/`. Check that the destination does not already exist before copying. Start a new task and invoke `$bbq-content-repurposing`, supplying the article body, audience, channel, language and desired action. If it is absent, restart Codex or use the explicit path. Discovery is documented by [OpenAI](https://learn.chatgpt.com/docs/build-skills); automatic selection was not tested in this release.

Each Skill must be copied with its `scripts`, `references`, or `assets` children. GEO and SEO helpers require Python 3.9+; content repurposing has no script dependency. Run helpers from the repository as shown in their guides, or use paths relative to the installed Skill directory.

## WorkBuddy AI (review-assisted)

Sign in to the official WorkBuddy application. In Skills, choose Add Skill → Upload Skill and select the release ZIP for the individual Skill. Verify it appears among installed/enabled skills, then select it in a fresh conversation and supply the example. The [official guide](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) describes importing local packages. This import flow was completed in WorkBuddy AI international desktop 5.5.2. Three cases ran, but two first responses failed factual checks and needed explicit feedback. See the full evidence before treating output as publishable.

If import is unavailable, explicitly provide `SKILL.md` and the source in a conversation; label that result manual instruction mode, not installed-Skill compatibility. A login or unsupported runtime is a prerequisite, not permission to request a password or buy a subscription. Compare the actual draft against sources, including its hook and any fictional labels. Run all three [cases](../validation/content-repurposing/REVIEW.md) before reporting compatibility.

## Boundaries

- A title or inaccessible URL is insufficient source material. Supply body/notes; any outline remains a suggestion.
- Third-party results, hypothetical examples and future plans keep their original owner and status.
- Unchecked links remain unchecked. Fictional example.org links are fixtures, not evidence.
- Drafts do not authorize posting, sending messages, or account changes.
- No promise of faster work, revenue, rankings, or AI citations follows from these tests.
