# app/models/payment_allocation.py

import uuid
from decimal import Decimal
from sqlmodel import SQLModel, Field


class PaymentAllocation(SQLModel, table=True):
    __tablename__ = "payment_allocations"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    payment_id: uuid.UUID = Field(
        foreign_key="payments.id",
        index=True
    )

    invoice_id: uuid.UUID = Field(
        foreign_key="invoices.id",
        index=True
    )

    allocated_amount: Decimal = Field(
        max_digits=14,
        decimal_places=2
    )
