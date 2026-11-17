from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ValidationError

from app.ai.bedrock_client import invoke_model
from app.ai.tool_registry import TOOLS

DEFAULT_SYSTEM_PROMPT = (
    "You are Business Pulse, an AI business intelligence assistant.\n\n"
    "Your responsibility is to answer questions using verified business information.\n\n"
    "Rules:\n"
    "1. Use available tools to retrieve business metrics.\n"
    "2. Never invent financial or operational figures.\n"
    "3. Do not generate or execute SQL.\n"
    "4. Use only the tools provided to you.\n"
    "5. Clearly distinguish actual data from estimates.\n"
    "6. Explain the period covered by the data.\n"
    "7. If data is unavailable, say so.\n"
    "8. Never modify business records.\n"
    "9. Provide concise, business-friendly explanations.\n"
    "10. Never claim a recommendation was executed."
)

ALLOWED_TOOLS: dict[str, Any] = {
    tool["toolSpec"]["name"]: tool["toolSpec"] for tool in TOOLS
}


class RevenueSummaryArgs(BaseModel):
    period_start: str
    period_end: str


class OrderSummaryArgs(BaseModel):
    period_start: str
    period_end: str


class TopCustomersArgs(BaseModel):
    period_start: str
    period_end: str
    limit: int = Field(default=5, ge=1)


class ReceivablesArgs(BaseModel):
    pass


VALIDATION_MODELS: dict[str, type[BaseModel]] = {
    "get_revenue_summary": RevenueSummaryArgs,
    "get_order_summary": OrderSummaryArgs,
    "get_top_customers": TopCustomersArgs,
    "get_receivables": ReceivablesArgs,
}

def _get_tool_functions() -> dict[str, Any]:
    from app.repositories.business_repository import (
        get_order_summary,
        get_receivables,
        get_revenue_summary,
        get_top_customers,
    )

    return {
        "get_revenue_summary": get_revenue_summary,
        "get_order_summary": get_order_summary,
        "get_top_customers": get_top_customers,
        "get_receivables": get_receivables,
    }


def _extract_text_from_content(content: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for block in content:
        if "text" in block:
            blocks.append(str(block["text"]))
    return "\n".join(blocks).strip()


def _extract_tool_uses(content: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tool_uses: list[dict[str, Any]] = []
    for block in content:
        if "toolUse" in block:
            tool_uses.append(block["toolUse"])
    return tool_uses


def _execute_tool(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    if tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not in the allowlist.")

    model_cls = VALIDATION_MODELS.get(tool_name)
    if model_cls is None:
        raise ValueError(f"No validation model defined for tool '{tool_name}'.")

    validated = model_cls.model_validate(tool_input)
    tool_functions = _get_tool_functions()
    result = tool_functions[tool_name](**validated.model_dump())
    return result


def ask_business_question(
    question: str,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    max_tool_rounds: int = 3,
) -> dict[str, Any]:
    """Send a user question to Bedrock with tool calling and a bounded tool loop."""
    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": [{"text": question}],
        }
    ]
    tools_used: list[str] = []

    for _ in range(max_tool_rounds):
        response = invoke_model(
            messages=messages,
            system_prompt=system_prompt,
            tool_config={"tools": TOOLS},
        )

        stop_reason = response.get("stopReason")
        output = response.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])

        tool_uses = _extract_tool_uses(content)
        if stop_reason != "tool_use" or not tool_uses:
            final_answer = _extract_text_from_content(content)
            return {
                "question": question,
                "answer": final_answer,
                "tools_used": tools_used,
                "data_source": "PostgreSQL",
                "status": "COMPLETED",
            }

        tool_results: list[dict[str, Any]] = []
        for tool_use in tool_uses:
            tool_name = tool_use.get("name")
            tool_use_id = tool_use.get("toolUseId")
            tool_input = tool_use.get("input", {})

            if not tool_name or not tool_use_id:
                continue

            if tool_name not in ALLOWED_TOOLS:
                raise ValueError(f"Tool '{tool_name}' is not allowed.")

            try:
                validated_input = VALIDATION_MODELS[tool_name].model_validate(tool_input)
                tool_functions = _get_tool_functions()
                tool_output = tool_functions[tool_name](**validated_input.model_dump())
            except ValidationError as exc:
                tool_output = {
                    "error": "Invalid tool arguments",
                    "details": exc.errors(),
                }

            tools_used.append(tool_name)
            tool_results.append(
                {
                    "toolResult": {
                        "toolUseId": tool_use_id,
                        "content": [{"json": tool_output}],
                        "status": "SUCCESS",
                    }
                }
            )

        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": tool_results})

    return {
        "question": question,
        "answer": "The assistant reached the configured tool-call limit without a final answer.",
        "tools_used": tools_used,
        "data_source": "PostgreSQL",
        "status": "MAX_TOOL_ROUNDS_REACHED",
    }
