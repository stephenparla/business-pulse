# app/models/payment.py

import uuid
from datetime import date
from decimal import Decimal
from sqlmodel import SQLModel, Field


class Payment(SQLModel, table=True) :
    __tablename__ = "payments"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        index=True
    )

    payment_reference: str = Field(max_length=100)
    
    payment_date: date = Field(
        default_factory=date.today
    )
    
    amount: Decimal = Field(
        max_digits=14,
        decimal_places=2
    )
    
    currency_code: str = Field(max_length=3)
