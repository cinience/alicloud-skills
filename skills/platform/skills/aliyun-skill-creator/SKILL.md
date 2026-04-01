---
name: aliyun-skill-creator
description: Use when creating, migrating, or optimizing skills for this alicloud-skills repository. Use whenever users ask to add a new skill, import an external skill, refactor skill structure, improve trigger descriptions, add smoke tests under tests/**, or benchmark skill quality before merge.
version: 1.0.0
---

Category: tool

# Alibaba Cloud Skill Creator

Repository-specific skill engineering workflow for `alicloud-skills`.

## Use this skill when

- Creating a new skill under `skills/**`.
- Importing an external skill and adapting it to this repository.
- Updating skill trigger quality (`name` and `description` in frontmatter).
- Adding or fixing smoke tests under `tests/**`.
- Running structured benchmark loops before merge.

## Do not use this skill when

- The user only needs to execute an existing product skill.
- The task is purely application code under `apps/` with no skill changes.

## Repository constraints (must enforce)

- Skills live under `skills/<domain>/<subdomain>/<skill-name>/`.
- Skill folder names use kebab-case and should start with `alicloud-`.
- Every skill must include `SKILL.md` frontmatter with `name` and `description`.
- `skills/**/SKILL.md` content must stay English-only.
- Smoke tests must be in `tests/<domain>/<subdomain>/<skill-name>-test/SKILL.md`.
- Generated evidence goes to `output/<skill-or-test-skill>/` only.
- If skill inventory changes, refresh README index with `scripts/update_skill_index.sh`.

## Standard deliverable layout

```text
skills/<domain>/<subdomain>/<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   └── sources.md
└── scripts/ (optional)

tests/<domain>/<subdomain>/<skill-name>-test/
└── SKILL.md
```

## Workflow

1) Capture intent

- Confirm domain/subdomain and target skill name.
- Confirm whether this is new creation, migration, or refactor.
- Confirm expected outputs and success criteria.

2) Implement skill changes

- For new skills: scaffold structure and draft `SKILL.md` + `agents/openai.yaml`.
- For migration from external repo: copy full source tree first, then adapt.
- Keep adaptation minimal but explicit:
  - Replace environment-specific instructions that do not match this repo.
  - Add repository validation and output discipline sections.
  - Keep reusable bundled resources (`scripts/`, `references/`, `assets/`).

3) Add smoke test

- Create or update `tests/**/<skill-name>-test/SKILL.md`.
- Keep it minimal, reproducible, and low-risk.
- Include exact pass criteria and evidence location.

4) Validate locally

Run script compile validation for the skill:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/<domain>/<subdomain>/<skill-name> \
  --output output/<skill-name>-test/compile-check.json
```

Refresh skill index when inventory changed:

```bash
scripts/update_skill_index.sh
```

Confirm index presence:

```bash
rg -n "<skill-name>" README.md README.zh-CN.md README.zh-TW.md
```

Optional broader checks:

```bash
make test
make build-cli
```

5) Benchmark loop (optional, for major skills)

If the user asks for quantitative skill evaluation, reuse bundled tooling:

- `scripts/run_eval.py`
- `scripts/aggregate_benchmark.py`
- `eval-viewer/generate_review.py`

Prefer placing benchmark artifacts in a sibling workspace directory and keep per-iteration outputs.

## Definition of done

- Skill path and naming follow repository conventions.
- Frontmatter is complete and trigger description is explicit.
- Test skill exists and has objective pass criteria.
- Validation artifacts are saved under `output/`.
- README skill index is refreshed if inventory changed.

## References

- `references/schemas.md`
- `references/sources.md`
