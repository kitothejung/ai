from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = {
    "date",
    "price",
    "units_sold",
    "inventory_level",
    "promotion_active",
}


@dataclass(frozen=True)
class WeeklyMetricRow:
    week_start: str
    sales_amount: float
    demand_units: float
    supply_units: float


def _parse_float(value: str | None) -> float:
    if value is None or value == "":
        return 0.0
    return float(value)


def _week_start(date_text: str) -> str:
    dt = datetime.strptime(date_text, "%Y-%m-%d").date()
    start = dt.fromordinal(dt.toordinal() - dt.weekday())
    return start.isoformat()


def validate_columns(fieldnames: Iterable[str]) -> None:
    present = set(fieldnames)
    missing = REQUIRED_COLUMNS - present
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def weekly_metrics(csv_path: str | Path) -> list[WeeklyMetricRow]:
    sales_amounts = weekly_sales_amount(csv_path)
    demand_by_week = weekly_demand_units(csv_path)
    supply_by_week = weekly_supply_units(csv_path)

    weeks = sorted(set(sales_amounts) | set(demand_by_week) | set(supply_by_week))
    return [
        WeeklyMetricRow(
            week_start=week,
            sales_amount=sales_amounts.get(week, 0.0),
            demand_units=demand_by_week.get(week, 0.0),
            supply_units=supply_by_week.get(week, 0.0),
        )
        for week in weeks
    ]


def weekly_sales_amount(csv_path: str | Path) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)

    with Path(csv_path).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        validate_columns(reader.fieldnames or [])

        for row in reader:
            week = _week_start(row["date"])
            price = _parse_float(row.get("price"))
            units_sold = _parse_float(row.get("units_sold"))
            totals[week] += price * units_sold

    return dict(totals)


def sales_amount_for_date(csv_path: str | Path, target_date: str) -> tuple[int, float]:
    total = 0.0
    row_count = 0

    with Path(csv_path).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        validate_columns(reader.fieldnames or [])

        for row in reader:
            if row.get("date") != target_date:
                continue
            row_count += 1
            price = _parse_float(row.get("price"))
            units_sold = _parse_float(row.get("units_sold"))
            total += price * units_sold

    return row_count, total


def weekly_demand_units(csv_path: str | Path) -> dict[str, float]:
    demand: dict[str, float] = defaultdict(float)

    with Path(csv_path).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        validate_columns(reader.fieldnames or [])

        for row in reader:
            week = _week_start(row["date"])
            demand[week] += _parse_float(row.get("units_sold"))

    return dict(demand)


def weekly_supply_units(csv_path: str | Path) -> dict[str, float]:
    supply: dict[str, float] = defaultdict(float)

    with Path(csv_path).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        validate_columns(reader.fieldnames or [])

        for row in reader:
            week = _week_start(row["date"])
            supply[week] += _parse_float(row.get("inventory_level"))

    return dict(supply)


def format_weekly_report(rows: list[WeeklyMetricRow]) -> str:
    lines = ["week_start,sales_amount,demand_units,supply_units"]
    for row in rows:
        lines.append(
            f"{row.week_start},{row.sales_amount:.2f},{row.demand_units:.2f},{row.supply_units:.2f}"
        )
    return "\n".join(lines)


def rows_to_dicts(rows: list[WeeklyMetricRow]) -> list[dict[str, float | str]]:
    return [
        {
            "week_start": row.week_start,
            "sales_amount": round(row.sales_amount, 2),
            "demand_units": round(row.demand_units, 2),
            "supply_units": round(row.supply_units, 2),
        }
        for row in rows
    ]


def write_report(rows: list[WeeklyMetricRow], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        json.dump(rows_to_dicts(rows), f, ensure_ascii=False, indent=2)
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute weekly SCM metrics from CSV")
    parser.add_argument("csv_path", help="Path to the source CSV file")
    args = parser.parse_args()

    print(format_weekly_report(weekly_metrics(args.csv_path)))
