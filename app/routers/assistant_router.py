from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.ai.assistant_service import ask_business_question

router = APIRouter(tags=["Assistant"])


@router.post("/assistant/ask")
async def ask_assistant(payload: dict[str, Any]) -> dict[str, Any]:
    """Ask the assistant a business question with Bedrock tool use enabled."""
    question = payload.get("question")
    if not question or not str(question).strip():
        raise HTTPException(status_code=400, detail="Question is required.")

    system_prompt = payload.get("system_prompt")
    max_tool_rounds = payload.get("max_tool_rounds", 3)

    return ask_business_question(
        question=str(question),
        system_prompt=str(system_prompt) if system_prompt else None,
        max_tool_rounds=int(max_tool_rounds),
    )
