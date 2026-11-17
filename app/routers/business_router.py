# app/routers/business_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.session import get_db
from app.models.order import Order
from app.models.customer import Customer
from app.models.organization import Organization

router = APIRouter(tags=["Business Operations"])

# ============================================================================
# 1. Orders Scope
# ============================================================================

@router.get("/orders/get_orders", response_model=List[Order])
async def get_orders(
    customer_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch all historical orders belonging to a specific customer UUID.
    """
    statement = select(Order).where(Order.customer_id == customer_id)
    result = await db.execute(statement)
    orders = result.scalars().all()
    
    if not orders:
        raise HTTPException(
            status_code=404, 
            detail=f"No orders found for customer: {customer_id}"
        )
        return [] # Ensures safe list iteration downstream
        
    return orders


# ============================================================================
# 2. Multi-Tenant Organization Scope (New business endpoints)
# ============================================================================

@router.get("/organizations/{org_id}/customers", response_model=List[Customer])
async def get_tenant_customers(
    org_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch all customers strictly isolated under a single organization tenant.
    """
    statement = select(Customer).where(Customer.organization_id == org_id)
    result = await db.execute(statement)
    customers = result.scalars().all()
    
    return customers
