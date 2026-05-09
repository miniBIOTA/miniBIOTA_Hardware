---
name: hardware-architecture-reference
description: Repo-local playbook for answering or updating physical, hydrological, climate, rain, enclosure, and system-boundary hardware architecture context.
---
# Hardware Architecture Reference

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when Josue says things like:

- "Explain the physical architecture."
- "How does the rain system work?"
- "What is connected to what?"
- "Update the hydrology reference."
- "What counts as the system boundary?"
- "How are the atmospheres mounted?"

## Required Memory

- `memory/02-system-architecture.md`
- `memory/06-hardware-safety-rules.md`
- `memory/07-cross-agent-relationships.md`
- `memory/08-recurring-decisions.md`

## Required References

- Start with the relevant `0. Hardware Systems/` folder:
  - `0. Hardware Systems/1. Climate System/`
  - `0. Hardware Systems/2. Rain System/`
  - `0. Hardware Systems/3. Lighting System/`
  - `0. Hardware Systems/4. Wave & Tide System/`
  - `0. Hardware Systems/5. Control System/`
  - `0. Hardware Systems/6. Enclosure/`
- Use `skills/hardware-architecture-reference/reference/physical-architecture.md`, `hydrological-architecture.md`, and `climate-and-rain-system.md` only for older supporting context that has not yet been promoted into `0. Hardware Systems/`.

## Workflow

1. Identify whether the question is about enclosure, hydrology, air topology, climate, rain, closure, or naming.
2. Read the relevant memory and exact `0. Hardware Systems/` file before answering detailed questions.
3. Keep current state, target state, and planned future features separate.
4. Use current canonical biome names: Freshwater Lake, Lakeshore, Lowland Meadow, Mangrove Forest, Marine Shore, Seagrass Meadow.
5. When architecture changes affect Brain strategy state, update the Brain engineering brief at closeout.
6. Do not make physical-world recommendations that alter live conditions without naming safety implications and getting approval when needed.

## Expected Output

```markdown
Architecture answer:
- Current state:
- Target/planned state:
- Safety or cross-domain implications:
- Source reference:
```

## Write And Approval Rules

- Respect `MINIBIOTA_WRITE_MODE`.
- Architecture docs can be edited after stating intent when write mode allows.
- Physical changes to the live biosphere require explicit approval.
