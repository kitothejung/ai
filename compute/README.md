# Compute Layer

This directory contains deterministic data-processing code used by the SCM agent.

## Purpose

- Read large CSV files without sending them to the LLM.
- Precompute weekly metrics.
- Return compact outputs that the LLM can summarize or explain.

## Current Module

- `scm_metrics.py` - weekly sales, demand, and supply aggregation.

## Usage Pattern

1. Run the compute layer on the CSV.
2. Pass only the compact result to the LLM.
3. Let the LLM explain or summarize the computed metrics.
