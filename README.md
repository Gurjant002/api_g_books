# api_g_books
API de g-books

## Entorno Virtual (venv)

Para crear un entorno virtual y gestionar las dependencias del proyecto, sigue estos pasos:

1. **Crear un entorno virtual**:
    ```bash
    python -m venv venv
    ```

2. **Activar el entorno virtual**:
    - En Windows:
        ```bash
        venv\Scripts\activate
        ```
    - En macOS y Linux:
        ```bash
        source venv/bin/activate
        ```

3. **Instalar dependencias en el entorno virtual**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Desactivar el entorno virtual**:
    ```bash
    deactivate
    ```

## Cómo arrancar el servidor

Para iniciar el servidor, ejecuta el siguiente comando en la raíz del proyecto:

```bash
python run server
```

## Uso de Alembic para migraciones de base de datos

1. **Inicializar Alembic** (solo la primera vez):
    ```bash
    alembic init alembic
    ```
2. **Crear una nueva migración**:
    ```bash
    alembic revision --autogenerate -m "mensaje de la migración"
    ```
3. **Aplicar migraciones**:
    ```bash
    alembic upgrade head
    ```

## Requisitos previos

- Python 3.x
- Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Variables de entorno

Configura las variables necesarias en un archivo `.env` si es requerido por el proyecto.

## Estructura del proyecto

- `run`: Script principal para arrancar el servidor.
- `alembic/`: Carpeta de migraciones de base de datos.
- `requirements.txt`: Dependencias del proyecto.

## Contacto

Para dudas o sugerencias, contacta al mantenedor del proyecto.
