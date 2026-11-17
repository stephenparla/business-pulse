from __future__ import annotations

import asyncio
import uuid
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import SessionLocal
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.order import Order
from app.models.organization import Organization
from app.models.payment import Payment
from app.models.payment_allocation import PaymentAllocation
from app.services.business_intelligence_service import (
    get_order_summary as get_order_summary_service,
    get_outstanding_receivables as get_outstanding_receivables_service,
    get_revenue_summary as get_revenue_summary_service,
    get_top_customers as get_top_customers_service,
)


def _money(value: str | Decimal) -> Decimal:
    return Decimal(value) if isinstance(value, str) else value


async def seed_fictional_business_data(db: AsyncSession) -> Organization:
    """Create a seed organization and sample customer data when the app starts empty."""
    existing_org = await db.scalar(
        select(Organization).where(Organization.name == "Northwind Operations")
    )
    if existing_org is not None:
        return existing_org

    organization = Organization(
        name="Northwind Operations",
        industry="Wholesale Distribution",
        default_currency="USD",
        timezone="America/New_York",
    )
    db.add(organization)
    await db.flush()

    customer_seed_data = [
        {
            "customer_code": "APEX-001",
            "name": "Apex Retail",
            "email": "billing@apexretail.io",
            "status": "ACTIVE",
        },
        {
            "customer_code": "SUMMIT-002",
            "name": "Summit Manufacturing",
            "email": "ops@summitmfg.co",
            "status": "ACTIVE",
        },
        {
            "customer_code": "HARBOR-003",
            "name": "Harbor Foods",
            "email": "acct@harborfoods.com",
            "status": "ACTIVE",
        },
        {
            "customer_code": "REDWOOD-004",
            "name": "Redwood Logistics",
            "email": "finance@redwoodlogistics.com",
            "status": "ACTIVE",
        },
    ]

    customers: list[Customer] = []
    for row in customer_seed_data:
        customer = Customer(
            organization_id=organization.id,
            customer_code=row["customer_code"],
            name=row["name"],
            email=row["email"],
            status=row["status"],
        )
        customers.append(customer)

    db.add_all(customers)
    await db.flush()

    seeded_orders = [
        {
            "customer_id": customers[0].id,
            "order_number": "PO-1001",
            "status": "completed",
            "subtotal": Decimal("900.00"),
            "tax_amount": Decimal("45.00"),
            "total_amount": Decimal("945.00"),
            "ordered_at": date.today() - timedelta(days=18),
        },
        {
            "customer_id": customers[1].id,
            "order_number": "PO-1002",
            "status": "completed",
            "subtotal": Decimal("1200.00"),
            "tax_amount": Decimal("60.00"),
            "total_amount": Decimal("1260.00"),
            "ordered_at": date.today() - timedelta(days=14),
        },
        {
            "customer_id": customers[2].id,
            "order_number": "PO-1003",
            "status": "pending",
            "subtotal": Decimal("500.00"),
            "tax_amount": Decimal("25.00"),
            "total_amount": Decimal("525.00"),
            "ordered_at": date.today() - timedelta(days=7),
        },
        {
            "customer_id": customers[3].id,
            "order_number": "PO-1004",
            "status": "completed",
            "subtotal": Decimal("1750.00"),
            "tax_amount": Decimal("87.50"),
            "total_amount": Decimal("1837.50"),
            "ordered_at": date.today() - timedelta(days=22),
        },
    ]

    orders = [
        Order(
            organization_id=organization.id,
            customer_id=row["customer_id"],
            order_number=row["order_number"],
            ordered_at=row["ordered_at"],
            status=row["status"],
            subtotal=row["subtotal"],
            tax_amount=row["tax_amount"],
            total_amount=row["total_amount"],
            currency_code="USD",
        )
        for row in seeded_orders
    ]
    db.add_all(orders)
    await db.flush()

    invoice_seed_data = [
        {
            "customer_id": customers[0].id,
            "order_id": orders[0].id,
            "invoice_number": "INV-2001",
            "due_date": date.today() + timedelta(days=10),
            "status": "paid",
            "subtotal": Decimal("900.00"),
            "tax_amount": Decimal("45.00"),
            "total_amount": Decimal("945.00"),
        },
        {
            "customer_id": customers[1].id,
            "order_id": orders[1].id,
            "invoice_number": "INV-2002",
            "due_date": date.today() + timedelta(days=15),
            "status": "partially_paid",
            "subtotal": Decimal("1200.00"),
            "tax_amount": Decimal("60.00"),
            "total_amount": Decimal("1260.00"),
        },
        {
            "customer_id": customers[2].id,
            "order_id": orders[2].id,
            "invoice_number": "INV-2003",
            "due_date": date.today() + timedelta(days=12),
            "status": "open",
            "subtotal": Decimal("500.00"),
            "tax_amount": Decimal("25.00"),
            "total_amount": Decimal("525.00"),
        },
        {
            "customer_id": customers[3].id,
            "order_id": orders[3].id,
            "invoice_number": "INV-2004",
            "due_date": date.today() - timedelta(days=5),
            "status": "overdue",
            "subtotal": Decimal("1750.00"),
            "tax_amount": Decimal("87.50"),
            "total_amount": Decimal("1837.50"),
        },
    ]

    invoices = [
        Invoice(
            organization_id=organization.id,
            customer_id=row["customer_id"],
            order_id=row["order_id"],
            invoice_number=row["invoice_number"],
            invoice_date=date.today() - timedelta(days=10),
            due_date=row["due_date"],
            status=row["status"],
            subtotal=row["subtotal"],
            tax_amount=row["tax_amount"],
            total_amount=row["total_amount"],
            currency_code="USD",
        )
        for row in invoice_seed_data
    ]
    db.add_all(invoices)
    await db.flush()

    payments = [
        Payment(
            organization_id=organization.id,
            payment_reference="PMT-3001",
            payment_date=date.today() - timedelta(days=4),
            amount=Decimal("945.00"),
            currency_code="USD",
        ),
        Payment(
            organization_id=organization.id,
            payment_reference="PMT-3002",
            payment_date=date.today() - timedelta(days=3),
            amount=Decimal("850.00"),
            currency_code="USD",
        ),
    ]
    db.add_all(payments)
    await db.flush()

    payment_allocations = [
        PaymentAllocation(payment_id=payments[0].id, invoice_id=invoices[0].id, allocated_amount=Decimal("945.00")),
        PaymentAllocation(payment_id=payments[1].id, invoice_id=invoices[1].id, allocated_amount=Decimal("850.00")),
    ]
    db.add_all(payment_allocations)

    await db.commit()
    await db.refresh(organization)
    return organization


