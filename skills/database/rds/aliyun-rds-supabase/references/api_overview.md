API 概览（RDS AI 服务 2025-05-07）
=================================

来源：阿里云文档「API概览」。用于快速定位接口分组与操作名，参数以原文档为准。文档链接见 `sources.md`。

目录
----
- RDS AI 助手
- 实例（RDS Supabase）
- RAG Agent
- 安全

RDS AI 助手
----------
- ChatMessages: 发送对话消息
- ModifyMessagesFeedbacks: 修改消息反馈
- ChatMessagesTaskStop: 停止对话
- GetConversations: 查看历史对话
- GetMessages: 查看对话消息
- DescribeEventsList: 查询事件列表
- ListCustomAgentTools: 查询用户 Agent 工具列表
- UpdateCustomAgent: 更新用户 Agent
- GetCustomAgent: 查询专属 Agent
- ListCustomAgent: 查询专属 Agent 列表
- DeleteCustomAgent: 删除用户 Agent
- CreateCustomAgent: 创建用户专属 Agent

实例（RDS Supabase）
-------------------
- CreateAppInstance: 创建 RDS AI 应用实例
- DeleteAppInstance: 删除 RDS AI 应用实例
- RestartInstance: 重启实例
- StopInstance: 暂停实例
- StartInstance: 启动实例
- ResetInstancePassword: 重置实例登录/数据库密码
- DescribeAppInstanceAttribute: 查询实例详情
- DescribeAppInstances: 查询实例列表
- DescribeInstanceEndpoints: 查询连接地址
- DescribeInstanceAuthInfo: 查询认证信息
- ModifyInstanceAuthConfig: 修改认证配置
- DescribeInstanceStorageConfig: 查看存储配置
- ModifyInstanceStorageConfig: 修改存储配置
- ModifyInstanceConfig: 修改实例通用配置（EIP/NAT 等）

RAG Agent
---------
- ModifyInstanceRAGConfig: 修改 RAG Agent 配置
- DescribeInstanceRAGConfig: 查看 RAG Agent 配置

安全
----
- ModifyInstanceIpWhitelist: 修改 IP 白名单
- DescribeInstanceIpWhitelist: 查看 IP 白名单
- ModifyInstanceSSL: 修改 SSL 配置
- ModifyInstancesSSL: 批量修改 SSL 配置
- DescribeInstanceSSL: 查看 SSL 配置
