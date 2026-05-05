---
name: telemetry-coordinator
description: Repo-local playbook for the Wyse read-only telemetry coordinator, Supabase snapshot flow, website telemetry contract, and coordinator tests.
---
# Telemetry Coordinator

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when Josue says things like:

- "Work on the telemetry coordinator."
- "Deploy the Wyse snapshot service."
- "Update the telemetry pipeline."
- "Fix the website monitoring payload."
- "Add Supabase telemetry history."
- "Test telemetry snapshot output."

## Required Memory

- `memory/05-telemetry-and-data-flow.md`
- `memory/06-hardware-safety-rules.md`
- `memory/07-cross-agent-relationships.md`
- `memory/08-recurring-decisions.md`

## Required References

- `skills/telemetry-coordinator/reference/telemetry-pipeline-plan.md`
- `services/telemetry_coordinator.py`
- `services/tests/test_telemetry_coordinator.py`
- `deploy/systemd/minibiota-telemetry.service.example` when deployment is in scope

## Workflow

1. Determine whether the task is read-only code/test work, deployment, schema work, live MQTT work, or command-path work.
2. Read the telemetry plan reference and current service/tests before changing behavior.
3. Preserve the first coordinator implementation's read-only boundary unless the user explicitly scopes command publishing or history writes.
4. Ask before Supabase schema changes, Wyse service deployment, MQTT publishing, or setpoint command processing.
5. Keep the website snapshot contract compatible with the Web telemetry consumer.
6. Run `python -m unittest discover services/tests` when practical.
7. Use dry-run output for contract checks when useful.
8. Report whether any live MQTT, schema, service deployment, or command behavior changed.

## Expected Output

```markdown
Telemetry work:
- Surface:
- Files changed:
- Contract checked:
- Tests:
- Live systems touched:
- Deferred items:
```

## Write And Approval Rules

- Respect `MINIBIOTA_WRITE_MODE`.
- Coordinator code edits are okay after stating intent when write mode allows.
- Schema/table changes require explicit approval.
- MQTT publishing or setpoint command processing requires explicit approval.
- Service deployment or Wyse/systemd configuration changes require explicit approval.
