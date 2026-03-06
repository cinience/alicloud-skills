# Output Specification

## Root Path

```text
output/alicloud-solution-content-article-illustrator/<topic-slug>/
```

## Required Files

```text
source.md
outline.md
article.with-images.md
delivery-report.md
workflow-run.json
artifacts.json
prompts/
images/
edits/
```

## Naming Rules

- Source article: `source.md`
- Final illustrated article: `article.with-images.md`
- Prompt files: `prompts/NN-<slug>.md`
- Image files: `images/NN-<slug>.png`
- Edit records: `edits/NN-<slug>.md`

## Markdown Rule

Use relative links only:

```md
![alt text](images/01-cover.png)
```

## Evidence Rules

- Keep artifact listings in the output root.
- Record which outline item produced each image.
- If an image was edited, record the reason and replacement path.
- If preferences were loaded, save a preference summary artifact for reproducibility.
