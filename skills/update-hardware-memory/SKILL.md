---
name: update-hardware-memory
description: Repo-local playbook for safely promoting recurring hardware decisions or repeated instructions into Hardware memory files.
---
# Update Hardware Memory

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when Josue says things like:

- "Remember this for future hardware work."
- "Add this to Hardware memory."
- "Make this a durable hardware rule."
- "Update the Hardware Agent memory."
- "This should be part of the control-system workflow now."

## Required Memory

- `memory/00-index.md`
- `memory/01-agent-purpose.md` when the agent role changes
- `memory/02-system-architecture.md` when physical/hydrological/climate architecture changes
- `memory/03-control-network.md` when Opal/Wyse/MQTT/network assumptions change
- `memory/04-firmware-and-biome-map.md` when biome firmware status changes
- `memory/05-telemetry-and-data-flow.md` when telemetry architecture changes
- `memory/06-hardware-safety-rules.md` when safety or approval rules change
- `memory/07-cross-agent-relationships.md` when cross-domain boundaries change
- `memory/08-recurring-decisions.md` for durable decisions
- `memory/inbox.md` for untriaged candidate memory

## Workflow

1. Capture the candidate memory in the user's words.
2. Decide whether it is durable, temporary, task-specific, or already recorded.
3. Check the relevant memory file and `memory/00-index.md` for duplicates.
4. Choose the smallest correct home. Use `memory/inbox.md` when the home is unclear.
5. Update memory concisely. Prefer one durable rule over a long recap.
6. Update `memory/00-index.md` only when a new file, major routing change, or new playbook needs discoverability.
7. Update skill reference files only when exact setup/protocol detail changes.
8. Update the Brain engineering brief when strategy-level state changes.
9. Read every changed memory/reference file end to end.

## Expected Output

```markdown
Memory proposal:
- Candidate memory:
- Durable or temporary:
- Existing duplicate check:
- Target file:
- Proposed wording:
- Brain brief update:

After update:
- Changed files:
- Read-through:
- Remaining questions:
```

## Write And Approval Rules

- Ask before promoting memory unless the user explicitly requested the write.
- Keep memory concise and stable.
- Do not use memory files as session logs.
- Preserve source-of-truth order from `AGENTS.md`.

## Do Not Do

- Do not create uncontrolled memory bloat.
- Do not duplicate detailed reference files inside memory.
- Do not overwrite implemented firmware/service truth.
- Do not write raw setup detail into the Brain engineering brief.
