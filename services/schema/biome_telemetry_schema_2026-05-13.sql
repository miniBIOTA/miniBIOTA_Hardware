-- miniBIOTA internal biome telemetry history
-- Date: 2026-05-13
-- Status: Applied successfully in Supabase SQL Editor on 2026-05-13; retained as Hardware schema reference.
-- Purpose: store per-biome time-series telemetry for control-system analysis.
--
-- Producer:
-- - Hardware/Wyse telemetry coordinator inserts/upserts one row per active sensor biome per history interval.
--
-- Consumer:
-- - Internal analysis/operator tooling.
-- - Not required by the public website current-state telemetry surface.
--
-- Boundary:
-- - This table is internal history for analysis and programming decisions.
-- - Do not expose pump percentage or liquid/heat-exchanger temperature publicly without a separate Web contract decision.
-- - Do not add command queues, relay control, actuator control, or MQTT publishing here.

create table if not exists public.biome_telemetry (
  id bigserial primary key,
  biome_id integer not null references public.biomes(id) on update cascade on delete restrict,
  recorded_at timestamptz not null,
  inserted_at timestamptz not null default now(),
  bio_temp_c double precision,
  bio_humidity_pct double precision,
  atmo_temp_c double precision,
  atmo_humidity_pct double precision,
  liquid_temp_c double precision,
  pump_pct double precision,
  target_temp_c double precision,
  constraint biome_telemetry_unique_biome_recorded_at unique (biome_id, recorded_at),
  constraint biome_telemetry_bio_humidity_pct_range check (
    bio_humidity_pct is null or (bio_humidity_pct >= 0 and bio_humidity_pct <= 100)
  ),
  constraint biome_telemetry_atmo_humidity_pct_range check (
    atmo_humidity_pct is null or (atmo_humidity_pct >= 0 and atmo_humidity_pct <= 100)
  ),
  constraint biome_telemetry_pump_pct_range check (
    pump_pct is null or (pump_pct >= 0 and pump_pct <= 100)
  )
);

comment on table public.biome_telemetry is
  'Internal miniBIOTA per-biome telemetry history for analysis of climate behavior, heat exchanger temperature, pump run percentage, and sensor readings.';

comment on column public.biome_telemetry.biome_id is
  'miniBIOTA biome id, matching Hardware project folder numbers and public biomes.';

comment on column public.biome_telemetry.recorded_at is
  'UTC timestamp when the ESP32 telemetry packet was received by the Wyse coordinator.';

comment on column public.biome_telemetry.inserted_at is
  'UTC timestamp when Supabase stored or last upserted this history row.';

comment on column public.biome_telemetry.bio_temp_c is
  'Biome air temperature from the biome-side sensor channel, in Celsius.';

comment on column public.biome_telemetry.bio_humidity_pct is
  'Biome air humidity from the biome-side sensor channel, as percent relative humidity.';

comment on column public.biome_telemetry.atmo_temp_c is
  'Atmosphere air temperature from the atmosphere-side sensor channel, in Celsius.';

comment on column public.biome_telemetry.atmo_humidity_pct is
  'Atmosphere air humidity from the atmosphere-side sensor channel, as percent relative humidity.';

comment on column public.biome_telemetry.liquid_temp_c is
  'Liquid/heat-exchanger temperature from the climate loop sensor channel, in Celsius.';

comment on column public.biome_telemetry.pump_pct is
  'Pump run percentage reported by firmware for internal control-system analysis.';

comment on column public.biome_telemetry.target_temp_c is
  'Read-only target temperature value reported by firmware when known; firmware placeholder 0.0 is stored as null by the coordinator.';

create index if not exists biome_telemetry_biome_recorded_at_desc_idx
  on public.biome_telemetry (biome_id, recorded_at desc);

create index if not exists biome_telemetry_recorded_at_desc_idx
  on public.biome_telemetry (recorded_at desc);

alter table public.biome_telemetry enable row level security;
