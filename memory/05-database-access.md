# Hardware Database Access Responsibilities

The Hardware Agent treats database access as a live-system boundary. Read telemetry by default. Snapshot writes, control commands, and schema changes require explicit approval and careful verification.

## Access Model

- Database access needed: Yes, mostly read-only.
- Default mode: Read-only telemetry and structured status checks.
- MCP: Company owns active cross-domain operating interpretation. Brain may still provide broad Supabase MCP read awareness during transition; this domain may use MCP read access for relevant telemetry/hardware records, but should escalate cross-domain interpretation to Company.
- Preferred path: approved service code such as the telemetry coordinator for Hardware-owned workflows, App Planner for project/task records, Company/domain-owned helpers, and MCP/read-only awareness for controlled helper paths. Brain tool code is archive/recovery lookup only.
- Secrets: Local environment variables or ignored local config only.

## Table Responsibilities

| Category | Tables |
|---|---|
| Owned | `telemetry_snapshot`; `biome_telemetry`; future `setpoint_commands` only when approved |
| Read-only | `biomes`, `species`, `biosphere_profile`, App monitoring records, public telemetry endpoints, `work_projects`, and `tasks` |
| Controlled write | `telemetry_snapshot` and `biome_telemetry` through approved service/helper paths; Hardware Planner `work_projects` and `tasks` only after explicit user approval |
| Admin/migration | Telemetry schema, live-control tables, and migrations only with explicit user approval |

## Approval Boundary

Explicit user approval is required for raw SQL, migrations, destructive writes, schema changes, service-role actions, telemetry schema edits, live-control commands, setpoint queues, firmware changes that affect controls, MQTT topic changes, deployment changes, or Planner project/task writes.

## Planner Task Records

Hardware work is managed in the App Planner through Supabase `work_projects` and `tasks`.

- Read Planner projects/tasks when current work priorities, blockers, or completion status matter.
- Hardware Planner tasks should route to Hardware ownership. Any current Engineering / `Engineering & Hardware` labels are legacy Planner labels that need approved cleanup.
- Creating projects/tasks, linking tasks to projects, adding subtasks, changing status, marking done, or archiving are live operational writes.
- At closeout, offer to update Planner task status when completed work maps clearly to an open task.

## Project-Manager Delegation
When Josue grants standing Hardware project-manager delegation, the Hardware Agent may manage ordinary Hardware Planner `work_projects` and `tasks` through the approved shared Planner/Supabase write path. Current Hardware work should route to the Hardware domain/owner. Any current Engineering / `Engineering & Hardware` labels are legacy Planner labels; verify the live `work_domains` row before bulk changes and clean up legacy labels only through approved Planner writes. State intended Planner changes before writing, read changed rows back, and report changed records at closeout. This delegation does not cover telemetry/control records, firmware, MQTT, setpoints, deployment, schema/migrations, service-role/admin actions, app behavior, or live-biosphere actions.

## Company Reporting

At session close, update or flag Company Hardware reports when hardware state changes:

- `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_overview.md`
- `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Brain transition/archive fallback while retirement is in progress:

- `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_overview.md`
- `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Report firmware status, telemetry status, live-system risks, deployment changes, wiring issues, and cross-domain dependencies back to Company. Keep the Brain archive lookup aligned only when Brain transition state still needs it.
