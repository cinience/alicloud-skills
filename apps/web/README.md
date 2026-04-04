# Animus Web

This directory contains the Next.js frontend used by the desktop/web chat experience in this repository.

## Stack

- Next.js 16 App Router
- React 19
- Playwright for end-to-end checks
- A legacy chat surface mounted from `src/legacy/App`

## Local Development

From `apps/web`:

```bash
pnpm install --frozen-lockfile --ignore-scripts
pnpm dev
```

The dev server runs on `http://127.0.0.1:10111`.

## Common Commands

```bash
pnpm lint
pnpm build
pnpm test:e2e
```

From the repository root, the equivalent commands are:

```bash
pnpm --dir apps/web lint
pnpm --dir apps/web build
pnpm --dir apps/web test:e2e
```

## Environment

- `NEXT_PUBLIC_WS_URL` (optional)
- Default WebSocket endpoint: `ws://127.0.0.1:10112/ws`

## Notes

- The App Router entrypoint is `src/app/page.tsx`.
- The current UI is still branded as `Animus Web` in code and metadata.
- Static export artifacts are written to `apps/web/out/` after a production build.
