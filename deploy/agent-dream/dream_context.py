"""Dream context feeder (agent-mode cron script for claude-os-dream).
Cron sessions have no file tools, so this script injects everything the agent
needs into the prompt: the Dream contract (SKILL.md) + the operator's fresh
live-data.json. The agent then answers with the raw dream JSON ONLY, and the
companion no-agent job (dream_writer.py) persists it to the outbox.
"""
import json, os, time, datetime
BASE = "/opt/data/shared/claude-os"
today = datetime.date.today().isoformat()
try:
    st = os.stat(f"{BASE}/live-data.json")
    age_h = (time.time() - st.st_mtime) / 3600
    live = open(f"{BASE}/live-data.json").read()
    skill = open(f"{BASE}/SKILL.md").read()
except OSError as e:
    print(f"DREAM-CONTEXT ERROR: {e}. Respond with exactly [SILENT].")
    raise SystemExit(0)
if age_h > 26:
    print(f"DREAM-CONTEXT: live-data.json is {age_h:.0f}h stale (>26h). Respond with exactly [SILENT].")
    raise SystemExit(0)
print(f"DREAM-CONTEXT: today={today} · live-data age={age_h:.1f}h · contract and data follow.")
print("\n===== DREAM CONTRACT (SKILL.md) =====\n")
print(skill)
print("\n===== OPERATOR LIVE DATA (live-data.json) =====\n")
print(live)
