# app/models/order_item.py

import uuid
from decimal import Decimal
from sqlmodel import SQLModel, Field


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    order_id: uuid.UUID = Field(
        foreign_key="orders.id",
        index=True
    )

    product_code: str = Field(max_length=50)
    product_name: str = Field(max_length=200)
    
    quantity: Decimal = Field(
        max_digits=12,
        decimal_places=3
    )
    
    unit_price: Decimal = Field(
        max_digits=14,
        decimal_places=2
    )
    
    line_total: Decimal = Field(
        max_digits=14,
        decimal_places=2
    )
