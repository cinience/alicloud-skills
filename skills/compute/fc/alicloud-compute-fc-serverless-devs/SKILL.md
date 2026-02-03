---
name: alicloud-compute-fc-serverless-devs
description: Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function. Use when users need CLI-based FC quick start or Serverless Devs setup guidance.
---

Category: tool

# 函数计算（FC 3.0）Serverless Devs

## 目标

- 安装并验证 Serverless Devs。
- 配置凭证、初始化示例、部署、调用与删除。
- 以 Python 运行时为例提供 CLI 流程。

## 快速接入流程

1. 安装 Node.js（14+）与 npm。
2. 安装并验证 Serverless Devs。
3. 通过引导完成凭证配置。
4. 初始化示例项目并进入目录。
5. 部署、调用与可选删除。

## 安装 Serverless Devs（npm）

全局安装（需要 sudo 权限）：

```bash
sudo npm install @serverless-devs/s -g
sudo s -v
```

无 sudo 的替代方案（推荐在受限环境使用）：

```bash
npx -y @serverless-devs/s -v
```

## 配置凭证（引导式）

```bash
sudo s config add
```

选择 `Alibaba Cloud (alibaba)`，按提示填写 `AccountID`、`AccessKeyID`、`AccessKeySecret`，并设置 alias。

## 配置凭证（命令式）

使用命令行参数一次性写入密钥别名（无需交互）：

```bash
s config add -a default --AccessKeyID <AK> --AccessKeySecret <SK> -f
```

如果使用环境变量，可将其注入命令（示例）：

```bash
s config add -a default -kl AccessKeyID,AccessKeySecret -il ${ALIBABA_CLOUD_ACCESS_KEY_ID},${ALIBABA_CLOUD_ACCESS_KEY_SECRET} -f
```

或者使用 Serverless Devs 约定的环境变量 JSON（示例）：

```bash
export default_serverless_devs_key='{\"AccountID\":\"<AccountID>\",\"AccessKeyID\":\"<AK>\",\"AccessKeySecret\":\"<SK>\"}'
```

`s.yaml` 中引用：

```yaml
access: default_serverless_devs_key
```

## 初始化示例（Python）

```bash
sudo s init start-fc3-python
cd start-fc3-python
```

初始化完成后会生成 `s.yaml`、`code/` 与 `readme.md`，可在 `code/index.py` 修改函数逻辑。

## 部署、调用与删除

```bash
sudo s deploy
sudo s invoke -e "test"
sudo s remove
```

## 自定义域名绑定（避免默认域名强制下载）

> 说明：FC 默认域名会强制添加 `Content-Disposition: attachment`，浏览器会触发下载。
> 需要通过自定义域名访问才能去掉该行为。

### 步骤 1：为域名配置 CNAME

在 DNS 服务商处把域名解析到 FC 公网 CNAME：

```
<account_id>.<region_id>.fc.aliyuncs.com
```

示例（杭州地域）：

```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```

注意：如果是根域名（例如 `animus.run`）且 DNS 不支持根域名 CNAME，
请使用 ALIAS/ANAME 记录，或改用 `www.animus.run` 子域名。

### 步骤 2：在 Serverless Devs 中创建自定义域名

方式 A：在 `s.yaml` 中新增 `fc3-domain` 资源：

```yaml
resources:
  newsDomain:
    component: fc3-domain
    props:
      region: cn-hangzhou
      domainName: animus.run
      protocol: HTTP
      routeConfig:
        routes:
          - functionName: honnold-taipei101-news
            qualifier: LATEST
            methods:
              - GET
              - HEAD
            path: /*
```

`region` 为示例默认值；若未确定最合适 Region，执行时应询问用户。

然后部署：

```bash
printf 'y\n' | npx -y @serverless-devs/s deploy
```

方式 B：使用控制台（Advanced Features > Custom Domains）创建自定义域名并配置路由。

### 常见错误

- `DomainNameNotResolved`：域名未解析到正确的 FC CNAME。
- `InvalidICPLicense`：中国大陆地域需要 ICP 备案且备案需接入阿里云。

## 参考

- 细节与官方步骤见 `references/install_serverless_devs_and_docker.md`。
- HTTP 触发器限制与响应头说明（默认域名会强制添加 Content-Disposition: attachment）
  - https://www.alibabacloud.com/help/en/functioncompute/fc-3-0/user-guide/http-triggers-overview
- 自定义域名绑定与 CNAME 说明
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names

- 官方文档来源清单：`references/sources.md`
