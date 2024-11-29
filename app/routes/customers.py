from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Customer, Gender
from app.schemas import Customer as CustomerSchema

router = APIRouter()

# Obtener todos los clientes
@router.get("/customers", response_model=list[CustomerSchema])
async def get_all_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Customer.customer_id,
            Customer.age,
            Customer.frequency_of_purchases,
            Customer.promo_code_used,
            Customer.subscription_status,
            Gender.gender.label("gender")
        ).join(Gender, Customer.gender_id == Gender.gender_id)
    )
    customers = result.mappings().all()
    return customers

# Obtener un cliente por ID
@router.get("/customers/{customer_id}", response_model=CustomerSchema)
async def get_customer_by_id(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Customer.customer_id,
            Customer.age,
            Customer.frequency_of_purchases,
            Customer.promo_code_used,
            Customer.subscription_status,
            Gender.gender.label("gender")
        )
        .join(Gender, Customer.gender_id == Gender.gender_id)
        .where(Customer.customer_id == customer_id)
    )
    customer = result.mappings().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer

# Eliminar un cliente
@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.customer_id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    await db.delete(customer)
    await db.commit()
    return {"message": "Customer deleted successfully"}
