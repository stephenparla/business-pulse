# app/models/invoice.py

import uuid
from datetime import date
from decimal import Decimal
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "invoice_number",
            name="uq_organization_invoice_number"
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

    customer_id: uuid.UUID = Field(
        foreign_key="customers.id",
        index=True
    )

    order_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="orders.id",
        index=True
    )

    invoice_number: str = Field(max_length=50)
    
    invoice_date: date = Field(
        default_factory=date.today
    )
    
    due_date: date

    status: str = Field(default="draft")
    
    subtotal: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=14,
        decimal_places=2
    )
    
    tax_amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=14,
        decimal_places=2
    )
    
    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=14,
        decimal_places=2
    )
    
    currency_code: str = Field(max_length=3)
