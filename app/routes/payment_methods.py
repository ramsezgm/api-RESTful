from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.database import get_db
from app.models import PaymentMethod, Purchase
from app.schemas import PaymentMethodUsage
from typing import List

router = APIRouter()

# Endpoint 1: Obtener todos los métodos de pago
@router.get("/payment-methods", response_model=List[str])
async def get_all_payment_methods(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PaymentMethod.payment_method))
    payment_methods = result.scalars().all()

    if not payment_methods:
        raise HTTPException(status_code=404, detail="No se encontraron métodos de pago")

    return payment_methods

# Endpoint 2: Obtener los métodos de pago con su conteo de uso
@router.get("/payment-methods/usage", response_model=List[PaymentMethodUsage])
async def get_payment_method_usage(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            PaymentMethod.payment_method.label("payment_method_name"),
            func.count(Purchase.purchase_id).label("usage_count")
        )
        .join(Purchase, Purchase.payment_method_id == PaymentMethod.payment_method_id)
        .group_by(PaymentMethod.payment_method)
        .order_by(func.count(Purchase.purchase_id).desc())
    )
    payment_methods_usage = result.mappings().all()

    if not payment_methods_usage:
        raise HTTPException(status_code=404, detail="No se encontraron datos de uso para los métodos de pago")

    return [
        PaymentMethodUsage(
            payment_method_name=usage["payment_method_name"],
            usage_count=usage["usage_count"]
        )
        for usage in payment_methods_usage
    ]
