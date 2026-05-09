# Tanks And Cabinets

## Biome Tanks

Six 29-gallon biome tanks form the main ecological sequence:

1. Freshwater Lake
2. Lakeshore
3. Lowland Meadow
4. Mangrove Forest
5. Marine Shore
6. Seagrass Meadow

## Atmosphere Tanks

Four vertically mounted 29-gallon atmosphere tanks sit above:

- Lakeshore.
- Lowland Meadow.
- Mangrove Forest.
- Marine Shore.

Freshwater Lake and Seagrass Meadow route humid air into adjacent atmosphere processors rather than having their own atmosphere tanks in the current deployment.

## Cabinet And Elevation Logic

Each biome tank is supported by a custom plywood cabinet with enclosed front doors. Cabinet heights create intentional vertical staggering:

```text
Freshwater Lake < Lakeshore < Lowland Meadow = Mangrove Forest > Marine Shore > Seagrass Meadow
```

This elevation staging supports surface water continuity, convection-driven airflow, terrain gradient, and hydrological flow logic.

