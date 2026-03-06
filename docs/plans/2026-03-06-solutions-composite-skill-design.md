# Solutions Composite Skill Design

**Date:** 2026-03-06

**Status:** Approved

## Goal

Define a repository-standard pattern for "solutions" skills: end-to-end, task-oriented skills that combine multiple lower-level skills into an opinionated workflow for real user outcomes.

The first target profile is a content and marketing workflow based on article illustration. It should preserve the core user-facing capabilities of `baoyu-article-illustrator` while adding Alibaba Cloud-native recommended execution backends and fitting this repository's governance model, output conventions, and smoke-test structure.

## Problem

Most existing skills in this repository are product-scoped and API-scoped. They are useful building blocks, but they do not yet provide a strong out-of-the-box workflow for concrete user tasks such as:

- analyze an article
- decide where images should go
- generate illustrations
- revise weak images
- write a final Markdown article with images inserted

The repository needs a standard way to express these higher-level workflows without weakening existing governance around validation, evidence, and test coverage.

## Decision Summary

- Introduce a new top-level domain for composite workflows: `skills/solutions/`
- Use the skill naming prefix `alicloud-solution-...`
- Keep the repository's existing `SKILL.md` minimum structure, but extend it with workflow-state requirements suitable for multi-step orchestration
- Preserve the original article-illustrator interaction model as the product baseline: pre-check, preference loading, Type x Style selection, outline generation, saved prompts, and final insertion workflow
- Add Alibaba Cloud capabilities as recommended backend adapters, not as replacements for the original workflow model
- Define a standard supporting layout for `references/`, `templates/`, `scripts/`, `prompts/`, and config references
- Define a matching smoke-test pattern under `tests/solutions/`
- Start with a content and marketing profile derived from the article-illustration workflow pattern

## Scope

### In Scope

- Standards for solution-style skills under `skills/solutions/`
- Required folder structure and file responsibilities
- `SKILL.md` section requirements for solution skills
- Compatibility principles for retaining an external reference skill's core behavior
- Output and evidence conventions
- Smoke-test conventions
- A first profile for article-to-illustrated-Markdown workflows
- A first recommended Alibaba Cloud backend adapter pair for generation and repair

### Out Of Scope

- Migrating all existing product skills
- Building a general execution engine
- Reproducing every style reference file from the external skill on day one
- Adding all downstream dependencies in the first iteration

## Naming And Placement

### Domain

All composite, end-to-end, user-outcome-oriented skills live under:

```text
skills/solutions/
```

### Skill Name Prefix

All such skills use:

```text
alicloud-solution-...
```

### Example

```text
skills/solutions/alicloud-solution-content-article-illustrator/
tests/solutions/alicloud-solution-content-article-illustrator-test/
```

This separates solution workflows from product-scoped skills and keeps README grouping, coverage reporting, and future governance rules clean.

## Standard Directory Layout

Each solution skill should follow this structure:

```text
skills/solutions/<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── prompts/
│   └── system.md
├── references/
│   ├── sources.md
│   ├── workflow.md
│   ├── usage.md
│   ├── styles.md
│   ├── prompt-construction.md
│   ├── output-spec.md
│   └── test-plan.md
│   └── config/
│       ├── first-time-setup.md
│       └── preferences-schema.md
├── templates/
│   ├── outline.md
│   ├── prompt.md
│   └── delivery-report.md
└── scripts/
    ├── validate_inputs.py
    ├── build_outline.py
    └── collect_evidence.py
```

### File Responsibilities

- `SKILL.md`: the compact operational contract. It must stay short and execution-oriented.
- `prompts/system.md`: reusable orchestration prompt guidance when the workflow needs stronger consistency.
- `references/workflow.md`: detailed step-by-step guidance for the full task flow.
- `references/usage.md`: invocation patterns and concrete usage examples.
- `references/styles.md`: the supported style system and Type x Style compatibility.
- `references/prompt-construction.md`: prompt-building rules and constraints.
- `references/output-spec.md`: artifact paths, naming rules, and required evidence.
- `references/test-plan.md`: test expectations and pass criteria for the solution workflow.
- `references/config/*`: preference loading and first-time setup guidance.
- `templates/`: reusable skeletons for generated artifacts.
- `scripts/`: only for mechanical support work such as validation, outline generation, and evidence collection.

Core orchestration logic should remain visible in the skill docs, not hidden inside scripts. Solution skills may use helper scripts, but the workflow must remain inspectable in Markdown.

## Required SKILL.md Structure

Solution skills should retain the repository minimum sections and extend them with workflow-state guidance:

```markdown
---
name: alicloud-solution-content-article-illustrator
description: Use when the user needs an end-to-end Alibaba Cloud content workflow, such as analyzing an article, planning visuals, generating illustrations, revising weak images, and producing a Markdown article with inserted image references.
---

# Content Article Illustrator

## Validation
- one minimal executable validation command
- validation evidence written under `output/<skill-name>/`

## Output And Evidence
- artifact root path
- required evidence files

## Workflow
1. Intake
2. Analyze
3. Confirm Settings
4. Build Plan
5. Generate Assets
6. Review And Repair
7. Finalize Delivery

## State Gates
- drafted
- confirmed
- generated
- validated
- delivered

## References
- local references
- official sources
```

## Workflow State Model

The first standard state machine for solution skills is:

1. `drafted`
The source input is loaded and the initial outline exists.

2. `confirmed`
Required user-facing settings are confirmed in one batch.

3. `generated`
Prompts are saved and first-pass assets have been generated.

