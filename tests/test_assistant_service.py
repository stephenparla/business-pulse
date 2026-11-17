from __future__ import annotations

from app.ai.assistant_service import ask_business_question


def test_ask_business_question_handles_tool_use_round(monkeypatch):
    call_count = {"value": 0}

    def fake_invoke_model(messages, system_prompt, tool_config):
        call_count["value"] += 1
        if call_count["value"] == 1:
            return {
                "stopReason": "tool_use",
                "output": {
                    "message": {
                        "content": [
                            {
                                "toolUse": {
                                    "toolUseId": "tool-123",
                                    "name": "get_top_customers",
                                    "input": {
                                        "period_start": "2026-10-01",
                                        "period_end": "2026-10-31",
                                        "limit": 5,
                                    },
                                }
                            }
                        ]
                    }
                },
            }

        return {
            "stopReason": "end_turn",
            "output": {
                "message": {
                    "content": [
                        {
                            "text": "Your top five customers generated $125,000 in invoiced sales."
                        }
                    ]
                }
            },
        }

    monkeypatch.setattr("app.ai.assistant_service.invoke_model", fake_invoke_model)

    def fake_tool_functions():
        return {
            "get_top_customers": lambda **kwargs: {
                "items": [
                    {
                        "customer_name": "Apex Retail",
                        "total_revenue": 125000,
                    }
                ],
                "count": 1,
            }
        }

    monkeypatch.setattr("app.ai.assistant_service._get_tool_functions", fake_tool_functions)

    result = ask_business_question("Who are my top five customers this month?")

    assert result["question"] == "Who are my top five customers this month?"
    assert "125,000" in result["answer"]
    assert result["status"] == "COMPLETED"
    assert "get_top_customers" in result["tools_used"]
    assert result["data_source"] == "PostgreSQL"
