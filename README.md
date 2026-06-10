# MTS Backend API

Backend API desarrollado con **Serverless Framework**, **Python**, **SQLAlchemy**, **Alembic**, **Marshmallow** y **PostgreSQL**.

Este proyecto está configurado para trabajar localmente con una base de datos PostgreSQL en Docker y ejecutar funciones tipo AWS Lambda usando `serverless-offline`.

---

## Tecnologías principales

- Python 3.12
- Serverless Framework
- serverless-offline
- PostgreSQL
- SQLAlchemy
- Alembic
- Marshmallow
- Docker Compose

---

## Requisitos previos

Antes de iniciar, asegúrate de tener instalado:

- Python 3.12+
- Node.js
- npm
- Docker Desktop
- Serverless Framework
- Git

Opcional:

- `psql`, cliente de línea de comandos de PostgreSQL

> Nota: Si ya tienes PostgreSQL instalado localmente en el puerto `5432`, se recomienda exponer el PostgreSQL de Docker en el puerto `5433`.

---

## Estructura general del proyecto

```txt
mts-backend-api/
│
├── app/
│   ├── core/
│   │   └── database.py
│   │
│   ├── handlers/
│   │   └── molds_handler.py
│   │
│   ├── models/
│   │   └── mold.py
│   │
│   ├── repositories/
│   │   └── mold_repository.py
│   │
│   ├── schemas/
│   │   └── mold_schema.py
│   │
│   └── services/
│       └── molds_service.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── docker-compose.yml
├── alembic.ini
├── serverless.yml
├── requirements.txt
├── package.json
├── .env
└── README.md
```

---

## Configuración de variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+psycopg://app_user:app_password@localhost:5433/app_db
STAGE=local
```

Si estás usando el puerto `5432` para Docker, usa:

```env
DATABASE_URL=postgresql+psycopg://app_user:app_password@localhost:5432/app_db
```

---

## Configuración de PostgreSQL local con Docker

Ejemplo de `docker-compose.yml`:

```yml
services:
  postgres:
    image: postgres:16
    container_name: local-postgres
    restart: always
    environment:
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
      POSTGRES_DB: app_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Levantar la base de datos:

```bash
docker compose up -d
```

Detener la base de datos:

```bash
docker compose down
```

Eliminar la base de datos local junto con el volumen:

```bash
docker compose down -v
```

> Cuidado: `docker compose down -v` elimina la data local de PostgreSQL.

---

## Crear y activar ambiente virtual de Python

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

En macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Dependencias Python esperadas

El archivo `requirements.txt` debería incluir dependencias similares a estas:

```txt
SQLAlchemy>=2.0
psycopg[binary]>=3.1
alembic>=1.13
marshmallow>=3.21
marshmallow-sqlalchemy>=1.0
python-dotenv>=1.0
```

---

## Instalación de dependencias Node.js

Instalar dependencias del proyecto:

```bash
npm install
```

Instalar Serverless Offline si todavía no está instalado:

```bash
npm install --save-dev serverless serverless-offline
```

---

## Configuración de Serverless

Ejemplo base de `serverless.yml`:

```yml
service: mts-backend-api

frameworkVersion: "4"

useDotenv: true

provider:
  name: aws
  runtime: python3.12
  region: us-east-1
  stage: ${opt:stage, 'local'}
  timeout: 30
  environment:
    DATABASE_URL: ${env:DATABASE_URL}
    STAGE: ${self:provider.stage}

plugins:
  - serverless-offline

functions:
  listMolds:
    handler: app/handlers/molds_handler.list_molds
    events:
      - httpApi:
          path: /molds
          method: get

  createMold:
    handler: app/handlers/molds_handler.create_mold
    events:
      - httpApi:
          path: /molds
          method: post
```

---

## Configuración de Alembic

Alembic se utiliza para manejar migraciones de base de datos.

Inicializar Alembic, si todavía no existe la carpeta `alembic/`:

```bash
alembic init alembic
```

En `alembic/env.py`, asegúrate de importar la metadata de SQLAlchemy:

```python
from app.core.database import Base
from app.models.mold import Mold

target_metadata = Base.metadata
```

También asegúrate de cargar la variable `DATABASE_URL`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not configured")

