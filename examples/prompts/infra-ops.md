# 计算与基础设施运维

## 目标

管理 ECS/SWAS 实例并进行日志排查与备份。

## 提示词样例

用 `aliyun-ecs-manage` 列出所有 Region 的 ECS 实例 ID、状态与规格。

用 `aliyun-swas-manage` 列出轻量应用服务器实例 ID、IP 与套餐规格。

用 `aliyun-sls-log-query` 查询最近 15 分钟 5xx 日志并按状态聚合。

用 `aliyun-hbr-backup` 查询备份任务状态，输出失败任务列表。

如需容灾中心流程，改用 `aliyun-bdrc-backup` 查询资源与策略。
