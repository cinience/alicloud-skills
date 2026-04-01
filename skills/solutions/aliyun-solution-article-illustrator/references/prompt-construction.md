# Prompt Construction

## Rules

- Save prompt files before any image generation step.
- Each prompt must map back to one `outline.md` entry.
- Use article-specific terms, concepts, and labels instead of generic filler.
- Keep prompts explicit about what to show and what to avoid.
- Keep Type and Style as separate fields so the workflow can combine them consistently.
- Use structured sections so prompts remain inspectable and reusable across backends.

## Required Prompt Structure

Each prompt file should use a short header plus structured body sections:

```text
Title:
Target Section:
Type:
Style:
Visual Goal:
References:
Layout:
ZONES:
LABELS:
COLORS:
STYLE NOTES:
ASPECT:
Prompt:
Negative Prompt:
```

## Section Requirements

- `Title`: short human-readable title.
- `Target Section`: where the image will be inserted.
- `Type`: one workflow type such as `infographic` or `flowchart`.
- `Style`: one selected style such as `notion` or `blueprint`.
- `Visual Goal`: why this image exists.
- `References`: optional saved reference images or extracted notes.
- `Layout`: overall composition such as `grid`, `top-down`, or `split view`.
- `ZONES`: named visual regions with concrete content.
- `LABELS`: article-specific terms, numbers, metrics, or short quotes.
- `COLORS`: semantic colors or palette hints.
- `STYLE NOTES`: line treatment, rendering guidance, texture, mood.
- `ASPECT`: ratio or size target.
- `Prompt`: final generation prompt body.
- `Negative Prompt`: exclusions or quality guardrails.

## Reference Usage Rules

- Only include file-backed references if the files actually exist.
- Use `direct` when the reference should materially shape the output composition.
- Use `style` when only the aesthetic language should carry over.
- Use `palette` when only colors should carry over.
- If no file is saved, describe extracted characteristics in prompt text instead of pretending there is a file-backed reference.

## Type-Specific Guidance

### Infographic

- Prefer `Layout`, `ZONES`, and `LABELS` with concrete data.
- Use `COLORS` semantically, not decoratively.

### Scene

- Emphasize atmosphere, focal point, and emotional intent in `STYLE NOTES`.

### Flowchart

- Use `Layout` for directionality and `ZONES` for ordered steps.

### Comparison

- Split `ZONES` clearly between the two sides.

### Framework

- Use `ZONES` and `LABELS` to show conceptual relationships.

### Timeline

- Keep chronological order explicit in `ZONES` and `LABELS`.

## Prompt Quality Requirements

- `ZONES` must not be vague; each zone should describe specific visual content.
- `LABELS` should use real article language whenever possible.
- `COLORS` should reflect meaning, brand, or category.
- `STYLE NOTES` should reinforce the selected style without overwriting Type.
- `Prompt` should summarize the structured sections, not replace them.
- `References` should clearly state `direct`, `style`, or `palette` usage when a reference is present.

## Repair Prompt Rules

- Repair prompts must describe what changes and what stays fixed.
- Limit automated repair to one pass per image.
- Save repair prompts under `edits/` or reference them from the edit record.
- Repair prompts should restate the original `Type`, `Style`, and preserved elements.
