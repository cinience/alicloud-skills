命令助手（Command/Invoke/Run）
=============================

来源：阿里云帮助文档 `InvokeCommand` 等接口说明。

关键点
------
- 目标实例必须处于 Running 状态。
- 实例需安装云助手 Agent（可用 `InstallCloudAssistant` 安装）。
- Windows 实例执行 PowerShell 需保证 PowerShell 模块可用。

常用接口
--------
- CreateCommand: 创建命令模板
- InvokeCommand: 在实例上执行已创建命令
- RunCommand: 直接下发命令执行（无需先创建命令）
- DescribeInvocations / DescribeInvocationResult: 查询执行结果与状态

常见参数提示
------------
- CommandType: `RunShellScript`（Linux）或 `RunPowerShellScript`（Windows）
- InstanceIds: 目标实例 ID 列表（JSON 数组）
- Timeout: 命令超时时间
- WorkingDir: 运行目录（可选）

最佳实践
--------
- 批量执行时优先使用 `InvokeCommand` 并轮询 `DescribeInvocations` 获取状态。
- 需要可复用/可审计时先 `CreateCommand`，否则直接 `RunCommand` 更快捷。
