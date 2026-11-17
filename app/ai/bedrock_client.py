import boto3

from app.core.config import settings

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=settings.BEDROCK_REGION,
)


def get_model_id() -> str:
    return settings.BEDROCK_MODEL_ID


def invoke_model(messages: list[dict], system_prompt: str, tool_config: dict) -> dict:
    model_id = get_model_id()
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompt,
        toolConfig=tool_config,
    )
    return response
