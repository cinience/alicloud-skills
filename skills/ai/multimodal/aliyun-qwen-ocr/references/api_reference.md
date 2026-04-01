# Qwen OCR API Reference Notes

## Endpoint

- Domestic: `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- International: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`
- Global (Virginia): `https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions`

## Minimal request body

```json
{
  "model": "qwen-vl-ocr",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/invoice.png"
          },
          "max_pixels": 8388608
        },
        {
          "type": "text",
          "text": "Extract seller name, date, and total amount."
        }
      ]
    }
  ],
  "temperature": 0.01
}
```

## Built-in task example

```json
{
  "model": "qwen-vl-ocr-2025-11-20",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/table.png"
          }
        }
      ]
    }
  ],
  "ocr_options": {
    "task": "table_parsing"
  }
}
```

## Notes

- `qwen-vl-ocr-latest` and `qwen-vl-ocr-2025-11-20` use `32*32` pixels per image token.
- Older snapshots use `28*28` pixels per image token.
- For local files in HTTP/OpenAI-compatible workflows, prefer converting to a public URL or a Base64 data URL as documented by Alibaba Cloud.
