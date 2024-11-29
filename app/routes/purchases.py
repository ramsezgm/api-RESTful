from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Purchase, Item, Location, Color, PaymentMethod
from app.schemas import Purchase as PurchaseSchema

router = APIRouter()

# Obtener todas las compras
@router.get("/purchases", response_model=list[PurchaseSchema])
async def get_all_purchases(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Purchase.purchase_id,
            Purchase.purchase_amount,
            Purchase.customer_id,
            Item.item.label("item_name"),
            Location.location.label("location_name"),
            Color.color.label("color_name"),
            PaymentMethod.payment_method.label("payment_method_name") 
        )
        .join(Purchase.item)
        .join(Purchase.location)
        .join(Purchase.color)
        .join(Purchase.payment_method)
    )
    purchases = result.mappings().all()  # Devuelve los resultados como un diccionario
    return purchases

# Obtener una compra por ID
@router.get("/purchases/{purchase_id}", response_model=PurchaseSchema)
async def get_purchase_by_id(purchase_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Purchase.purchase_id,
            Purchase.purchase_amount,
            Purchase.customer_id,
            Item.item.label("item_name"),
            Location.location.label("location_name"),
            Color.color.label("color_name"),
            PaymentMethod.payment_method.label("payment_method_name")
        )
        .join(Item, Purchase.item_id == Item.item_id)
        .join(Location, Purchase.location_id == Location.location_id)
        .join(Color, Purchase.color_id == Color.color_id)
        .join(PaymentMethod, Purchase.payment_method_id == PaymentMethod.payment_method_id)
        .where(Purchase.purchase_id == purchase_id)
    )
    purchase = result.mappings().first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return purchase

# Eliminar una compra por ID
@router.delete("/purchases/{purchase_id}")
async def delete_purchase(purchase_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Purchase).where(Purchase.purchase_id == purchase_id)
    )
    purchase = result.scalar_one_or_none()
    if not purchase:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    
    await db.delete(purchase)
    await db.commit()
    return {"detail": f"Compra con ID {purchase_id} eliminada exitosamente"}