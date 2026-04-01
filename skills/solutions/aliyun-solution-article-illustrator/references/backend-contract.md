# Backend Contract

This solution skill recommends Alibaba Cloud backends by default, but does not hard-bind to them.

## Recommended Defaults

- Generation backend: `aliyun-modelstudio-qwen-image`
- Edit backend: `aliyun-modelstudio-qwen-image-edit`

## Generation Backend Requirements

Inputs:

- saved prompt file content
- optional reference images
- requested size or aspect
- optional style hint

Outputs:

- image file path or retrievable image URL
- metadata that can be saved as evidence

## Edit Backend Requirements

Inputs:

- source image
- edit instruction or saved edit prompt
- optional mask or local-edit parameters

Outputs:

- edited image file path or retrievable image URL
- metadata that can be saved as evidence
