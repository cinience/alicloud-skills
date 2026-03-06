# Content Article Illustrator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add the first `skills/solutions/` composite skill, `alicloud-solution-content-article-illustrator`, preserving the core workflow capabilities of `baoyu-article-illustrator` while recommending `alicloud-ai-image-qwen-image` and `alicloud-ai-image-qwen-image-edit` as default Alibaba Cloud execution backends rather than hard-binding to them.

**Architecture:** Create a new solution-skill directory with a compact `SKILL.md`, detailed references, reusable templates, configuration docs, and minimal helper scripts. Preserve the original workflow model including `EXTEND.md` preference loading, Type x Style settings, outline-first planning, and saved prompt files, then define provider-agnostic generation and repair backend contracts with Alibaba Cloud image skills as the default recommendation. Mirror it with a solution smoke test that validates compatibility features as well as repository artifact structure.

**Tech Stack:** Markdown documentation, Python helper scripts, repository smoke-test skills, existing guard scripts, README index generation.

---

### Task 1: Inspect Existing Downstream Image Skills

**Files:**
- Modify: `skills/ai/image/alicloud-ai-image-qwen-image/SKILL.md`
- Modify: `skills/ai/image/alicloud-ai-image-qwen-image-edit/SKILL.md`
- Reference: `docs/plans/2026-03-06-solutions-composite-skill-design.md`

**Step 1: Read the image skill contracts**

Run:

```bash
sed -n '1,240p' skills/ai/image/alicloud-ai-image-qwen-image/SKILL.md
sed -n '1,240p' skills/ai/image/alicloud-ai-image-qwen-image-edit/SKILL.md
```

Expected: enough detail to reference their workflows and prerequisites as the default recommended backend path in the new solution skill.

**Step 2: Record reusable invocation patterns**

Write down:

- expected inputs
- output expectations
- any prompt or file constraints
- the parts that should remain provider-agnostic in the solution skill contract

**Step 3: Do not change these skills unless a gap blocks the recommended backend path**

Expected: downstream skills remain stable unless there is a concrete compatibility problem.

### Task 2: Create the New Solution Skill Skeleton

**Files:**
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/SKILL.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/agents/openai.yaml`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/prompts/system.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/sources.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/workflow.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/usage.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/styles.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/prompt-construction.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/output-spec.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/test-plan.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/backend-contract.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/config/first-time-setup.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/references/config/preferences-schema.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/templates/outline.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/templates/prompt.md`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/templates/delivery-report.md`

**Step 1: Write the failing structure check**

Run:

```bash
test -f skills/solutions/alicloud-solution-content-article-illustrator/SKILL.md
```

Expected: FAIL before files exist.

**Step 2: Add the compatibility-oriented directory and file skeleton**

Implement the full directory layout from the approved design doc, including prompt and config references needed to retain the original workflow model.

**Step 3: Write a compact `SKILL.md`**

Include:

- valid frontmatter
- `Validation`
- `Output And Evidence`
- `Workflow`
- `References`

**Step 4: Add detailed references**

Move long-form instructions into `references/` to keep `SKILL.md` compact, but preserve original behavior concepts such as Type x Style, `EXTEND.md`, prompt structure, and backend-selection flexibility.

**Step 5: Re-run the structure check**

Run:

```bash
test -f skills/solutions/alicloud-solution-content-article-illustrator/SKILL.md
```

Expected: PASS.

### Task 3: Add Helper Scripts For Mechanical Work

**Files:**
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/scripts/validate_inputs.py`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/scripts/build_outline.py`
- Create: `skills/solutions/alicloud-solution-content-article-illustrator/scripts/collect_evidence.py`
- Test: `tests/common/compile_skill_scripts.py`

**Step 1: Write the failing compile check**

Run:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/solutions/alicloud-solution-content-article-illustrator \
  --output output/alicloud-solution-content-article-illustrator-test/compile-check.json
```

Expected: FAIL before scripts exist.

**Step 2: Implement minimal scripts**

Rules:

- keep logic mechanical
- no hidden workflow orchestration
- use ASCII only
- support preference loading and outline generation without bypassing saved-prompt discipline
- avoid baking provider-specific assumptions into helper scripts

**Step 3: Re-run compile check**

Run the same command again.

Expected: PASS with `compile-check.json.status=pass`.

### Task 4: Encode The Article Workflow Contract

**Files:**
- Modify: `skills/solutions/alicloud-solution-content-article-illustrator/SKILL.md`
- Modify: `skills/solutions/alicloud-solution-content-article-illustrator/references/workflow.md`
- Modify: `skills/solutions/alicloud-solution-content-article-illustrator/references/output-spec.md`
- Modify: `skills/solutions/alicloud-solution-content-article-illustrator/references/prompt-construction.md`

