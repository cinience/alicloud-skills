# Apps Workspace

This directory contains application code for this repository.

## Layout

- `cmd/alicloud-skills`: Go CLI entrypoint.
- `internal/agent`: shared Go runtime/agent logic for the CLI/Desktop app.
- `desktop`: Wails-based desktop app backend and embedded web assets.
- `web`: Next.js frontend app.
- `go.mod`, `go.sum`: Go module definition for all Go code in `apps/`.

## Common Commands

Run from repository root:

```bash
make test
make build-cli
make build-desktop
make run
```

Direct Go commands:

```bash
go -C apps test ./...
go -C apps build ./cmd/alicloud-skills
go -C apps run ./cmd/alicloud-skills run --help
```

Web commands:

```bash
pnpm --dir apps/web install --frozen-lockfile --ignore-scripts
pnpm --dir apps/web lint
pnpm --dir apps/web build
pnpm --dir apps/web test:e2e
```

See [apps/web/README.md](/home/vipas/workspace/saker-ai/alicloud-skills/apps/web/README.md) for app-specific frontend notes.
