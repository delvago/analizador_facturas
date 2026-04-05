# 🧾 Analizador de Facturas AI

Este proyecto es una aplicación integral diseñada para automatizar el registro y análisis de gastos personales o empresariales. Utiliza Inteligencia Artificial para extraer información estructurada a partir de descripciones de facturas en lenguaje natural y visualiza los datos en un tablero interactivo.

## 🚀 Características

- **Extracción Inteligente**: Utiliza GPT-4o-mini para procesar texto y extraer automáticamente la fecha, el valor y la categoría del gasto.
- **Categorización Automática**: Clasifica los gastos en categorías predefinidas (vivienda, alimentación, servicios, transporte, salud, deudas, ahorro, ocio).
- **Dashboard Interactivo**: Visualización de gastos mediante tablas y gráficos de barras (vía Recharts).
- **Arquitectura Robusta**: Backend con FastAPI, base de datos PostgreSQL y frontend moderno con Reflex.
- **Automatización**: Incluye soporte para n8n, permitiendo crear un flujo de automatización que le hace reportes semanales al usuario de sus gastos, con recomendaciones financieras.

## 🛠️ Stack Tecnológico

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) + [SQLAlchemy](https://www.sqlalchemy.org/)
- **IA**: [OpenAI API](https://openai.com/api/) (Modelo GPT-4o-mini)
- **Frontend**: [Reflex](https://reflex.dev/) (Framework de Python puro para web)
- **Base de Datos**: [PostgreSQL](https://www.postgresql.org/)
- **Orquestación**: [Docker Compose](https://docs.docker.com/compose/)
- **Automatización**: [n8n](https://n8n.io/)

## 📋 Requisitos Previos

- Docker y Docker Compose instalados.
- Una clave de API de OpenAI (`OPENAI_API_KEY`).
- Credenciales para usar la API de GMAIL (`GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`). 

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
OPENAI_API_KEY=tu_clave_aqui
DATABASE_URL=postgresql://user:password@db:5432/facturas_db

# Variables para Postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=facturas_db
POSTGRESS_PORT=5432

# Variables para n8n
N8N_PORT=5678
# Añade estas variables si quieres que n8n reconozca las variables del archivo .env
N8N_ALLOW_ENV_VARIABLES=true
N8N_BLOCK_ENV_ACCESS_IN_NODE=false
```

## 📦 Instalación y Despliegue

Para levantar todos los servicios (Base de datos, API, Frontend y n8n), simplemente ejecuta:

```bash
docker-compose up --build
```

Una vez finalizado el proceso, podrás acceder a:
- **Frontend**: `http://localhost:3000`
- **API (Docs)**: `http://localhost:8000/docs`
- **n8n**: `http://localhost:5678`

## 🖥️ Uso de la Aplicación

1. **Registro de Factura**: En el chat del frontend, escribe un mensaje como: *"Ayer gasté 50.000 en el supermercado por la cena"*.
2. **Procesamiento**: La IA extraerá los datos y los guardará en la base de datos PostgreSQL.
3. **Actualización**: Haz clic en el botón "Actualizar tabla" para ver el nuevo registro reflejado en la lista y en el gráfico de "Resumen por Categoría".

## 📂 Estructura del Proyecto

- `/main.py`: Lógica del servidor FastAPI y conexión con OpenAI.
- `/frontend/app/app.py`: Interfaz de usuario y lógica de estado construida con Reflex.
- `docker-compose.yml`: Configuración de los contenedores de la infraestructura.
