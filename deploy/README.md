# Deploy examples (Linux VPS, systemd)
Adjust paths/users, then: `cp *.service *.timer /etc/systemd/system/ && systemctl daemon-reload && systemctl enable --now <units>`.
- `claude-os.service` — the dashboard under systemd (Restart=always pairs with the clean env-reload exit).
- `claude-os-aggregate.service` + `.timer` — data refresh every 2 minutes.
- `claude-os-watchdog.service` + `.timer` — liveness probe + auto-restart.
- `agent-home-mount.service` — id-mapped bind mount pattern for reading/writing a containerized agent's volume WITHOUT touching its ownership (map the agent's uid:gid to your service user's). Read-only variant: add `ro`.
  RULES: never chown/chmod/setfacl agent data; only the mapped service user operates through the mount; root inspects raw paths only.
