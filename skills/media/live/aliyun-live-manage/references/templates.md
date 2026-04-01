# Live Task Templates

Use these templates after confirming region/domain/app/stream.

## 1) Add a live domain

- API: `AddLiveDomain`
- Required params template:
  - `DomainName`: `<example.yourdomain.com>`
  - `DomainType`: `liveVideo`
  - `Region`: `<cn-hangzhou>`

## 2) Configure recording for an app

- API: `AddLiveAppRecordConfig`
- Required params template:
  - `DomainName`: `<live-domain>`
  - `AppName`: `<app-name>`
  - `OssEndpoint`: `<oss-cn-hangzhou.aliyuncs.com>`
  - `OssBucket`: `<bucket-name>`
  - `OssObjectPrefix`: `<recordings/{AppName}/{StreamName}>`
  - `OnDemond`: `<0|1>`

## 3) Query online streams

- API: `DescribeLiveStreamOnlineList`
- Required params template:
  - `DomainName`: `<live-domain>`
  - `AppName`: `<app-name>`
  - `PageNum`: `<1>`
  - `PageSize`: `<50>`

## 4) Forbid/resume a stream

- APIs: `ForbidLiveStream` / `ResumeLiveStream`
- Required params template:
  - `DomainName`: `<live-domain>`
  - `AppName`: `<app-name>`
  - `StreamName`: `<stream-name>`
  - `ResumeTime` (for forbid): `<2026-03-05T00:00:00Z>`

## Evidence Checklist

- Save request payloads and API responses under `output/aliyun-live-manage/`.
- Record exact region and timestamps for each mutation operation.
