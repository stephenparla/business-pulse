from __future__ import annotations

from typing import Any


def get_tool_definitions() -> list[dict[str, Any]]:
    """Return the tool definitions exposed to the AI assistant."""
    return [
        {
            "name": "get_revenue_summary",
            "description": "Retrieve actual revenue metrics for a reporting period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period_start": {"type": "string"},
                    "period_end": {"type": "string"},
                },
                "required": ["period_start", "period_end"],
            },
        },
        {
            "name": "get_order_summary",
            "description": "Retrieve order counts and status breakdown for a reporting period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period_start": {"type": "string"},
                    "period_end": {"type": "string"},
                },
                "required": ["period_start", "period_end"],
            },
        },
        {
            "name": "get_top_customers",
            "description": "Retrieve customers ranked by invoiced sales for a reporting period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period_start": {"type": "string"},
                    "period_end": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["period_start", "period_end"],
            },
        },
        {
            "name": "get_receivables",
            "description": "Retrieve outstanding and overdue receivables.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    ]
