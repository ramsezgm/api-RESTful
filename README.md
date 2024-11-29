# Crear un archivo README.txt en español en texto plano
readme_content = """
# API de Ventas

La API de Ventas es un servicio backend construido con FastAPI para gestionar y analizar datos de ventas. Permite operaciones relacionadas con clientes, compras, productos, ubicaciones y métodos de pago.

## Tabla de Contenidos

- [Características](#características)
- [Endpoints](#endpoints)
- [Instalación](#instalación)
- [Ejecutando la API](#ejecutando-la-api)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

---

## Características

- Gestión de Clientes: Recuperar y eliminar datos de clientes.
- Gestión de Compras: Recuperar y eliminar registros de compras.
- Gestión de Productos: Recuperar detalles de productos, ventas por producto y los productos más vendidos.
- Gestión de Ubicaciones: Recuperar ubicaciones y analizar las ventas por ubicación.
- Gestión de Métodos de Pago: Recuperar métodos de pago y analizar su uso.

---

## Endpoints

### Clientes

- `GET /api/v1/customers`: Recuperar todos los clientes.
- `GET /api/v1/customers/{customer_id}`: Recuperar un cliente por ID.
- `DELETE /api/v1/customers/{customer_id}`: Eliminar un cliente por ID.

### Compras

- `GET /api/v1/purchases`: Recuperar todas las compras.
- `GET /api/v1/purchases/{purchase_id}`: Recuperar una compra por ID.
- `DELETE /api/v1/purchases/{purchase_id}`: Eliminar una compra por ID.

### Productos

- `GET /api/v1/items`: Recuperar todos los productos.
- `GET /api/v1/items/{item_id}`: Recuperar detalles de un producto.
- `GET /api/v1/items/{item_id}/sales`: Recuperar datos de ventas de un producto específico.
- `GET /api/v1/items/sales/order`: Recuperar datos de ventas de todos los productos.

### Ubicaciones

- `GET /api/v1/locations`: Recuperar todas las ubicaciones.
- `GET /api/v1/locations/{location_id}/sales`: Recuperar datos de ventas de una ubicación específica.
- `GET /api/v1/locations/sales/all`: Recuperar datos de ventas de todas las ubicaciones.

### Métodos de Pago

- `GET /api/v1/payment-methods`: Recuperar todos los métodos de pago.
- `GET /api/v1/payment-methods/usage`: Recuperar estadísticas de uso de métodos de pago.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ramsezgm/api-RESTful.git
   cd sales-api
2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv venv
    # Activar en Windows
    .\venv\Scripts\activate
    # Activar en Linux/MacOS
    source venv/bin/activate
    
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

4. Configura el archivo `.env` con la siguiente información:
    ```bash
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=tu_contraseña
    DB_NAME=sales
    DB_PORT=3306
    
## Ejecutando la API

1. Inicia el servidor:
    ```bash
    uvicorn main:app --reload

2. Accede a la documentación de la API en:
-   Swagger UI: http://127.0.0.1:8000/docs
-   ReDoc: http://127.0.0.1:8000/redoc