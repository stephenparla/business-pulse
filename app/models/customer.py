
# app/models/customer.py

import uuid
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "customer_code",
            name="uq_customer_org_code"
        ),
    )

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        index=True
    )

    customer_code: str = Field(max_length=50)

    name: str = Field(max_length=200)

    email: str | None = Field(
        default=None,
        max_length=255
    )

    status: str = Field(default="ACTIVE")
