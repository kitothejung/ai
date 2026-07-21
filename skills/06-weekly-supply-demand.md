# Weekly Supply and Demand

Use this skill to estimate weekly supply and demand from SCM CSV data.

## Working Definitions

- Demand = sum of `units_sold` grouped by week.
- Supply = sum of `inventory_level` grouped by week, or a proxy derived from available stock if the user requests a different interpretation.

## Steps

1. Load the CSV file.
2. Parse `date`.
3. Group records by week.
4. Sum `units_sold` as weekly demand.
5. Sum `inventory_level` as weekly supply proxy.
6. Report both values side by side and include the supply-demand gap.

## Caveat

- This dataset does not appear to contain an explicit procurement or inbound supply field, so `inventory_level` is used as the practical proxy unless the user defines supply differently.

