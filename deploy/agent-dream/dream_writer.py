"""Dream writer (no-agent cron). Finds the newest claude-os-dream run response,
extracts the raw dream JSON, validates the required schema fields, and writes
the outbox file the Claude OS aggregator ingests. Silent when nothing to do."""
import json, os, glob, re, datetime
OUT_DIR = "/opt/data/shared/claude-os/dreams"
LOGS = "os.environ.get("LOG_DIR", "/opt/data/cron/output/<your-dream-job-id>")"
logs = sorted(glob.glob(f"{LOGS}/*.md"), reverse=True)
for path in logs[:6]:
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"## Response\s*\n(.*)\Z", text, re.S)
    if not m:
        continue
    body = m.group(1).strip()
    body = re.sub(r"^```(?:json)?\s*", "", body)
    body = re.sub(r"\s*```$", "", body).strip()
    if not body.startswith("{"):
        continue
    try:
        dream = json.loads(body)
    except ValueError:
        continue
    if not all(k in dream for k in ("date", "model", "generatedAt", "prescriptions")):
        continue
    if not isinstance(dream["prescriptions"], list) or not dream["prescriptions"]:
        continue
    dest = f"{OUT_DIR}/dream-{dream['date']}.json"
    if os.path.exists(dest):
        break  # newest valid dream already persisted — nothing to do
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(dest, "w") as f:
        json.dump(dream, f, indent=2)
    print(f"dream_writer: wrote {dest} ({len(dream['prescriptions'])} prescriptions)")
    break
