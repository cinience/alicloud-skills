# 应用部署工作流

本文档记录将应用二进制部署到 SWAS 轻量应用服务器的最佳实践，包括 systemd 服务管理、二进制更新流程以及与 ESA CDN 联动的回源架构。

## 部署架构

```
用户 → ESA CDN (HTTPS/SSL 终止) → Origin Rule (HTTP:端口) → SWAS 服务器 → 应用服务
```

- **ESA CDN** 负责 SSL 终止、DDoS 防护和全球加速
- **Origin Rule** 控制回源协议（HTTP）和端口
- **SWAS 服务器** 运行应用服务，由 systemd 管理

## Systemd 服务配置

### 创建服务文件

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/myapp --server --addr :10112
Restart=always
RestartSec=5
WorkingDirectory=/root
Environment=HOME=/root
# 敏感信息通过环境变量注入
Environment=API_KEY=your-api-key

[Install]
WantedBy=multi-user.target
```

### 常用管理命令

```bash
# 启用开机自启
systemctl enable myapp

# 启动/停止/重启
systemctl start myapp
systemctl stop myapp
systemctl restart myapp

# 查看状态
systemctl status myapp

# 查看日志
journalctl -u myapp -n 50
journalctl -u myapp -f  # 实时跟踪

# 重新加载服务文件（修改 .service 后）
systemctl daemon-reload
```

## 二进制更新流程

### 关键：先停服务再上传

直接覆盖运行中的二进制文件会报 **"text file busy"** 错误。正确流程：

```bash
# 1. 交叉编译（本机）
GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64 ./cmd/

# 2. 停止远端服务
ssh -p $SSH_PORT root@$SERVER_IP "systemctl stop myapp"

# 3. 上传二进制
scp -P $SSH_PORT myapp-linux-amd64 root@$SERVER_IP:/usr/local/bin/myapp

# 4. 重启服务
ssh -p $SSH_PORT root@$SERVER_IP "chmod +x /usr/local/bin/myapp && systemctl start myapp"

# 5. 验证
sleep 2
ssh -p $SSH_PORT root@$SERVER_IP "systemctl is-active myapp"
```

### 部署脚本模板

```bash
#!/usr/bin/env bash
set -euo pipefail

SERVER_IP="1.2.3.4"
SSH_PORT="22"
SSH_USER="root"
SSH_OPTS="-o StrictHostKeyChecking=no"
APP_SRC="../myapp"
BINARY_NAME="myapp-linux-amd64"
REMOTE_BIN="/usr/local/bin/myapp"

echo "=== Deploy ==="

# 1. Build
echo "[1/3] Building for linux/amd64..."
cd "$APP_SRC"
git pull
GOOS=linux GOARCH=amd64 go build -o "$BINARY_NAME" ./cmd/
cd -

# 2. Upload (stop first to avoid "text file busy")
echo "[2/3] Uploading to ${SERVER_IP}..."
ssh -p "$SSH_PORT" $SSH_OPTS "${SSH_USER}@${SERVER_IP}" "systemctl stop myapp"
scp -P "$SSH_PORT" $SSH_OPTS "${APP_SRC}/${BINARY_NAME}" "${SSH_USER}@${SERVER_IP}:${REMOTE_BIN}"

# 3. Restart
echo "[3/3] Restarting service..."
ssh -p "$SSH_PORT" $SSH_OPTS "${SSH_USER}@${SERVER_IP}" \
    "chmod +x ${REMOTE_BIN} && systemctl start myapp"

# Verify
sleep 2
STATUS=$(ssh -p "$SSH_PORT" $SSH_OPTS "${SSH_USER}@${SERVER_IP}" "systemctl is-active myapp")
echo ""
echo "Service status: ${STATUS}"
echo "Done."
```

## 与 ESA CDN 联动

要将 SWAS 服务器上的应用通过 ESA CDN 暴露为 HTTPS 服务：

### 前置配置（一次性）

1. **ESA DNS 记录**: 添加 A 记录指向 SWAS IP，`proxied=true`
2. **SSL 证书**: 通过 ESA 申请免费 Let's Encrypt 证书
3. **Origin Rule**: 配置回源协议 HTTP、回源端口

详见 ESA skill 的 `references/origin-rules.md`。

### 流量路径

```
客户端 HTTPS 请求
  → ESA 边缘节点（SSL 终止、缓存、WAF）
    → Origin Rule 匹配（协议转换 HTTPS→HTTP）
      → HTTP 回源到 SWAS 服务器指定端口
        → 应用服务处理请求
```

### 验证连通性

```bash
# 1. 直接访问源站（绕过 CDN）
curl -sI http://$SERVER_IP:$PORT

# 2. 通过 CDN 访问
curl -sI https://sub.example.com

# 3. 检查响应头确认走了 ESA
# Server 应为 "ESA"，而非 "nginx" 或 "openresty"
```

## 安全最佳实践

### 敏感信息管理

- 不要在服务文件中存放明文密钥
- 使用应用内置的加密方案（如 AES-256-GCM）加密 API key
- Master key 通过 systemd Environment 注入
- 加密后的值以特定前缀标识（如 `ENC:`），应用启动时自动解密

### 防火墙

- SWAS 服务端口**无需**对公网开放（如果通过 ESA CDN 回源）
- ESA 回源 IP 来自 ESA 边缘节点，可配置防火墙仅放行 ESA IP 段
- SSH 端口建议修改为非标准端口，使用密钥认证

### SWAS 防火墙规则

通过 SWAS API 管理防火墙：

```python
# 开放应用端口（仅在需要直接访问时）
client.create_firewall_rules(swas_models.CreateFirewallRulesRequest(
    instance_id='your-instance-id',
    region_id='cn-shanghai',
    firewall_rules=[{
        'RuleProtocol': 'TCP',
        'Port': '10112',
        'SourceCidrIp': '0.0.0.0/0',  # 生产环境建议限制为 ESA IP 段
        'Remark': 'App service port'
    }]
))
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `text file busy` | 覆盖运行中的二进制 | 先 `systemctl stop` 再上传 |
| 服务启动失败 | 二进制权限不对 | `chmod +x /usr/local/bin/myapp` |
| 端口被占用 | 旧进程未完全退出 | `lsof -i :端口` 查看并 kill |
| CDN 502 | 源站服务未启动或端口不对 | 直接 curl 源站确认 |
| CDN 返回旧内容 | 边缘缓存 | 等待过期或手动刷新 |
| SSH 连接超时 | 端口或密钥错误 | 确认 SSH 端口和密钥配置 |
