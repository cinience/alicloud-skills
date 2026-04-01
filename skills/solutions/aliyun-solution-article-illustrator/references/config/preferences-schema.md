# Preferences Schema

Supported preference fields:

```yaml
---
version: 1

watermark:
  enabled: false
  content: ""
  position: bottom-right
  opacity: 0.7

preferred_style:
  name: null
  description: ""

language: null
default_type: null
default_density: null
default_output_dir: null

custom_styles: []
---
```

## Field Reference

- `version`: schema version.
- `watermark.enabled`: whether watermarking should be enabled by default.
- `watermark.content`: watermark text or handle.
- `watermark.position`: default placement such as `bottom-right`.
- `watermark.opacity`: opacity hint for downstream generation or post-processing.
- `preferred_style.name`: preferred built-in or custom style name.
- `preferred_style.description`: notes or override guidance for the preferred style.
- `language`: preferred image-text language.
- `default_type`: preferred illustration type.
- `default_density`: preferred image density.
- `default_output_dir`: preferred output location policy.
- `custom_styles`: optional list of custom style definitions.

## Output Directory Options

- `same-dir`
- `imgs-subdir`
- `illustrations-subdir`
- `independent`

## Custom Style Shape

Each custom style may include:

```yaml
- name: my-style
  description: "Short description"
```

The current repository implementation records custom style names in the preference summary. Deeper style attributes can be added later without changing the loader contract.

Preferences are optional. If absent, the workflow must still proceed with explicit confirmation.
