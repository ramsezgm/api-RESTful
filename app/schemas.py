from pydantic import BaseModel
from typing import List, Optional

# Esquema para la tabla Item
class Item(BaseModel):
    item_id: int
    item: str

    class Config:
        orm_mode = True

# Esquema para la tabla Color
class Color(BaseModel):
    color_id: int
    color: str

    class Config:
        orm_mode = True

# Esquema para la tabla PaymentMethod
class PaymentMethod(BaseModel):
    payment_method_id: int
    payment_method: str

    class Config:
        orm_mode = True

# Esquema para la tabla Location
class Location(BaseModel):
    location_id: int
    location: str

    class Config:
        orm_mode = True

# Esquema para la tabla Gender
class Gender(BaseModel):
    gender_id: int
    gender: str

    class Config:
        orm_mode = True

# Esquema para la tabla Customer
class Customer(BaseModel):
    customer_id: int
    age: int
    frequency_of_purchases: int
    promo_code_used: int
    subscription_status: int
    gender: Optional[str]  # Incluye información del género

    class Config:
        orm_mode = True

# Esquema para la tabla Purchase
class Purchase(BaseModel):
    purchase_id: int
    purchase_amount: float
    customer_id: int
    item_name: str  # Solo el nombre del ítem
    location_name: str  # Solo el nombre de la ubicación
    color_name: str  # Solo el nombre del color
    payment_method_name: str  # Solo el nombre del método de pago

    class Config:
        orm_mode = True

# Esquema para estadísticas de ventas de un producto
class ItemSales(BaseModel):
    item_name: str
    total_sales: int
    total_revenue: float
    
# Esquema para estadísticas de compras por ubicación
class LocationSales(BaseModel):
    location_name: str
    total_sales: int
    total_revenue: float
    
# Esquema para el uso de métodos de pago
class PaymentMethodUsage(BaseModel):
    payment_method_name: str
    usage_count: int