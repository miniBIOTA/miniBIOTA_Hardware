---
id: hardware_cross_agent_relationships
title: Cross-Agent Relationships
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [memory, brain, app, web, content, research, supabase]
---
# Cross-Agent Relationships

Hardware owns implementation detail for the physical biosphere, firmware, control network, and telemetry producer surfaces. Other domains consume summarized state or structured outputs.

## Brain / Strategy Agent

- Brain strategy state lives in `M:\miniBIOTA\miniBIOTA_Brain\6. miniBIOTA_Hardware\hardware_brief.md`.
- Hardware updates the brief when system state, priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change.
- Brain no longer mirrors Hardware docs. Brain routes detailed Hardware work to this repo's `AGENTS.md`, biome folders, `systems/`, `memory/`, `skills/`, and `skills/*/reference/`.
- Keep firmware details, setup guides, and exact architecture references in this repo, especially biome folders and `systems/`, not in the Brain brief.

## App Agent

- App Monitoring consumes live MQTT data when on `mB2.4`.
- App setpoint control is a live-control surface and must coordinate with Hardware safety rules.
- App fallback telemetry from Supabase should match the coordinator snapshot contract.

## Web Agent

- The website should consume public-safe telemetry from Supabase snapshots/history.
- Website telemetry contract details should stay aligned with `skills/telemetry-coordinator/reference/telemetry-pipeline-plan.md` and Web's technical architecture.
- Public website monitoring is read-only unless a separate approved command path exists.

## Content Agent

- Hardware downtime, rewire sessions, visible failures, rain events, wave/tide behavior, and sensor changes can affect filming and story planning.
- Coordinate before scheduling content that depends on biomes 2-5 during the planned sensor/controller rewire.
- The six public system names in `systems/00-index.md` must stay aligned with website/App/Brain system records.

## Research / Ecosystem

- Hardware observations about climate, rain, hydrology, closure, and sensor failures can affect ecological interpretation.
- Do not turn hardware readings into ecological conclusions without the right Research/Ecosystem context.

## Supabase

- Supabase is canonical for structured telemetry records once tables are implemented.
- Schema changes and command queue writes require explicit approval.
- Do not use Supabase as a scratchpad for testing return values.
