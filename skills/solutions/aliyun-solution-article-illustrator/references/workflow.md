# Workflow

## 1. Pre-check

- If the user provides reference images, save them under `references/` before using them in prompts.
- Only treat a reference as file-backed if it is actually saved on disk.
- Look for project-level `EXTEND.md` at `.alicloud-skills/aliyun-solution-article-illustrator/EXTEND.md`.
- Look for user-level `EXTEND.md` at `$HOME/.alicloud-skills/aliyun-solution-article-illustrator/EXTEND.md`.
- Load and summarize preferences if present.
- Use `scripts/load_preferences.py` when you need a reproducible preference summary artifact.
- If no preference file exists, continue with explicit confirmation and reference `config/first-time-setup.md`.
- Choose a topic slug for the output directory.

## 2. Analyze

- Identify article sections, key claims, and paragraphs that benefit from visual support.
- Prefer images that clarify structure, concepts, comparisons, or narrative transitions.
- Record each candidate insertion point in `outline.md`.
- If references exist, classify them as `direct`, `style`, or `palette` usage.

## 3. Confirm Settings

Confirm these settings in one batch:

- illustration type
- density
- style
- optional language
- output size
- generation backend
- edit backend
- reference usage mode when reference images are available

## 4. Build Plan

- Create `outline.md` from the template.
- Create one prompt file per image under `prompts/`.
- Prompt files must be saved before any image generation step.
- Recommend Alibaba Cloud backends by default, but allow replacement if the backend contract is satisfied.
- If a saved reference image exists, record whether it is used as `direct`, `style`, or `palette`.

## 5. Generate Assets

- Generate first-pass images with the selected backend.
- Save images under `images/` using ordered filenames.
- Pass reference images only when the selected backend supports them and the files are actually saved.

## 6. Review And Repair

- Review each image against its outline entry.
- If needed, run one repair pass with the selected edit backend.
- Save repair intent and output under `edits/`.

## Reference Usage Modes

- `direct`: use the saved reference image as a strong visual reference when the target output is closely aligned.
- `style`: extract visual characteristics from the reference and describe them in prompt text.
- `palette`: extract colors only and express them in `COLORS`.

## 7. Finalize Delivery

- Write a new file named `article.with-images.md`.
- Insert relative Markdown image links such as `![alt text](images/01-cover.png)`.
- Do not overwrite `source.md`.
- Write `delivery-report.md` summarizing generated artifacts and any repair pass.
