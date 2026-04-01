# PTS API Quick Map (2020-10-20)

Source: `https://api.aliyun.com/meta/v1/products/PTS/versions/2020-10-20/api-docs.json`

## Inventory And Resource Discovery

- `GetAllRegions`
- `GetUserVpcs`
- `GetUserVpcVSwitch`
- `GetUserVpcSecurityGroup`
- `ListEnvs`

## Scene Lifecycle

- `CreatePtsScene`
- `SavePtsScene`
- `ModifyPtsScene`
- `DeletePtsScene`
- `DeletePtsScenes`
- `ListPtsScene`
- `GetPtsScene`

## Open JMeter Scene Lifecycle

- `SaveOpenJMeterScene`
- `RemoveOpenJMeterScene`
- `ListOpenJMeterScenes`
- `GetOpenJMeterScene`

## Test Execution Control

- `StartPtsScene`
- `StopPtsScene`
- `AdjustPtsSceneSpeed`
- `GetPtsSceneRunningStatus`
- `GetPtsSceneRunningData`

## JMeter Test Execution Control

- `StartTestingJMeterScene`
- `StopTestingJMeterScene`
- `AdjustJMeterSceneSpeed`
- `GetJMeterSceneRunningData`

## Debug Control

- `StartDebugPtsScene`
- `StopDebugPtsScene`
- `GetPtsDebugSampleLogs`
- `StartDebuggingJMeterScene`
- `StopDebuggingJMeterScene`
- `GetJMeterSamplingLogs`

## Reports And Metrics

- `ListPtsReports`
- `GetPtsReportsBySceneId`
- `GetPtsReportDetails`
- `ListJMeterReports`
- `GetJMeterReportDetails`
- `GetJMeterSampleMetrics`
- `GetJMeterLogs`

## Baseline Management

- `CreatePtsSceneBaseLineFromReport`
- `GetPtsSceneBaseLine`
- `UpdatePtsSceneBaseLine`
- `DeletePtsSceneBaseLine`

## Environment Management

- `SaveEnv`
- `RemoveEnv`
