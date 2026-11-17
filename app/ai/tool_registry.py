"""Registry of AI tool specifications exposed to the assistant."""

TOOLS = [
    {
        "toolSpec": {
            "name": "get_revenue_summary",
            "description": (
                "Returns actual invoiced sales for a specified date range."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "period_start": {
                            "type": "string",
                            "description": "Start date YYYY-MM-DD",
                        },
                        "period_end": {
                            "type": "string",
                            "description": "End date YYYY-MM-DD",
                        },
                    },
                    "required": ["period_start", "period_end"],
                    "additionalProperties": False,
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "get_order_summary",
            "description": (
                "Returns order counts and status breakdown for a specified date range."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "period_start": {
                            "type": "string",
                            "description": "Start date YYYY-MM-DD",
                        },
                        "period_end": {
                            "type": "string",
                            "description": "End date YYYY-MM-DD",
                        },
                    },
                    "required": ["period_start", "period_end"],
                    "additionalProperties": False,
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "get_top_customers",
            "description": (
                "Returns customers ranked by invoiced sales for a specified date range."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "period_start": {
                            "type": "string",
                            "description": "Start date YYYY-MM-DD",
                        },
                        "period_end": {
                            "type": "string",
                            "description": "End date YYYY-MM-DD",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of customers to return.",
                            "default": 5,
                        },
                    },
                    "required": ["period_start", "period_end"],
                    "additionalProperties": False,
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "get_receivables",
            "description": (
                "Returns outstanding and overdue receivables for the current organization."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                }
            },
        }
    },
]
