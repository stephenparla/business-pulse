from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.order import Order
from app.models.payment_allocation import PaymentAllocation
from app.schemas.business import (
    OrderSummaryResponse,
    OutstandingReceivableResponse,
    RevenueSummaryResponse,
    TopCustomerResponse,
)


async def get_revenue_summary(db: AsyncSession, organization_id: UUID) -> RevenueSummaryResponse:
    invoices = (
        await db.execute(select(Invoice).where(Invoice.organization_id == organization_id))
    ).scalars().all()

    total_revenue = sum(
        (invoice.total_amount for invoice in invoices if invoice.status != "draft"),
        Decimal("0.00"),
    )
    outstanding_revenue = Decimal("0.00")
    paid_revenue = Decimal("0.00")

    for invoice in invoices:
        allocations = (
            await db.execute(
                select(func.coalesce(func.sum(PaymentAllocation.allocated_amount), Decimal("0.00"))).where(
                    PaymentAllocation.invoice_id == invoice.id
                )
            )
        ).scalar() or Decimal("0.00")
        paid_so_far = min(allocations, invoice.total_amount)
        outstanding_amount = max(invoice.total_amount - paid_so_far, Decimal("0.00"))
        paid_revenue += paid_so_far
        outstanding_revenue += outstanding_amount

    return RevenueSummaryResponse(
        organization_id=organization_id,
        total_revenue=total_revenue,
        paid_revenue=paid_revenue,
        outstanding_revenue=outstanding_revenue,
        invoice_count=len(invoices),
    )


async def get_order_summary(db: AsyncSession, organization_id: UUID) -> OrderSummaryResponse:
    orders = (
        await db.execute(select(Order).where(Order.organization_id == organization_id))
    ).scalars().all()

    total_orders = len(orders)
    completed_orders = sum(1 for order in orders if order.status.lower() == "completed")
    pending_orders = sum(1 for order in orders if order.status.lower() == "pending")
    cancelled_orders = sum(1 for order in orders if order.status.lower() == "cancelled")
    total_order_value = sum((order.total_amount for order in orders), Decimal("0.00"))
    average_order_value = (
        (total_order_value / Decimal(total_orders)) if total_orders else Decimal("0.00")
    )

    return OrderSummaryResponse(
        organization_id=organization_id,
        total_orders=total_orders,
        completed_orders=completed_orders,
        pending_orders=pending_orders,
        cancelled_orders=cancelled_orders,
        total_order_value=total_order_value,
        average_order_value=average_order_value,
    )


async def get_top_customers(db: AsyncSession, organization_id: UUID) -> list[TopCustomerResponse]:
    customers = (
        await db.execute(select(Customer).where(Customer.organization_id == organization_id))
    ).scalars().all()

    summary: list[TopCustomerResponse] = []
    for customer in customers:
        orders = (
            await db.execute(select(Order).where(Order.customer_id == customer.id))
        ).scalars().all()
        invoices = (
            await db.execute(select(Invoice).where(Invoice.customer_id == customer.id))
        ).scalars().all()

        total_revenue = sum(
            (invoice.total_amount for invoice in invoices if invoice.status != "draft"),
            Decimal("0.00"),
        )
        summary.append(
            TopCustomerResponse(
                customer_id=customer.id,
                customer_code=customer.customer_code,
                customer_name=customer.name,
                total_revenue=total_revenue,
                order_count=len(orders),
            )
        )

    return sorted(summary, key=lambda item: item.total_revenue, reverse=True)[:10]


async def get_outstanding_receivables(db: AsyncSession, organization_id: UUID) -> list[OutstandingReceivableResponse]:
    customers = (
        await db.execute(select(Customer).where(Customer.organization_id == organization_id))
    ).scalars().all()

    items: list[OutstandingReceivableResponse] = []
    for customer in customers:
        invoices = (
            await db.execute(select(Invoice).where(Invoice.customer_id == customer.id))
        ).scalars().all()

        outstanding_total = Decimal("0.00")
        invoice_count = 0
        for invoice in invoices:
            if invoice.status not in {"open", "overdue", "partially_paid"}:
                continue
            allocations = (
                await db.execute(
                    select(func.coalesce(func.sum(PaymentAllocation.allocated_amount), Decimal("0.00"))).where(
                        PaymentAllocation.invoice_id == invoice.id
                    )
                )
            ).scalar() or Decimal("0.00")
            outstanding_total += max(invoice.total_amount - allocations, Decimal("0.00"))
            invoice_count += 1

        if outstanding_total > Decimal("0.00"):
            items.append(
                OutstandingReceivableResponse(
                    customer_id=customer.id,
                    customer_code=customer.customer_code,
                    customer_name=customer.name,
                    outstanding_amount=outstanding_total,
                    invoice_count=invoice_count,
                )
            )

    return sorted(items, key=lambda item: item.outstanding_amount, reverse=True)
