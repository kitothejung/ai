# Weekly Sales Amount Sum

Use this skill to calculate weekly sales amount totals from SCM CSV data.

## Definition

- Weekly sales amount = sum of `price * units_sold` grouped by week.
- If multiple stores or products are present, sum across all records in the week unless filtered otherwise.

## Steps

1. Load the CSV file.
2. Parse `date`.
3. Compute `sales_amount = price * units_sold` for each row.
4. Group by week.
5. Sum `sales_amount` for each week.
6. Report week start or ISO week number, total sales amount, and any large week-over-week changes.

## Notes

- If currency formatting is needed, keep the unit consistent with the source data.
- If `price` appears to be a unit price and not a total, keep the calculation above.

