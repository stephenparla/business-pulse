import os


class Settings:
    BEDROCK_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID",
        "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    )


settings = Settings()
