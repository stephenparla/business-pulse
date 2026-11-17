from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select

from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.order import Order
from app.models.organization import Organization
from app.models.payment import Payment
from app.models.payment_allocation import PaymentAllocation
from app.repositories.business_repository import seed_fictional_business_data
from app.services.business_intelligence_service import (
    get_order_summary,
    get_outstanding_receivables,
    get_revenue_summary,
    get_top_customers,
)


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_seed_fictional_business_data(db_session):
    org = await seed_fictional_business_data(db_session)
    assert org.name == "Northwind Operations"

    customers = await db_session.execute(select(Customer).where(Customer.organization_id == org.id))
    assert customers.scalars().all()

    orders = await db_session.execute(select(Order).where(Order.organization_id == org.id))
    assert len(orders.scalars().all()) >= 4


@pytest.mark.asyncio
async def test_business_summary_queries(db_session):
    org = await seed_fictional_business_data(db_session)

    revenue = await get_revenue_summary(db_session, org.id)
    order_summary = await get_order_summary(db_session, org.id)
    top_customers = await get_top_customers(db_session, org.id)
    receivables = await get_outstanding_receivables(db_session, org.id)

    assert revenue.organization_id == org.id
    assert revenue.total_revenue > Decimal("0.00")
    assert order_summary.organization_id == org.id
    assert order_summary.total_orders >= 1
    assert len(top_customers) >= 1
    assert sum(item.outstanding_amount for item in receivables) >= Decimal("0.00")
