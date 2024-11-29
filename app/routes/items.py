from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import Item, Purchase
from app.schemas import Item as ItemSchema, ItemSales

router = APIRouter()

# Endpoint 1: Obtener todos los items
@router.get("/items", response_model=list[ItemSchema])
async def get_all_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items

# Endpoint 2: Obtener detalles de un item
@router.get("/items/{item_id}", response_model=ItemSchema)
async def get_item_by_id(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.item_id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

# Endpoint 3: Obtener ventas por producto
@router.get("/items/{item_id}/sales", response_model=ItemSales)
async def get_sales_by_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Item.item.label("item_name"),
            func.count(Purchase.purchase_id).label("total_sales"),
            func.sum(Purchase.purchase_amount).label("total_revenue")
        )
        .join(Purchase, Purchase.item_id == Item.item_id)
        .where(Item.item_id == item_id)
        .group_by(Item.item)
    )
    sales_data = result.mappings().first()
    if not sales_data:
        raise HTTPException(status_code=404, detail="No se encontraron ventas para este producto")
    return sales_data

# Endpoint 4: Obtener las ventas generadas de todos los ítems
@router.get("/items/sales/order", response_model=list[ItemSales])
async def get_sales_of_all_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Item.item.label("item_name"),
            func.count(Purchase.purchase_id).label("total_sales"),
            func.sum(Purchase.purchase_amount).label("total_revenue")
        )
        .join(Purchase, Purchase.item_id == Item.item_id)
        .group_by(Item.item)
        .order_by(func.count(Purchase.purchase_id).desc())
    )
    sales_data = result.mappings().all()

    if not sales_data:
        raise HTTPException(status_code=404, detail="No se encontraron ventas para los ítems")

    all_sales = [
        ItemSales(
            item_name=item["item_name"],
            total_sales=item["total_sales"],
            total_revenue=item["total_revenue"]
        )
        for item in sales_data
    ]

    return all_sales