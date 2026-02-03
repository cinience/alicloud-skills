# Python SDK 基本调用

## 安装

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U aliyun-log-python-sdk
```

## 初始化与查询

```python
from aliyun.log import LogClient, GetLogsRequest

client = LogClient(endpoint, access_key_id, access_key_secret)
request = GetLogsRequest(project, logstore, from_time, to_time, query=query)
response = client.get_logs(request)
logs = response.get_logs()
```
