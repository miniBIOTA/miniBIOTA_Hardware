---
id: hardware_cross_agent_relationships
title: Cross-Agent Relationships
domain: engineering_and_hardware
last_updated: 2026-05-10
tags: [memory, brain, app, web, content, research, supabase]
---
# Cross-Agent Relationships

Hardware owns implementation detail for the physical biosphere, firmware, control network, and telemetry producer surfaces. Other domains consume summarized state or structured outputs.

## Company / Brain

- Active Hardware operating summaries live in `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_overview.md` and `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`.
- Company reporting state lives in `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`. Brain copies are historical/archive lookup only.
- Hardware updates or flags Company reports when system state, priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change.
- Brain no longer mirrors Hardware docs. Company and Brain route detailed Hardware work to this repo's `AGENTS.md`, biome folders, `0. Hardware Systems/`, `memory/`, `skills/`, and `skills/*/reference/`.
- Keep firmware details, setup guides, and exact architecture references in this repo, especially biome folders and `0. Hardware Systems/`, not in Company summaries or the Brain archive lookup.

## App Agent

- App Monitoring consumes live MQTT data when on `mB2.4`.
- App setpoint control is a live-control surface and must coordinate with Hardware safety rules.
- App fallback telemetry from Supabase should match the coordinator snapshot contract.
- App Planner is the live project-management surface for Hardware work.
- Hardware projects are Hardware-owned Planner records. If Supabase `work_projects` or linked tasks still show Engineering / `Engineering & Hardware`, treat that as legacy Planner labeling that needs approved cleanup, not active ownership routing.
- Hardware sessions should read Planner tasks when choosing what to work on and should offer to mark tasks done when completed work clearly maps to an open task.
- Planner project/task creation, status changes, completion, archive, and subtask writes are live operational records and need explicit approval.

## Web Agent

- The website should consume public-safe telemetry from Supabase snapshots/history.
- Website telemetry contract details should stay aligned with `skills/telemetry-coordinator/reference/telemetry-pipeline-plan.md` and Web's technical architecture.
- Public website monitoring is read-only unless a separate approved command path exists.

## Content Agent

- Hardware downtime, rewire sessions, visible failures, rain events, wave/tide behavior, and sensor changes can affect filming and story planning.
- Coordinate before scheduling content that depends on biomes 2-5 during the planned sensor/controller rewire.
- The six public system names in `0. Hardware Systems/README.md` must stay aligned with website, App, and Company system records. Brain is historical/archive lookup only.

## Research / Ecosystem

- Hardware observations about climate, rain, hydrology, closure, and sensor failures can affect ecological interpretation.
- Do not turn hardware readings into ecological conclusions without the right Research/Ecosystem context.

## Supabase

- Supabase is canonical for structured telemetry records once tables are implemented.
- Supabase is canonical for Hardware Planner project/task records through the App Planner tables.
- Schema changes and command queue writes require explicit approval.
- Do not use Supabase as a scratchpad for testing return values.
