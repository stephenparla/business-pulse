
# app/models/organization.py

import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    name: str = Field(max_length=200)

    industry: str | None = Field(
        default=None,
        max_length=100
    )

    default_currency: str = Field(
        default="USD",
        max_length=3
    )

    timezone: str = Field(
        default="America/New_York",
        max_length=100
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
