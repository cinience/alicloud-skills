# VOD Task Templates

Use these templates after confirming region/media scope and auth method.

## 1) Create upload credential for video

- API: `CreateUploadVideo`
- Required params template:
  - `Title`: `<video-title>`
  - `FileName`: `<video.mp4>`
  - `TemplateGroupId`: `<optional-template-group-id>`
  - `StorageLocation`: `<optional-storage-location>`

## 2) Query media details

- API: `GetVideoInfo`
- Required params template:
  - `VideoId`: `<video-id>`

## 3) Get playback authorization

- API: `GetVideoPlayAuth`
- Required params template:
  - `VideoId`: `<video-id>`
  - `AuthInfoTimeout`: `<3600>`

## 4) Submit transcode jobs

- API: `SubmitTranscodeJobs`
- Required params template:
  - `VideoId`: `<video-id>`
  - `TemplateGroupId`: `<template-group-id>`
  - `Priority`: `<1-10>`

## 5) Delete media assets

- API: `DeleteVideo`
- Required params template:
  - `VideoIds`: `<video-id-1,video-id-2>`

## Evidence Checklist

- Save request payloads and API responses under `output/aliyun-vod-manage/`.
- Keep a mapping of input file names to returned media IDs.