**Step 1: Write the failing contract checklist**

Create a manual checklist covering:

- `EXTEND.md` preference loading and fallback
- separate Type and Style settings
- backend recommendation vs backend requirement
- prompt files saved before generation
- single repair pass
- output article saved as `article.with-images.md`
- relative image links under `images/`

Expected: the checklist is incomplete before the docs are updated.

**Step 2: Update docs to satisfy the contract**

Document the full workflow:

1. pre-check and load preferences
2. analyze
3. confirm Type, Density, Style, and optional Language
4. choose or recommend a backend
5. build outline
6. save prompt files
7. generate images through the selected backend
8. optionally edit images once through the selected edit backend
8. write illustrated Markdown output
9. collect evidence

**Step 3: Verify the docs cover all checklist items**

Run:

```bash
rg -n "EXTEND.md|Type|Style|article.with-images.md|images/|prompt files|repair pass|outline" \
  skills/solutions/alicloud-solution-content-article-illustrator
```

Expected: every required contract item is discoverable, including non-binding backend language.

### Task 5: Add The Smoke-Test Skill

**Files:**
- Create: `tests/solutions/alicloud-solution-content-article-illustrator-test/SKILL.md`
- Create: `tests/solutions/alicloud-solution-content-article-illustrator-test/scripts/smoke_test_article_illustrator.py`

**Step 1: Write the failing test structure check**

Run:

```bash
test -f tests/solutions/alicloud-solution-content-article-illustrator-test/SKILL.md
```

Expected: FAIL before files exist.

**Step 2: Add the smoke-test skill**

The test should verify:

- frontmatter
- script compilation
- preference-loading guidance exists
- Type and Style are separate configuration axes
- backend recommendation is documented without hard-binding
- outline generation
- prompt-before-image discipline
- final `article.with-images.md`
- relative `images/...` Markdown links
- evidence under `output/alicloud-solution-content-article-illustrator-test/`

**Step 3: Add a minimal smoke-test helper**

The helper can simulate artifact generation without calling external image APIs. It should validate file ordering and final Markdown insertion format.

**Step 4: Re-run the structure check**

Run:

```bash
test -f tests/solutions/alicloud-solution-content-article-illustrator-test/SKILL.md
```

Expected: PASS.

### Task 6: Refresh Repository Indexes And Coverage Expectations

**Files:**
- Modify: `README.zh-CN.md`
- Modify: `README.zh-TW.md`
- Modify: any generated README/index sections updated by scripts

**Step 1: Run the index refresh command**

Run:

```bash
scripts/update_skill_index.sh
```

Expected: README sections include the new `solutions` entry if the generator supports it.

**Step 2: Inspect generated changes**

Run:

```bash
rg -n "alicloud-solution-content-article-illustrator|solutions" README.zh-CN.md README.zh-TW.md docs/INDEX.md
```

Expected: the new skill is discoverable in generated indexes or any missing generator support is obvious.

**Step 3: Adjust generator logic only if required**

If `solutions` is not recognized, add the smallest change necessary to existing scripts.

### Task 7: Validate The New Skill End-To-End

**Files:**
- Test: `skills/solutions/alicloud-solution-content-article-illustrator/**`
- Test: `tests/solutions/alicloud-solution-content-article-illustrator-test/**`

**Step 1: Run script compilation**

Run:

```bash
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/solutions/alicloud-solution-content-article-illustrator \
  --output output/alicloud-solution-content-article-illustrator-test/compile-check.json
```

Expected: PASS.

**Step 2: Run skill linting**

Run:

```bash
python3 scripts/lint_skills.py
```

Expected: PASS with no frontmatter or structure regressions.

**Step 3: Run governance guards**

Run:

```bash
python3 scripts/guards/check_frontmatter.py
python3 scripts/guards/check_skill_test_coverage.py --stage legacy
```

Expected: PASS, or a clearly identified coverage delta caused by the new skill without its test.

**Step 4: Save evidence**

Write outputs under:

```text
output/alicloud-solution-content-article-illustrator-test/
```

### Task 8: Commit In Small Units

**Files:**
- Commit: design-consistent solution skill files
- Commit: smoke-test files
- Commit: any index-generation changes

**Step 1: Commit the new solution skill**

```bash
git add skills/solutions/alicloud-solution-content-article-illustrator
git commit -m "feat: add content article illustrator solution skill"
```

**Step 2: Commit the smoke test**

```bash
git add tests/solutions/alicloud-solution-content-article-illustrator-test
git commit -m "test: add smoke test for content article illustrator solution skill"
```

**Step 3: Commit generated index updates if any**

```bash
git add README.zh-CN.md README.zh-TW.md docs/INDEX.md
git commit -m "docs: refresh skill index for solutions skills"
```

Only create commits that match actual changed files.
