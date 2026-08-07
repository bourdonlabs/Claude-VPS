# VPS & Self-Hosted Mode

*This fork makes Claude OS run first-class on any Linux VPS — containers, reverse proxies, always-on agents — while staying 100% backwards-compatible with the original Mac setup (every change is opt-in via env vars; Mac-only probes no-op gracefully).*

## Why
Upstream assumes one operator account on one Mac: tools detected via `/Applications` and `~`, the dashboard reached at `localhost`, engines executed as local CLIs. On a VPS none of that holds — agents live in containers, access comes through a proxy at your own domain, and your AI subscriptions are consumed by agents, not local apps. This fork closes each gap **config-first**: declare what the box can't detect, auto-detect what it can.

## Quick start (VPS)
1. Clone to your server; `bun install`; run under systemd (see `deploy/`).
2. Copy `.env.example` → `.env.local` and set the values for your stack.
3. Serve `127.0.0.1:<port>` through any reverse proxy — nginx, Caddy, Cloudflare Tunnel, Tailscale serve — at your own hostname, optionally under a sub-path (e.g. `/mission-control/`).
4. Open the wizard. Step 2 detects containerized Claude Code + Hermes; step 3 knows Qdrant; step 4 persists keys server-side; step 7 offers the agent-fulfilled Dream engine.

## Configuration (all optional — unset = original Mac behavior)
| Variable | What it does |
|---|---|
| `CLAUDE_OS_TRUSTED_HOSTS` | Comma-separated hostnames your proxy serves — trusted exactly like localhost. Empty = localhost-only (secure default). |
| `HERMES_HOME` | Where the Hermes agent's data lives (default `~/.hermes`). Point at a container volume mount and every Hermes panel (status/skills/sessions/memory/models + write features) runs against the real agent. |
| `CLAUDE_OS_CLAUDE_DIR` | Your real Claude Code data dir (default `~/.claude`; auto-falls-back to `/docker/*/claude-home`). Powers usage windows, projects, plan detection. |
| `CLAUDE_OS_CLAUDE_JSON` | Path to `.claude.json` (MCP connector detection) when it isn't next to the data dir. |
| `CLAUDE_OS_CLAUDE_CODE_HOME` | Explicit containerized Claude Code home for step-2 detection. |
| `CLAUDE_OS_HERMES_URL` | Hermes agent dashboard URL to live-probe (default `http://127.0.0.1:9119`). |
| `CLAUDE_OS_AGENT_DREAM_DIR` | Enables **agent-fulfilled Dreams** (below). |
| `CLAUDE_OS_CLAUDE_PLAN` | Declare your Claude plan (`pro`\|`max_5x`\|`max_20x`) — headless boxes can't sniff subscription tiers. |
| `CLAUDE_OS_CHATGPT_PLAN` | Declare your ChatGPT plan (`plus`\|`team`\|`pro`) when it's consumed by an agent rather than a local install. |
| `VITE_HERMES_AGENT_URL` | Where the "open Hermes" buttons point (default `http://localhost:9119`). |
| `QDRANT_URL` / `QDRANT_API_KEY` | Self-hosted vector DB — wizard card, integrations tile, and collections rendered in the memory constellation exactly like Pinecone. |

## Agent-fulfilled Dreams ($0 extra, no CLI, no API key)
Your always-on agent writes the nightly Dream on whatever subscription it already uses:
1. Set `CLAUDE_OS_AGENT_DREAM_DIR=/path/your/agent/can/reach` — the aggregator exports `live-data.json` there (inbox, ≤2 min fresh) and ingests `<dir>/dreams/` (outbox).
2. Drop `skills/dream/SKILL.md` in the folder as the contract.
3. Schedule your agent (early morning, your timezone): *read the contract + inbox → write `dreams/dream-YYYY-MM-DD.json` per the schema — file only, no prose.*
4. Wizard step 7 shows **Hermes (agent-fulfilled): ready**. Results appear on the Dream card minutes after your agent writes.

## Operational hardening included
- **Deterministic env reloads**: under systemd, any `.env.local` write triggers a clean process exit + 3s respawn (vite's in-place restart can wedge under bun). Bare `bun run dev` keeps stock behavior.
- **Liveness watchdog** (`deploy/`): probes the dashboard every 2 min, auto-restarts on 2 straight failures.
- **Linux Dream scheduling parity**: `scripts/install-dream-cron.ts` now really installs on Linux (idempotent marker-managed crontab, aggregate-then-dream, quoted paths) instead of printing a suggestion.
- **Container access pattern** (`deploy/`): read-only and read-write id-mapped bind mounts let the dashboard see agent volumes without touching their ownership — no chown/ACLs on agent data, ever.

## What stays desktop-first
Initial setup and the 3D graph views are desk surfaces by design. Mac-only signals (Keychain plan detection, `/Applications` scans) skip cleanly on Linux with the plan-declaration vars above as the honest replacement.
