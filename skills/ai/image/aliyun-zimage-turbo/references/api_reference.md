# Z-Image Turbo API Reference (DashScope)

Keep this reference minimal and update only when the API behavior changes.

## Endpoints

- Beijing: `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- Singapore: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

## Request (basic)

```json
{
  "model": "z-image-turbo",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {"text": "A calm lake at dawn, a lone angler casting a line"}
        ]
      }
    ]
  },
  "parameters": {
    "size": "1024*1024",
    "prompt_extend": false,
    "seed": 1234
  }
}
```

## Response (shape)

```json
{
  "request_id": "...",
  "output": {
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": [
            {"image": "https://..."},
            {"text": "rewritten prompt (optional)"},
            {"reasoning_content": "reasoning (optional)"}
          ]
        }
      }
    ]
  },
  "usage": {
    "width": 1024,
    "height": 1024
  }
}
```

## Parameters

- `size` (string): width*height; total pixels between `512*512` and `2048*2048`.
- `seed` (int): optional seed for reproducibility.
- `prompt_extend` (bool): rewrite prompt; costs more than `false`.

## Notes

- Response returns a single image URL in `output.choices[0].message.content`.
- Image URL is time-limited; download promptly.
