from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import Location, Purchase
from app.schemas import Location as LocationSchema, LocationSales

router = APIRouter()

# Endpoint 1: Obtener todas las ubicaciones
@router.get("/locations", response_model=list[LocationSchema])
async def get_all_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    locations = result.scalars().all()
    return locations

# Endpoint 2: Obtener estadísticas de compras por ubicación
@router.get("/locations/{location_id}/sales", response_model=LocationSales)
async def get_sales_by_location(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Location.location.label("location_name"),
            func.count(Purchase.purchase_id).label("total_sales"),
            func.sum(Purchase.purchase_amount).label("total_revenue")
        )
        .join(Purchase, Purchase.location_id == Location.location_id)
        .where(Location.location_id == location_id)
        .group_by(Location.location)
    )
    sales_data = result.mappings().first()
    if not sales_data:
        raise HTTPException(status_code=404, detail="No se encontraron compras para esta ubicación")
    return sales_data

# Endpoint 3: Obtener todas las ubicaciones y sus ventas
@router.get("/locations/sales/all", response_model=list[LocationSales])
async def get_sales_of_all_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Location.location.label("location_name"),
            func.count(Purchase.purchase_id).label("total_sales"),
            func.sum(Purchase.purchase_amount).label("total_revenue")
        )
        .join(Purchase, Purchase.location_id == Location.location_id)
        .group_by(Location.location)
    )
    sales_data = result.mappings().all()

    if not sales_data:
        raise HTTPException(status_code=404, detail="No se encontraron ventas para las ubicaciones")
    return sales_data