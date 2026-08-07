# Agent-fulfilled Dreams — script-assisted pattern
If your agent's unattended/cron mode sandboxes file & terminal tools (common,
and correct security), split the job: scripts do deterministic I/O, the agent
only thinks.
1. `dream_context.py` — agent-mode cron script: injects the Dream contract +
   fresh live-data into the prompt. The agent's ENTIRE response is the raw
   dream JSON.
2. `dream_writer.py` — companion no-agent cron (e.g. every 30 min): extracts
   the newest valid JSON response from the job's run logs, validates required
   fields, writes `<CLAUDE_OS_AGENT_DREAM_DIR>/dreams/dream-<date>.json`.
Set `LOG_DIR` (the generator job's output dir) and `OUT_DIR` in dream_writer.py
to your paths. Hermes example: `hermes cron create '0 10 * * *' "<prompt>"
--script dream_context.py` + `hermes cron create '*/30 * * * *' --no-agent
--script dream_writer.py`.
