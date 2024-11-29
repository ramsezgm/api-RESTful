from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Modelo para la tabla Item
class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    purchases = relationship("Purchase", back_populates="item")

# Modelo para la tabla Color
class Color(Base):
    __tablename__ = "color"
    color_id = Column(Integer, primary_key=True, index=True)
    color = Column(String, nullable=False)
    purchases = relationship("Purchase", back_populates="color")

# Modelo para la tabla PaymentMethod
class PaymentMethod(Base):
    __tablename__ = "payment_method"
    payment_method_id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(String, nullable=False)
    purchases = relationship("Purchase", back_populates="payment_method")

# Modelo para la tabla Location
class Location(Base):
    __tablename__ = "location"
    location_id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    purchases = relationship("Purchase", back_populates="location")

# Modelo para la tabla Gender
class Gender(Base):
    __tablename__ = "gender"
    gender_id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=False)
    customers = relationship("Customer", back_populates="gender")

# Modelo para la tabla Customer
class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    frequency_of_purchases = Column(Integer, nullable=False)
    promo_code_used = Column(Integer, nullable=False)
    subscription_status = Column(String, nullable=False)
    gender_id = Column(Integer, ForeignKey("gender.gender_id"))

    # Relaciones
    gender = relationship("Gender", back_populates="customers")
    purchases = relationship("Purchase", back_populates="customer") 

# Modelo para la tabla Purchase
class Purchase(Base):
    __tablename__ = "purchase"
    purchase_id = Column(Integer, primary_key=True, index=True)
    purchase_amount = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey("item.item_id"))
    location_id = Column(Integer, ForeignKey("location.location_id"))
    color_id = Column(Integer, ForeignKey("color.color_id"))
    payment_method_id = Column(Integer, ForeignKey("payment_method.payment_method_id"))
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))

    item = relationship("Item", back_populates="purchases")
    color = relationship("Color", back_populates="purchases")
    location = relationship("Location", back_populates="purchases")
    payment_method = relationship("PaymentMethod", back_populates="purchases")
    customer = relationship("Customer", back_populates="purchases")
