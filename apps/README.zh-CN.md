# Apps 工作区

该目录存放本仓库的应用代码。

## 目录结构

- `cmd/alicloud-skills`：Go CLI 入口。
- `internal/agent`：CLI/Desktop 共用的 Go 运行时与 Agent 逻辑。
- `desktop`：基于 Wails 的桌面应用后端与嵌入资源。
- `web`：Next.js 前端应用。
- `go.mod`、`go.sum`：`apps/` 下 Go 代码的模块定义。

## 常用命令

在仓库根目录执行：

```bash
make test
make build-cli
make build-desktop
make run
```

直接执行 Go 命令：

```bash
go -C apps test ./...
go -C apps build ./cmd/alicloud-skills
go -C apps run ./cmd/alicloud-skills run --help
```

Web 相关命令：

```bash
pnpm --dir apps/web install --frozen-lockfile --ignore-scripts
pnpm --dir apps/web lint
pnpm --dir apps/web build
pnpm --dir apps/web test:e2e
```

前端应用的细节说明见 [apps/web/README.md](/home/vipas/workspace/saker-ai/alicloud-skills/apps/web/README.md)。
