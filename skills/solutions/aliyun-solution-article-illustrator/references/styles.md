# Styles

Type and Style are separate axes.

## Types

- `infographic`
- `scene`
- `flowchart`
- `comparison`
- `framework`
- `timeline`

## Styles

- `notion`
- `warm`
- `minimal`
- `blueprint`
- `watercolor`
- `editorial`

Detailed notes:

- `references/styles/notion.md`
- `references/styles/warm.md`
- `references/styles/minimal.md`
- `references/styles/blueprint.md`
- `references/styles/watercolor.md`
- `references/styles/editorial.md`

## Type x Style Compatibility Matrix

| Type | notion | warm | minimal | blueprint | watercolor | editorial |
|------|:------:|:----:|:-------:|:---------:|:----------:|:---------:|
| infographic | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓✓ |
| scene | ✓ | ✓✓ | ✓ | ✗ | ✓✓ | ✓ |
| flowchart | ✓✓ | ✓ | ✓ | ✓✓ | ✗ | ✓ |
| comparison | ✓✓ | ✓ | ✓✓ | ✓ | ✓ | ✓✓ |
| framework | ✓✓ | ✓ | ✓✓ | ✓✓ | ✗ | ✓ |
| timeline | ✓✓ | ✓ | ✓ | ✓ | ✓✓ | ✓✓ |

`✓✓` = highly recommended, `✓` = compatible, `✗` = not recommended

## Auto Selection By Type

| Type | Primary Style | Secondary Styles |
|------|---------------|------------------|
| infographic | `blueprint` | `notion`, `editorial` |
| scene | `warm` | `watercolor`, `notion` |
| flowchart | `blueprint` | `notion`, `editorial` |
| comparison | `notion` | `editorial`, `minimal` |
| framework | `blueprint` | `notion`, `minimal` |
| timeline | `editorial` | `warm`, `watercolor` |

## Auto Selection By Content Signals

| Content Signals | Recommended Type | Recommended Styles |
|-----------------|------------------|--------------------|
| API, metrics, data, comparison | `infographic` | `blueprint`, `editorial` |
| tutorial, workflow, how-to, steps | `flowchart` | `notion`, `blueprint` |
| framework, architecture, principles | `framework` | `blueprint`, `minimal` |
| story, reflection, journey | `scene` | `warm`, `watercolor` |
| history, evolution, roadmap | `timeline` | `editorial`, `warm` |
| pros/cons, before/after, alternatives | `comparison` | `notion`, `editorial` |

## Combination Notes

### `infographic` + `blueprint`

- Best for technical and architectural articles.
- Prefer grid layouts, schematic lines, and high information density.

### `scene` + `warm`

- Best for narrative and reflective content.
- Prefer soft gradients, inviting tone, and emotional clarity.

### `flowchart` + `notion`

- Best for approachable tutorials and SaaS/productivity explainers.
- Prefer simple step containers and minimal decoration.

### `comparison` + `editorial`

- Best for balanced side-by-side analysis.
- Prefer clear separators, strong headings, and concise labels.

### `framework` + `minimal`

- Best for conceptual models where clarity matters more than ornament.
- Prefer clean nodes, whitespace, and restrained color usage.

### `timeline` + `watercolor`

- Best for human, historical, or growth-oriented sequences.
- Prefer flowing progression and softer transitions.

The style list is intentionally smaller than the external reference skill in the first repository version. Additional style reference files can be added without changing the workflow contract.
