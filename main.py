from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql import text  # Importar `text`
from app.routes.customers import router as customers_router
from app.routes.purchases import router as purchases_router
from app.routes.items import router as items_router
from app.routes.locations import router as locations_router
from app.routes.payment_methods import router as payment_methods_router

app = FastAPI(
    title="sales API",
    description="API for sales",
    version="0.1"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener una sesión
@app.on_event("startup")
async def startup_event():
    from app.database import SessionLocal
    async with SessionLocal() as session:
        try:
            await session.execute(text("SELECT 1"))  # Consulta segura con `text`
            print("Conexión a la base de datos exitosa.")
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

app.include_router(customers_router, prefix="/api/v1", tags=["Customers"])
app.include_router(purchases_router, prefix="/api/v1", tags=["Purchases"])
app.include_router(items_router, prefix="/api/v1", tags=["Items"])
app.include_router(locations_router, prefix="/api/v1", tags=["Locations"])
app.include_router(payment_methods_router, prefix="/api/v1", tags=["Payment Methods"])

# Ruta principal
@app.get("/")
async def root():
    return {"message": "Hello World"}