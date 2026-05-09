---
name: control-network-setup
description: Repo-local playbook for setting up or troubleshooting the miniBIOTA Opal/Wyse/MQTT/ESP32 control network.
---
# Control Network Setup

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when Josue says things like:

- "Set up the Opal router."
- "Check the MQTT broker."
- "Why can't the node connect?"
- "What are the MQTT topics?"
- "How do I rebuild the control system?"
- "Add a new ESP32 node."

## Required Memory

- `memory/03-control-network.md`
- `memory/04-firmware-and-biome-map.md`
- `memory/06-hardware-safety-rules.md`

## Required References

- `systems/05-control-system/`
- `skills/control-network-setup/reference/control-system-setup.md`
- `skills/control-network-setup/reference/control-network.md`

## Workflow

1. Identify which layer is involved: Opal, Wyse/Mosquitto, ESP32 node, MQTT topics, OTA, App Monitoring, or wiring.
2. Read the relevant reference section before giving exact commands or addresses.
3. Distinguish read-only checks from configuration changes.
4. Ask before changing router/Wyse/Mosquitto/systemd configuration or publishing MQTT commands.
5. For node-specific work, verify the biome ID and folder before using topics or hostnames.
6. Prefer read-only diagnostics first: status checks, logs, read-only subscriptions, app observation, or local builds.
7. Report exactly what was checked and what was not changed.

## Expected Output

```markdown
Control network work:
- Layer:
- Read-only checks:
- Config changes:
- MQTT publishes:
- Next step:
```

## Write And Approval Rules

- Respect `MINIBIOTA_WRITE_MODE`.
- Opal, Wyse, Mosquitto, systemd, MQTT publishes, OTA, and firmware upload actions require explicit approval when they change live behavior or configuration.
- Do not create dummy MQTT publishes to inspect behavior.
