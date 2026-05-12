---
name: hardware-session-closeout
description: Close Hardware sessions with changed files, verification, Company report implications, Brain transition implications, live-system non-change checks, and unresolved questions.
---
# Hardware Session Closeout

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when the user says:

- "close out"
- "session closeout"
- "wrap up Hardware"
- "finish this hardware session"
- "what changed?"

## Required Memory

- `memory/00-index.md`
- `memory/05-database-access.md`
- `memory/05-telemetry-and-data-flow.md`
- `memory/06-hardware-safety-rules.md`
- `memory/07-cross-agent-relationships.md`
- `memory/08-recurring-decisions.md`

## Workflow

1. Identify changed files and touched surfaces: firmware, services, deploy files, memory, systems, skills, references, Company reports, Supabase, MQTT, OTA, router/Wyse config, live controls, and physical-system assumptions.
2. Read every new or changed documentation, memory, skill, or reference file end to end.
3. Decide whether Company Hardware reports need an update for manager-facing system state, priorities, milestones, risks, blockers, canonical names, or cross-domain dependencies, and whether the Brain archive lookup still needs alignment.
4. Decide whether firmware behavior, telemetry coordinator behavior, MQTT topics, OTA behavior, Supabase telemetry/schema, router/Wyse configuration, or live-control paths changed.
5. Run the smallest meaningful verification for the touched surface when practical.
6. Check whether completed work maps to an open App Planner Hardware task.
7. If a task can be cleared, ask before marking it done unless the user explicitly approved the live Planner update or standing Hardware project-manager delegation is active.
8. Run `git diff --name-only`.
9. Run `git status --short --branch`.
10. Confirm no firmware upload, MQTT command, live control, schema change, deployment change, router/Wyse change, Planner write, or physical-world action occurred unless explicitly approved.
11. Report unresolved questions and any deferred Company report, task, deployment, or domain follow-up.

## Expected Output

```markdown
Changed files:
- path

Verification:
- command or read-through performed

Not changed:
- firmware/live controls/schema/MQTT/OTA/router/Wyse/etc. as relevant

Unresolved questions:
- item or "None"
```

## Write And Approval Rules

- Do not upload firmware, publish MQTT commands, change router/Wyse configuration, change telemetry schema, or touch live controls from closeout.
- Do not update Company Hardware reports or the Brain archive lookup unless manager-facing state changed and the user has not deferred it.
- Do not write Supabase telemetry/control records without explicit approval and readback.
- Do not create, edit, complete, archive, or delete App Planner project/task records without explicit approval or standing Hardware project-manager delegation; always read back changed Planner rows.
- Do not commit, push, deploy, or restart services unless explicitly scoped.

## Do Not Do

- Do not claim live hardware verification happened if it was skipped.
- Do not treat a documentation-only session as firmware, telemetry, or live-control change.
- Do not hide wiring, sensor, telemetry, or deployment risks discovered during the session.
- Do not leave hardware state changes only in chat history.
