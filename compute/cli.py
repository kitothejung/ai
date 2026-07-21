from __future__ import annotations

import argparse
import json
from pathlib import Path

from compute.scm_metrics import (
    format_weekly_report,
    rows_to_dicts,
    weekly_demand_units,
    weekly_metrics,
    weekly_sales_amount,
    weekly_supply_units,
    write_report,
)


DEFAULT_CSV = "data/retail_store_sales_promotions_demand.csv"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _default_output(stem: str, suffix: str) -> Path:
    return PROJECT_ROOT / "outputs" / f"{stem}.{suffix}"


def main() -> None:
    parser = argparse.ArgumentParser(description="SCM analysis compute CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("weekly-sales", "weekly-demand", "weekly-supply", "weekly-all"):
        cmd = subparsers.add_parser(name)
        cmd.add_argument("csv_path", nargs="?", default=DEFAULT_CSV)
        cmd.add_argument("--json", action="store_true", help="Print JSON output")
        cmd.add_argument("--save", action="store_true", help="Save output to outputs/")

    args = parser.parse_args()
    csv_path = Path(args.csv_path)

    if args.command == "weekly-sales":
        result = weekly_sales_amount(csv_path)
        payload = [{"week_start": k, "sales_amount": round(v, 2)} for k, v in sorted(result.items())]
        default_file = _default_output(csv_path.stem + "-weekly-sales", "json")
    elif args.command == "weekly-demand":
        result = weekly_demand_units(csv_path)
        payload = [{"week_start": k, "demand_units": round(v, 2)} for k, v in sorted(result.items())]
        default_file = _default_output(csv_path.stem + "-weekly-demand", "json")
    elif args.command == "weekly-supply":
        result = weekly_supply_units(csv_path)
        payload = [{"week_start": k, "supply_units": round(v, 2)} for k, v in sorted(result.items())]
        default_file = _default_output(csv_path.stem + "-weekly-supply", "json")
    else:
        rows = weekly_metrics(csv_path)
        payload = rows_to_dicts(rows)
        default_file = _default_output(csv_path.stem + "-weekly-all", "json")

    if args.save:
        if args.command == "weekly-all":
            write_report(weekly_metrics(csv_path), default_file)
        else:
            default_file.parent.mkdir(parents=True, exist_ok=True)
            with default_file.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        print(default_file.as_posix(), flush=True)
        return

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "weekly-all":
        print(format_weekly_report(weekly_metrics(csv_path)))
        return

    for row in payload:
        print(row)
