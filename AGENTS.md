# Repository Guidelines

## Project Structure & Module Organization
- `skills/` is the canonical source of skills, grouped by domain (for example `skills/ai/`, `skills/compute/`, `skills/security/`).
- Each skill usually contains `SKILL.md`, optional `scripts/`, optional `references/`, and `agents/openai.yaml`.
- `tests/` mirrors skill domains and stores smoke-test skill specs (mostly `tests/**/SKILL.md`).
- `apps/` contains application code:
  - `apps/cmd/alicloud-skills` (Go CLI entrypoint)
  - `apps/internal/agent` (shared Go runtime logic)
  - `apps/desktop` (Wails desktop backend)
  - `apps/web` (Next.js frontend)
  - `apps/go.mod`, `apps/go.sum` (Go module for all Go code under `apps/`)
- `scripts/` contains repository maintenance tools (index generation, product metadata merge, README section generation).
- `examples/` contains prompt patterns and scenario docs.
- `output/` is for generated artifacts only; do not commit files from this directory.

## Build, Test, and Development Commands
- Install skills locally:
  - `npx skills add cinience/alicloud-skills --all -y --force`
- Regenerate README skill index section:
  - `scripts/update_skill_index.sh`
  - Equivalent explicit form: `python3 scripts/generate_skill_index.py`
- Build/test apps from repo root:
  - `make test`
  - `make build-cli`
  - `make build-desktop`
  - `make run` (optional args: `make run RUN_ARGS='run --help'`)
- Direct Go commands:
  - `go -C apps test ./...`
  - `go -C apps build ./cmd/alicloud-skills`
- Run a utility script directly when iterating:
  - `python3 scripts/analyze_products_vs_skills.py`

## Coding Style & Naming Conventions
- Python: 4-space indentation, type hints where practical, small focused functions (follow existing `scripts/*.py` patterns).
- JavaScript examples use CommonJS in this repo (see `skills/**/scripts/*.js`).
- Skill folders use kebab-case, prefixed by product scope (example: `aliyun-modelstudio-qwen-image`).
- Keep frontmatter in every `SKILL.md` with at least `name` and `description`.
- Language policy: keep `skills/**/SKILL.md` content in English only. If multilingual support is needed, place localized content in `README.zh-CN.md` / `README.zh-TW.md` instead of skill source files.

## Testing Guidelines
- This repository uses smoke-test skills instead of a single `pytest` suite.
- Add/update tests under `tests/<domain>/<skill>-test/SKILL.md`.
- Keep tests minimal and reproducible: one read-only or low-risk API path, clear pass/fail criteria, and saved evidence under `output/<test-skill>/`.
- When relevant, include exact prerequisites (env vars, region, SDK install command).

## Commit & Pull Request Guidelines
- Follow Conventional Commit style seen in history: `feat: ...`, `chore: ...`, `refactor(scope): ...`, `docs: ...`.
- Keep commits scoped to one concern (skill content, scripts, or docs/index regeneration).
- PRs should include:
  - What changed and why.
  - Affected paths (for example `skills/ai/...`, `apps/...`, `scripts/...`, `README*.md`).
  - Validation evidence (commands run, output location, screenshots/log snippets if useful).
  - Confirmation that generated README sections were refreshed when skill inventory changed.
