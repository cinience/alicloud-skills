# Test Plan

The smoke test for this skill should verify:

- required frontmatter exists
- helper scripts compile
- `load_preferences.py` resolves project-first fallback correctly
- preference summary captures watermark, output-dir, and custom-style metadata when present
- preference-loading guidance exists
- Type and Style are distinct concepts in the docs
- styles docs include a Type x Style compatibility matrix and auto-selection guidance
- backend recommendation is documented without hard-binding
- a minimal outline can be generated
- prompt docs require structured sections such as `ZONES`, `LABELS`, `COLORS`, and `ASPECT`
- workflow and prompt docs explain `direct`, `style`, and `palette` reference usage
- prompt files exist before images
- `article.with-images.md` is generated
- inserted image links use `images/...` relative paths
- evidence is written under `output/aliyun-solution-article-illustrator-test/`