def _serialize_model(model: object) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    return model


async def _get_default_organization_id(db: AsyncSession) -> uuid.UUID:
    organization = await db.scalar(select(Organization).order_by(Organization.created_at.asc()))
    if organization is None:
        raise ValueError("No organization found for business summary queries.")
    return organization.id


async def _get_revenue_summary_async(period_start: str, period_end: str) -> dict:
    del period_start, period_end
    async with SessionLocal() as db:
        organization_id = await _get_default_organization_id(db)
        result = await get_revenue_summary_service(db, organization_id)
        return _serialize_model(result)


async def _get_order_summary_async(period_start: str, period_end: str) -> dict:
    del period_start, period_end
    async with SessionLocal() as db:
        organization_id = await _get_default_organization_id(db)
        result = await get_order_summary_service(db, organization_id)
        return _serialize_model(result)


async def _get_top_customers_async(period_start: str, period_end: str, limit: int = 5) -> dict:
    del period_start, period_end
    async with SessionLocal() as db:
        organization_id = await _get_default_organization_id(db)
        result = await get_top_customers_service(db, organization_id)
        serialized = [
            _serialize_model(item)
            for item in result[:limit]
        ]
        return {"items": serialized, "count": len(serialized)}


async def _get_receivables_async() -> dict:
    async with SessionLocal() as db:
        organization_id = await _get_default_organization_id(db)
        result = await get_outstanding_receivables_service(db, organization_id)
        serialized = [_serialize_model(item) for item in result]
        return {"items": serialized, "count": len(serialized)}


def get_revenue_summary(period_start: str, period_end: str) -> dict:
    """Retrieve actual revenue metrics."""
    return asyncio.run(_get_revenue_summary_async(period_start, period_end))


def get_order_summary(period_start: str, period_end: str) -> dict:
    """Retrieve order counts and status breakdown."""
    return asyncio.run(_get_order_summary_async(period_start, period_end))


def get_top_customers(period_start: str, period_end: str, limit: int = 5) -> dict:
    """Retrieve customers ranked by invoiced sales."""
    return asyncio.run(_get_top_customers_async(period_start, period_end, limit=limit))


def get_receivables() -> dict:
    """Retrieve outstanding and overdue receivables."""
    return asyncio.run(_get_receivables_async())
