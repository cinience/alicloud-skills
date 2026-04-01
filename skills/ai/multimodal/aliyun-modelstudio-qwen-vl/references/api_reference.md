# Qwen VL API Reference Notes

## Endpoint (compatible mode)

- Domestic: `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- International: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

## Minimal request body

```json
{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/sample.jpg",
            "detail": "auto"
          }
        },
        {
          "type": "text",
          "text": "Describe the image and extract key entities."
        }
      ]
    }
  ],
  "max_tokens": 512,
  "temperature": 0.2
}
```

## Response extraction

- `choices[0].message.content` is the primary answer.
- `usage` contains token statistics when provided.
- `model` may return canonical model ID even if alias is used.

## Structured output options

- JSON mode:

```json
{
  "response_format": {
    "type": "json_object"
  }
}
```

- JSON Schema mode:

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "image_understanding_result",
      "schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "amount": {"type": "number"}
        },
        "required": ["title"]
      }
    }
  }
}
```

## Notes

- For deterministic extraction tasks, lower `temperature` (for example `0` to `0.2`).
- For production reproducibility, prefer pinned snapshot model IDs.
