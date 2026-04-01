# Usage

Use this skill when the user asks to:

- illustrate an article
- add images to a Markdown article
- generate article visuals with consistent Type and Style
- produce an illustrated Markdown deliverable

Typical flow:

1. load preferences from `EXTEND.md` if present
2. confirm Type, Density, Style, and optional Language
3. choose or accept a recommended backend
4. create `outline.md`
5. save prompt files under `prompts/`
6. generate images through the selected backend
7. optionally repair weak images once through the selected edit backend
8. write `article.with-images.md`

Executable example:

```bash
python3 skills/solutions/aliyun-solution-article-illustrator/scripts/run_workflow.py \
  --source path/to/article.md \
  --output-dir output/aliyun-solution-article-illustrator/example-run \
  --generation-backend mock
```