config.set_main_option("sqlalchemy.url", database_url)
```

---

## Crear una migración

Después de modificar o crear modelos SQLAlchemy:

```bash
alembic revision --autogenerate -m "create-mold-table"
```

Aplicar migraciones pendientes:

```bash
alembic upgrade head
```

Ver historial de migraciones:

```bash
alembic history
```

Ver migración actual aplicada en la base de datos:

```bash
alembic current
```

Revertir una migración:

```bash
alembic downgrade -1
```

---

## Ejecutar el proyecto localmente

Primero levanta PostgreSQL:

```bash
docker compose up -d
```

Luego aplica migraciones:

```bash
alembic upgrade head
```

Después ejecuta Serverless Offline:

```bash
serverless offline --stage local
```

El API debería quedar disponible en una URL similar a:

```txt
http://localhost:3000
```

---

## Endpoints disponibles

### Listar moldes

```http
GET /molds
```

Ejemplo con curl:

```bash
curl http://localhost:3000/molds
```

---

### Crear molde

```http
POST /molds
```

Body esperado:

```json
{
  "name": "Prueba 1",
  "entry_date": "2026-06-09T10:30:00Z"
}
```

Ejemplo con PowerShell:

```powershell
curl -X POST http://localhost:3000/molds `
  -H "Content-Type: application/json" `
  -d '{"name": "Prueba 1", "entry_date": "2026-06-09T10:30:00Z"}'
```

Ejemplo con Bash:

```bash
curl -X POST http://localhost:3000/molds \
  -H "Content-Type: application/json" \
  -d '{"name": "Prueba 1", "entry_date": "2026-06-09T10:30:00Z"}'
```

---

## Modelo Mold

Ejemplo de modelo SQLAlchemy:

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Mold(Base):
    __tablename__ = "molds"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    entry_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
```

---

## Flujo recomendado de desarrollo

1. Crear o modificar modelos en `app/models/`.
2. Generar migración con Alembic:

```bash
alembic revision --autogenerate -m "migration-description"
```

3. Revisar el archivo generado en `alembic/versions/`.
4. Aplicar migración:

```bash
alembic upgrade head
```

5. Actualizar repository, service, schema y handler según corresponda.
6. Ejecutar Serverless Offline:

```bash
serverless offline --stage local
```

7. Probar los endpoints con curl, Postman o Thunder Client.

---

## Solución de problemas comunes

### Error: password authentication failed for user

Verifica que el usuario, contraseña, base de datos y puerto coincidan entre:

- `.env`
- `docker-compose.yml`
- PostgreSQL real en ejecución

Si tienes PostgreSQL local en `5432`, usa Docker en `5433`.

---

### Error: Alembic no detecta metadata

Verifica que en `alembic/env.py` tengas:

```python
from app.core.database import Base
from app.models.mold import Mold

target_metadata = Base.metadata
```

Si no importas los modelos, Alembic puede no detectar las tablas.

---

### Error: null value violates not-null constraint

El request no está enviando un campo obligatorio o el handler no lo está pasando al service/repository.

Verifica el flujo:

```txt
HTTP request → handler → service → repository → model → database
```

---

### Error: Lambda timeout en serverless-offline

Posibles causas:

- La base de datos no está accesible.
- `DATABASE_URL` apunta al puerto incorrecto.
- El handler no está retornando respuesta.
- La conexión a PostgreSQL se queda esperando.

Recomendación: configurar timeout de conexión en SQLAlchemy:

```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 5,
    },
)
```

---

## Comandos útiles

Levantar PostgreSQL:

```bash
docker compose up -d
```

Detener PostgreSQL:

```bash
docker compose down
```

Eliminar volumen local:

```bash
docker compose down -v
```

Crear migración:

```bash
alembic revision --autogenerate -m "description"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

Ejecutar API local:

```bash
serverless offline --stage local
```

Probar conexión usando psql dentro del contenedor:

```bash
docker exec -it local-postgres psql -U app_user -d app_db
```

---

## Notas importantes

- No ejecutes migraciones automáticamente desde la Lambda.
- Las migraciones deben ejecutarse como paso separado de desarrollo o despliegue.
- Mantén la lógica de negocio fuera de los handlers.
- Usa repositories para acceso a datos.
- Usa services para reglas de negocio.
- Usa schemas para validación y serialización.
- Usa variables de entorno para separar configuración local, dev y prod.
