# app/routers/business_router.py

import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.customer import Customer
from app.models.order import Order
from app.models.organization import Organization
from app.repositories.business_repository import seed_fictional_business_data
from app.schemas.business import (
    OrderSummaryResponse,
    OutstandingReceivableResponse,
    RevenueSummaryResponse,
    TopCustomerResponse,
)
from app.services.business_intelligence_service import (
    get_order_summary,
    get_outstanding_receivables,
    get_revenue_summary,
    get_top_customers,
)
from sqlmodel import select

router = APIRouter(tags=["Business Operations"])


@router.post("/business/seed-data")
async def seed_business_data(db: AsyncSession = Depends(get_db)):
    organization = await seed_fictional_business_data(db)
    return {
        "message": "fictional company and customer data inserted",
        "organization_id": str(organization.id),
        "organization_name": organization.name,
    }


@router.get("/business/revenue-summary", response_model=RevenueSummaryResponse)
async def revenue_summary(
    organization_id: uuid.UUID = Query(..., description="Only view data for the selected tenant organization."),
    db: AsyncSession = Depends(get_db),
):
    return await get_revenue_summary(db, organization_id)


@router.get("/business/order-summary", response_model=OrderSummaryResponse)
async def order_summary(
    organization_id: uuid.UUID = Query(..., description="Only view data for the selected tenant organization."),
    db: AsyncSession = Depends(get_db),
):
    return await get_order_summary(db, organization_id)


@router.get("/business/top-customers", response_model=List[TopCustomerResponse])
async def top_customers(
    organization_id: uuid.UUID = Query(..., description="Only view data for the selected tenant organization."),
    db: AsyncSession = Depends(get_db),
):
    return await get_top_customers(db, organization_id)


@router.get("/business/receivables", response_model=List[OutstandingReceivableResponse])
async def outstanding_receivables(
    organization_id: uuid.UUID = Query(..., description="Only view data for the selected tenant organization."),
    db: AsyncSession = Depends(get_db),
):
    return await get_outstanding_receivables(db, organization_id)


@router.get("/business/outstanding-receivables", response_model=List[OutstandingReceivableResponse])
async def outstanding_receivables_alias(
    organization_id: uuid.UUID = Query(..., description="Only view data for the selected tenant organization."),
    db: AsyncSession = Depends(get_db),
):
    return await get_outstanding_receivables(db, organization_id)


@router.get("/orders/get_orders", response_model=List[Order])
async def get_orders(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    statement = select(Order).where(Order.customer_id == customer_id)
    result = await db.execute(statement)
    orders = result.scalars().all()
    return orders


@router.get("/organizations/{org_id}/customers", response_model=List[Customer])
async def get_tenant_customers(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    statement = select(Customer).where(Customer.organization_id == org_id)
    result = await db.execute(statement)
    customers = result.scalars().all()
    return customers
