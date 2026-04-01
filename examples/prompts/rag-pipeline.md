# 智能检索/RAG 系统

## 目标

从文档中构建向量索引并完成检索。

## 提示词样例

用 `aliyun-docmind-extract` 解析这个 PDF（URL: <your-pdf-url>），输出结构化结果并保存到 `output/`。

用 `aliyun-dashvector-search` 创建 dimension=768 的集合 `docs`，写入 5 条文档向量。

用 `aliyun-dashvector-search` 在集合 `docs` 上做 topk=5 相似度查询，过滤字段 `category=guide`。

如果需要备用方案，改用 `aliyun-opensearch-search` 或 `aliyun-milvus-search` 实现相同检索流程。
