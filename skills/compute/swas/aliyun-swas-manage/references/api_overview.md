API 概览（SWAS-OPEN 2020-06-01）
================================================

来源：阿里云帮助文档「API概览」。用于快速定位接口分组与操作名。详情与参数以原文档为准。

目录
----
- 实例
- 密钥对
- 防火墙模板
- 防火墙
- 快照
- 磁盘
- 自定义镜像
- 命令助手
- 轻量数据库服务
- 标签
- 其他资源

实例
----
- CreateInstances: 创建实例
- StartInstance / StartInstances: 启动实例（单/批量）
- ListInstanceStatus: 批量获取实例状态
- StopInstance / StopInstances: 停止实例（单/批量）
- UpdateInstanceAttribute: 修改实例部分信息（名称/密码）
- ListInstances: 获取实例列表
- LoginInstance: 远程登录实例（Workbench）
- DescribeInstanceVncUrl: 获取实例 VNC 连接地址
- ModifyInstanceVncPassword: 修改实例 VNC 密码
- ListInstancePlansModification: 获取可升级套餐列表
- ListInstancesTrafficPackages: 获取流量包使用情况
- DescribeInstancePasswordsSetting: 查询是否设置过密码
- InstallCloudMonitorAgent: 安装云监控插件
- DescribeCloudMonitorAgentStatuses: 查询云监控插件状态
- DescribeMonitorData: 获取实例监控数据
- DescribeSecurityAgentStatus: 查询安全中心 Agent 状态
- RebootInstance / RebootInstances: 重启实例（单/批量）
- UpgradeInstance: 升级实例套餐
- RenewInstance: 续费实例
- ResetSystem: 重置系统

密钥对
------
- CreateInstanceKeyPair / CreateKeyPair: 创建密钥对
- UploadInstanceKeyPair / ImportKeyPair: 导入密钥对
- DescribeInstanceKeyPair: 查询实例密钥对信息
- ListKeyPairs: 查询密钥对列表
- AttachKeyPair / DetachKeyPair: 绑定/解绑密钥对
- DeleteInstanceKeyPair / DeleteKeyPairs: 删除密钥对

防火墙模板
----------
- CreateFirewallTemplate: 创建防火墙模板
- DescribeFirewallTemplates: 查询防火墙模板
- CreateFirewallTemplateRules: 创建防火墙模板规则
- ApplyFirewallTemplate: 应用防火墙模板
- ModifyFirewallTemplate: 修改防火墙模板
- DescribeFirewallTemplateApplyResults: 查询模板应用结果
- DescribeFirewallTemplateRulesApplyResult: 查询模板规则应用结果
- DeleteFirewallTemplateRules: 删除防火墙模板规则
- DeleteFirewallTemplates: 删除防火墙模板

防火墙
------
- DeleteFirewallRules / DeleteFirewallRule: 批量/单条删除防火墙规则
- CreateFirewallRule / CreateFirewallRules: 创建防火墙规则（单/批量）
- ListFirewallRules: 查询实例防火墙规则
- ModifyFirewallRule: 修改防火墙规则
- EnableFirewallRule / DisableFirewallRule: 启用/禁用防火墙规则

快照
----
- CreateSnapshot: 创建快照
- ListSnapshots: 获取快照
- UpdateSnapshotAttribute: 修改快照备注
- DeleteSnapshot / DeleteSnapshots: 删除快照（单/批量）

磁盘
----
- UpdateDiskAttribute: 修改数据盘备注
- ListDisks: 查询磁盘信息
- ResetDisk: 回滚磁盘

自定义镜像
----------
- CreateCustomImage: 创建自定义镜像
- ListCustomImages: 查询自定义镜像
- ModifyImageShareStatus: 共享/解除共享自定义镜像
- AddCustomImageShareAccount: 跨账号共享自定义镜像
- ListCustomImageShareAccounts: 查看跨账号共享信息
- RemoveCustomImageShareAccount: 取消跨账号共享
- DeleteCustomImage / DeleteCustomImages: 删除自定义镜像（单/批量）

命令助手
--------
- DescribeCloudAssistantAttributes: 查询命令助手信息
- UpdateCommandAttribute: 修改命令
- InvokeCommand: 执行命令（通过已有命令）
- DescribeCommands: 查询命令
- DescribeCommandInvocations: 查询命令执行列表与状态
- DeleteCommand: 删除命令
- CreateCommand: 创建命令
- StartTerminalSession: 开启免密登录会话
- InstallCloudAssistant: 安装云助手
- DescribeCloudAssistantStatus: 查询云助手安装状态
- DescribeInvocationResult: 查询单个命令执行结果
- RunCommand: 执行命令（直接下发）
- DescribeInvocations: 查看命令详细信息

轻量数据库服务
--------------
- ModifyDatabaseInstanceParameter: 修改数据库参数
- StopDatabaseInstance / StartDatabaseInstance: 停止/启动数据库实例
- ModifyDatabaseInstanceDescription: 修改数据库实例描述
- DescribeDatabaseSlowLogRecords: 查询慢日志明细
- DescribeDatabaseErrorLogs: 查询错误日志
- DescribeDatabaseInstanceMetricData: 查询数据库监控
- DescribeDatabaseInstanceParameters: 查看数据库参数
- DescribeDatabaseInstances: 查看数据库实例信息
- AllocatePublicConnection: 申请公网访问地址
- RestartDatabaseInstance: 重启数据库实例
- ResetDatabaseAccountPassword: 重置数据库账号密码
- ReleasePublicConnection: 释放外网访问地址

标签
----
- TagResources: 绑定标签
- ListTagResources: 查询标签列表
- UntagResources: 解绑并删除标签

其他资源
--------
- ListRegions: 查询可用地域列表
- ListImages: 获取镜像列表
- ListPlans: 获取套餐信息
