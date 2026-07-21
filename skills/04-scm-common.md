# SCM Common Analysis

This skill defines the common workflow for SCM analysis over CSV files in `data/`.

## Input

- Read CSV files from `data/`.
- Prefer a single source file unless the user requests multiple files.
- Use the columns present in the dataset, especially `date`, `price`, `units_sold`, `inventory_level`, and `promotion_active`.

## Shared Assumptions

- `date` is the reporting date.
- `price` is the unit price.
- `units_sold` is the daily or record-level sold quantity.
- `inventory_level` is the available stock level at the time of record.
- `promotion_active` indicates whether a promotion was active for that record.

## General Workflow

1. Load the CSV.
2. Validate required columns.
3. Convert `date` to a date type.
4. Group by week when the user asks for weekly metrics.
5. Return concise metric summaries and any notable anomalies.
6. Prefer local computation for aggregation instead of sending raw rows to the LLM.

## Compute Boundary

- Use deterministic code for parsing, aggregation, and table generation.
- Use the LLM only for interpretation, summarization, and user-facing explanation.

## Operational Principle

- Large CSV inputs should be reduced locally before prompting the LLM.
