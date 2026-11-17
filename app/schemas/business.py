from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class RevenueSummaryResponse(BaseModel):
    organization_id: UUID
    total_revenue: Decimal = Field(default=Decimal("0.00"))
    paid_revenue: Decimal = Field(default=Decimal("0.00"))
    outstanding_revenue: Decimal = Field(default=Decimal("0.00"))
    invoice_count: int = 0


class OrderSummaryResponse(BaseModel):
    organization_id: UUID
    total_orders: int = 0
    completed_orders: int = 0
    pending_orders: int = 0
    cancelled_orders: int = 0
    total_order_value: Decimal = Field(default=Decimal("0.00"))
    average_order_value: Decimal = Field(default=Decimal("0.00"))


class TopCustomerResponse(BaseModel):
    customer_id: UUID
    customer_code: str
    customer_name: str
    total_revenue: Decimal = Field(default=Decimal("0.00"))
    order_count: int = 0


class OutstandingReceivableResponse(BaseModel):
    customer_id: UUID
    customer_code: str
    customer_name: str
    outstanding_amount: Decimal = Field(default=Decimal("0.00"))
    invoice_count: int = 0
