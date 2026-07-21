# Token Efficiency

This file records the operating rule for large CSV analysis.

## Principle

- Do not pass full large CSV data into the LLM when the metric can be computed locally first.
- Prefer deterministic code for grouping, filtering, aggregation, and formatting.
- Give the LLM only the compact result table or exceptions that need interpretation.

## Good Division of Work

- Code: parse rows, aggregate metrics, validate columns, and create compact summaries.
- LLM: interpret the result, explain anomalies, and turn metrics into narrative output.

## Why This Matters

- Reduces token usage.
- Improves speed.
- Reduces numeric mistakes.
- Makes the pipeline easier to reuse for multiple questions.