4. `validated`
Artifacts, naming, and structural expectations pass validation.

5. `delivered`
Final result files and evidence files are written.

This model is intentionally simple so it can later extend to other solution types such as troubleshooting or DevOps workflows.

## Compatibility Principle

The first solution skill should not merely imitate the outcome of `baoyu-article-illustrator`. It should preserve the major workflow affordances users rely on there:

- preference loading through a project-level or user-level `EXTEND.md` pattern
- Type x Style as separate concepts
- one-batch settings confirmation
- explicit outline generation before image generation
- prompt files saved before image generation
- structured prompt templates
- deterministic output organization for later edits

Alibaba Cloud support should be introduced underneath this experience as recommended execution backends and repository-governed validation.

## First Profile: Content Article Illustrator

The first concrete profile should be:

```text
alicloud-solution-content-article-illustrator
```

### Recommended Alibaba Cloud Backends In V1

- `alicloud-ai-image-qwen-image`
- `alicloud-ai-image-qwen-image-edit`

### Added Alibaba Cloud Capabilities In V1

- recommended text-to-image backend via Qwen Image
- recommended one-pass image repair backend via Qwen Image Edit
- repository-standard validation and evidence outputs

### Backend Binding Policy

The solution skill should not hard-bind to one generation provider. Instead:

- the workflow layer remains stable
- the backend contract is explicit
- Alibaba Cloud backends are the default recommendation in this repository
- other backends are allowed if they satisfy the same input and output contract

### Excluded From V1

- content generation
- moderation
- translation
- OSS upload

This keeps the first iteration focused on compatibility plus Alibaba Cloud image execution instead of expanding the dependency graph too early.

## Content Workflow Contract

The article-illustration profile should implement this flow:

1. Pre-check project and user preferences through `EXTEND.md`
2. Analyze article structure and candidate illustration positions
3. Confirm settings including Type, Density, Style, and optional Language
4. Generate `outline.md`
5. Generate and save prompt files before image generation
6. Use the selected image-generation backend for first-pass images
7. Optionally use the selected image-edit backend for one repair pass
8. Produce a new Markdown file with relative image links inserted
9. Produce delivery summary and evidence

### Key Rules

- Prompt files must be saved before any image generation step.
- Type and Style must remain separate dimensions in the workflow and documentation.
- Preferences loaded from `EXTEND.md` must influence defaults when present.
- The workflow may recommend specific backends, but must not require a single provider-specific skill name to be the only valid execution path.
- The source article must not be overwritten.
- The final Markdown output must be a new file named `article.with-images.md`.
- Inserted image references must use relative paths under `images/`.
- Each image entry must be tracked in `outline.md`, including whether edit mode was used.
- Automatic repair should be limited to one pass per image before escalation.

## Backend Contract

Solution skills should define a backend contract for generation and edit steps.

### Generation Backend

Expected inputs:

- saved prompt file content
- optional reference images
- requested size or aspect
- optional style hint

Expected outputs:

- image file path or retrievable image URL
- basic metadata sufficient for evidence

### Edit Backend

Expected inputs:

- source image
- saved edit prompt or structured edit instruction
- optional mask or local-edit parameters

Expected outputs:

- edited image file path or retrievable image URL
- basic metadata sufficient for evidence

The first repository implementation should recommend Alibaba Cloud backends, but the contract must remain provider-agnostic.

## Output And Evidence Standard

The first profile should write outputs here:

```text
output/alicloud-solution-content-article-illustrator/<topic-slug>/
└── source.md
└── article.with-images.md
└── outline.md
└── prompts/
└── images/
└── edits/
└── delivery-report.md
```

### Required Artifacts

- `source.md`
- `outline.md`
- at least one prompt file under `prompts/`
- generated image files under `images/`
- `article.with-images.md`
- `delivery-report.md`
- preference summary if `EXTEND.md` is loaded

### Required Evidence

- validation command output
- generated artifact listing
- image-to-outline mapping
- any edit history used during repair

## Markdown Insertion Rule

The first profile uses relative Markdown image references only:

```md
![alt text](images/01-cover.png)
```

No OSS URL placeholder is required in V1.

## Smoke-Test Standard

Each solution skill should have a matching test skill:

```text
tests/solutions/<skill-name>-test/
```

For the first article-illustration profile, the smoke test should verify:

- `SKILL.md` frontmatter is valid
- any helper scripts compile or run
- preference loading and fallback behavior are documented
- Type and Style remain distinct configuration axes
- a minimal outline can be generated
- prompt files exist before image generation
- `article.with-images.md` is produced
- inserted Markdown references use relative `images/...` paths
- evidence files are written to `output/<skill-name>-test/`

## Governance Compatibility

This design aligns with current repository rules:

- keeps `SKILL.md` frontmatter minimal
- preserves the required `Validation`, `Output And Evidence`, `Workflow`, and `References` sections
- writes artifacts under `output/`
- fits the mirrored `tests/**` smoke-test model
- can later integrate with coverage checks and README index generation without mixing with product domains

## Rollout Recommendation

1. Upgrade the first solution skill to preserve the original article-illustrator workflow model
2. Add the mirrored smoke test under `tests/solutions/`
3. Refresh README index generation if new sections are required
4. Reuse the same standard for future solution profiles only after the first one passes validation

## Open Decisions Deferred

The following decisions are intentionally deferred until after the first solution skill ships:

- whether solution skills need their own guard scripts
- whether `templates/` should be mandatory or optional
- whether future solution skills should permit more than one repair pass
- whether content workflows should later add moderation and upload phases
