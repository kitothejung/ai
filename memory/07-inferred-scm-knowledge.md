# Inferred SCM Knowledge

This file records assumptions inferred from `data/retail_store_sales_promotions_demand.csv`.

## Observed Columns

- `store_id`
- `product_id`
- `date`
- `category`
- `price`
- `promotion_active`
- `discount_percent`
- `units_sold`
- `inventory_level`
- `day_of_week`

## Inferred Meanings

- `date` is the analysis date.
- `price` is a unit price.
- `units_sold` is the sold quantity for the record.
- `inventory_level` is the stock level available for the record.
- `promotion_active` indicates whether a promotion was running.
- `discount_percent` is the applied discount rate.

## Analytical Conventions

- Weekly sales amount should be calculated as `price * units_sold`.
- Weekly demand should be calculated as summed `units_sold`.
- Weekly supply should be approximated from `inventory_level` unless a more explicit supply field is introduced later.

