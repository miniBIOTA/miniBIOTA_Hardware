# Hardware Database Access Responsibilities

The Hardware Agent treats database access as a live-system boundary. Read telemetry by default. Snapshot writes, control commands, and schema changes require explicit approval and careful verification.

## Access Model

- Database access needed: Yes, mostly read-only.
- Default mode: Read-only telemetry and structured status checks.
- MCP: Brain has broad Supabase MCP read awareness. This domain may use MCP read access for relevant telemetry/hardware records, but should escalate cross-domain interpretation to Brain.
- Preferred path: Brain helper functions in `M:\miniBIOTA\miniBIOTA_Brain\_system\minibiota_tools.py` and approved service code such as the telemetry coordinator.
- Secrets: Local environment variables or ignored local config only.

## Table Responsibilities

| Category | Tables |
|---|---|
| Owned | `telemetry_snapshot`; future `biome_telemetry` and `setpoint_commands` only when approved |
| Read-only | `biomes`, `species`, `biosphere_profile`, App monitoring records, public telemetry endpoints and `tasks` |
| Controlled write | `telemetry_snapshot` through approved service/helper paths; hardware `tasks` through helpers and durable context through repo/vault updates |
| Admin/migration | Telemetry schema, live-control tables, and migrations only with explicit user approval |

## Approval Boundary

Explicit user approval is required for raw SQL, migrations, destructive writes, schema changes, service-role actions, telemetry schema edits, live-control commands, setpoint queues, firmware changes that affect controls, MQTT topic changes, or deployment changes.

## Brain Reporting

At session close, update Brain when hardware state changes:

- `M:\miniBIOTA\miniBIOTA_Brain\6. miniBIOTA_Hardware\hardware_overview.md`
- `M:\miniBIOTA\miniBIOTA_Brain\6. miniBIOTA_Hardware\hardware_brief.md`

Report firmware status, telemetry status, live-system risks, deployment changes, wiring issues, and cross-domain dependencies back to Brain.
