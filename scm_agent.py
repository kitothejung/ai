from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from compute.scm_metrics import (
    sales_amount_for_date,
    weekly_demand_units,
    weekly_metrics,
    weekly_sales_amount,
    weekly_supply_units,
)


DEFAULT_CSV = "data/retail_store_sales_promotions_demand.csv"
DEFAULT_MODEL = "gpt-4o-mini"
API_URL = "https://api.openai.com/v1/responses"


def _load_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("openai_key")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return key


def _build_tools(csv_path: str) -> dict[str, callable]:
    return {
        "sales_amount_for_date": lambda date: _sales_amount_for_date_payload(csv_path, date),
        "weekly_sales_amount": lambda: weekly_sales_amount(csv_path),
        "weekly_demand_units": lambda: weekly_demand_units(csv_path),
        "weekly_supply_units": lambda: weekly_supply_units(csv_path),
        "weekly_metrics": lambda: [
            {
                "week_start": row.week_start,
                "sales_amount": round(row.sales_amount, 2),
                "demand_units": round(row.demand_units, 2),
                "supply_units": round(row.supply_units, 2),
            }
            for row in weekly_metrics(csv_path)
        ],
    }


def _sales_amount_for_date_payload(csv_path: str, date: str) -> dict[str, object]:
    rows, total = sales_amount_for_date(csv_path, date)
    return {
        "date": date,
        "rows": rows,
        "sales_amount": round(total, 2),
    }


def _response_schema() -> list[dict[str, object]]:
    return [
        {
            "type": "function",
            "name": "sales_amount_for_date",
            "description": "Get sales amount total for a specific date from the CSV.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format",
                    }
                },
                "required": ["date"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "weekly_metrics",
            "description": "Get weekly sales amount, demand, and supply totals.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "type": "function",
            "name": "weekly_sales_amount",
            "description": "Get weekly sales amount totals.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "type": "function",
            "name": "weekly_demand_units",
            "description": "Get weekly demand totals.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "type": "function",
            "name": "weekly_supply_units",
            "description": "Get weekly supply totals.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    ]


def _post_response(payload: dict) -> dict:
    api_key = _load_api_key()
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {detail}") from exc


def _extract_text(response: dict) -> str:
    texts: list[str] = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    texts.append(content.get("text", ""))
    return "\n".join(texts).strip()


def _collect_function_calls(response: dict) -> list[dict]:
    calls = []
    for item in response.get("output", []):
        if item.get("type") == "function_call":
            calls.append(item)
    return calls


def _call_tool(tool_name: str, arguments: dict, tool_handlers: dict[str, callable]) -> object:
    handler = tool_handlers.get(tool_name)
    if handler is None:
        raise RuntimeError(f"Unknown tool: {tool_name}")
    if tool_name == "sales_amount_for_date":
        return handler(arguments["date"])
    return handler()


def _ask_agent(csv_path: str, model: str, user_input: str) -> str:
    tool_handlers = _build_tools(csv_path)
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are an SCM analysis agent. "
                            "Use tools for any data lookup or calculation. "
                            "Answer in Korean by default unless the user asks otherwise. "
                            "Keep responses short, factual, and table-first. "
                            "Always format metric answers as a markdown table unless the user asks for JSON. "
                            "For date-level sales amount requests, return a one-row table with date, rows, and sales_amount. "
                            "For weekly questions, return a table with week_start, sales_amount, demand_units, and supply_units. "
                            "If the user asks for a date-level sales amount, use sales_amount_for_date. "
                            "If the user asks for weekly sales, demand, supply, or summary, use the weekly tools. "
                            "If the request is ambiguous, ask one clarifying question."
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_input}],
            },
        ],
        "tools": _response_schema(),
    }

    response = _post_response(payload)

    while True:
        calls = _collect_function_calls(response)
        if not calls:
            text = _extract_text(response)
            if text:
                return text
            raise RuntimeError("No assistant text returned from the model.")

        tool_outputs = []
        for call in calls:
            arguments = json.loads(call.get("arguments") or "{}")
            result = _call_tool(call["name"], arguments, tool_handlers)
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call["call_id"],
                    "output": json.dumps(result, ensure_ascii=False),
                }
            )

        response = _post_response(
            {
                "model": model,
                "previous_response_id": response["id"],
                "input": tool_outputs,
            }
        )


def _interactive_shell(csv_path: str, model: str) -> None:
    print(f"SCM agent ready with model: {model}")
    print("Ask in natural language, for example:")
    print("  - 2024-12-23 일 판매금액 합산해줘")
    print("  - 주간 요약 보여줘")
    print("  - exit")

    while True:
        try:
            query = input("scm> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break

        try:
            answer = _ask_agent(csv_path, model, query)
            print(answer.strip())
        except Exception as exc:
            print(f"Error: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SCM analysis agent")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=DEFAULT_CSV,
        help="Path to the SCM CSV file",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="OpenAI model name",
    )
    args = parser.parse_args()

    csv_path = str(Path(args.csv_path))
    _interactive_shell(csv_path, args.model)


if __name__ == "__main__":
    main()

