from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

# URL de la base de datos
DATABASE_URL = f"mysql+aiomysql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"

# Crear el motor de base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la base declarativa para los modelos
Base = declarative_base()

# Configurar la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependencia para obtener una sesión
async def get_db():
    async with SessionLocal() as session:
        yield session
