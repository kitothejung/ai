# SCM Agent Runner

This repository now includes a minimal executable entrypoint for the SCM analysis agent.

## Run

```bash
python scm_agent.py
```

If you run it with no arguments, it opens an interactive prompt.

## Examples

```bash
python scm_agent.py data/retail_store_sales_promotions_demand.csv
python scm_agent.py --format json
```

## What It Does

- Reads the CSV locally.
- Computes weekly sales amount, demand, and supply.
- Prints a compact report that an LLM can summarize if needed.
- Supports interactive date queries when started without arguments.
