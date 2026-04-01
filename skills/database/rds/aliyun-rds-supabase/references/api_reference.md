核心接口参数速查
================

说明：以下为常用接口的高频参数摘要，完整参数与约束以官方文档为准（见 `sources.md`）。

CreateAppInstance（创建实例）
---------------------------
常见参数：
- RegionId
- AppType（目前为 `supabase`）
- VSwitchId
- InstanceClass（当前仅 `rdsai.supabase.basic`）
- DBInstanceName（RDS PostgreSQL 实例 ID）
- AppName
- ClientToken（幂等）
- DatabasePassword / DashboardUsername / DashboardPassword
- PublicNetworkAccessEnabled
- PublicEndpointEnabled
- InitializeWithExistingData
- DBInstanceConfig（含 DBInstanceClass / DBInstanceStorage / PayType）

StartInstance / StopInstance / RestartInstance（生命周期）
-------------------------------------------------------
常见参数：
- RegionId
- InstanceName（实例 ID）

ModifyInstanceAuthConfig（认证配置）
-----------------------------------
常见参数：
- RegionId
- InstanceName
- ConfigList（认证配置列表）
  - Name（如 GOTRUE_* 配置项）
  - Value

ModifyInstanceStorageConfig（存储配置）
--------------------------------------
常见参数：
- RegionId
- InstanceName
- ConfigList（存储配置列表）
  - Name（如 AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / GLOBAL_S3_BUCKET / GLOBAL_S3_ENDPOINT / REGION / TENANT_ID 等）
  - Value
- ClientToken

ModifyInstanceIpWhitelist（白名单）
----------------------------------
常见参数：
- RegionId
- InstanceName
- IpWhitelist（逗号分隔，支持 IP 或 CIDR）
- ModifyMode（Cover / Append / Delete）
- GroupName
- ClientToken

ModifyInstanceSSL（SSL）
-----------------------
常见参数：
- RegionId
- InstanceName
- SSLEnabled（1 开 / 0 关）
- CAType（目前为 custom）
- ServerCert / ServerKey（自定义证书内容）

DescribeAppInstances（实例列表）
-------------------------------
常见参数：
- RegionId
- DBInstanceName（按 PG 实例过滤）
- AppType（supabase）
- PageSize / PageNumber

DescribeAppInstanceAttribute（实例详情）
---------------------------------------
常见参数：
- RegionId
- InstanceName

DescribeInstanceEndpoints（连接地址）
------------------------------------
常见参数：
- RegionId
- InstanceName

ResetInstancePassword（重置密码）
--------------------------------
常见参数：
- RegionId
- InstanceName
- DashboardPassword
- DatabasePassword

DescribeInstanceAuthInfo（认证信息）
-----------------------------------
常见参数：
- RegionId
- InstanceName

DescribeInstanceStorageConfig（存储配置查询）
--------------------------------------------
常见参数：
- RegionId
- InstanceName

DescribeInstanceIpWhitelist（白名单查询）
----------------------------------------
常见参数：
- RegionId
- InstanceName
- GroupName

DescribeInstanceSSL（SSL 查询）
------------------------------
常见参数：
- RegionId
- InstanceName

ModifyInstanceRAGConfig / DescribeInstanceRAGConfig（RAG）
---------------------------------------------------------
常见参数：
- RegionId
- InstanceName
- Status（开启/关闭）
- ConfigList（Name/Value）

RDS AI 助手（对话/事件/Agent）
------------------------------
ChatMessages（发送对话）
- Query
- ConversationId / ParentMessageId
- RegionId / Language / Timezone
- CustomAgentId
- EventMode

ChatMessagesTaskStop（停止对话）
- TaskId

GetConversations（历史对话）
- LastId
- Limit
- Pinned
- SortBy

GetMessages（对话消息）
- ConversationId
- FirstId
- Limit

ModifyMessagesFeedbacks（消息反馈）
- MessageId
- Rating（like/dislike）
- Content

DescribeEventsList（事件列表）
- RegionId
- InstanceIdList
- StartTime / EndTime
- PageSize / PageNumber

ListCustomAgentTools（Agent 工具列表）
- 无入参

CreateCustomAgent（创建 Agent）
- Name
- SystemPrompt
- EnableTools
- Tools

UpdateCustomAgent（更新 Agent）
- CustomAgentId
- Name / SystemPrompt
- EnableTools
- Tools

GetCustomAgent（查询 Agent）
- CustomAgentId

ListCustomAgent（Agent 列表）
- PageNumber / PageSize

DeleteCustomAgent（删除 Agent）
- CustomAgentId
