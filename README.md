# Analizador de Facturas AI

Este proyecto es una aplicación integral diseñada para automatizar el registro y análisis de gastos personales o empresariales. Utiliza Inteligencia Artificial para extraer información estructurada a partir de descripciones de facturas en lenguaje natural y visualiza los datos en un tablero interactivo.

## Características

- **Extracción Inteligente**: Utiliza GPT-4o-mini para procesar texto y extraer automáticamente la fecha, el valor y la categoría del gasto.
- **Categorización Automática**: Clasifica los gastos en categorías predefinidas (vivienda, alimentación, servicios, transporte, salud, deudas, ahorro, ocio).
- **Dashboard Interactivo**: Visualización de gastos mediante tablas y gráficos de barras (vía Recharts).
- **Arquitectura Robusta**: Backend con FastAPI, base de datos PostgreSQL y frontend moderno con Reflex.
- **Automatización**: Incluye un orquestador con n8n que genera reportes financieros semanales enviador por correo, analizador y redactador por IA.

## Stack Tecnológico

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) + [SQLAlchemy](https://www.sqlalchemy.org/)
- **IA**: [OpenAI API](https://openai.com/api/) (Modelo GPT-4o-mini)
- **Frontend**: [Reflex](https://reflex.dev/) (Framework de Python puro para web)
- **Base de Datos**: [PostgreSQL](https://www.postgresql.org/)
- **Orquestación**: [Docker Compose](https://docs.docker.com/compose/)
- **Automatización**: [n8n](https://n8n.io/)

## Requisitos Previos

- Docker y Docker Compose instalados.
- Una clave de API de OpenAI (`OPENAI_API_KEY`).
- Credenciales para usar la API de GMAIL (`GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`). 

## Configuración

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

# Añade ambas si quieres que n8n reconozca las variables del archivo .env
N8N_ALLOW_ENV_VARIABLES=true
N8N_BLOCK_ENV_ACCESS_IN_NODE=false
```

## Instalación y Despliegue

Para levantar todos los servicios (Base de datos, API, Frontend y n8n), simplemente ejecuta:

```bash
docker-compose up --build
```

Una vez finalizado el proceso, podrás acceder a:
- **Frontend**: `http://localhost:3000`
- **API (Docs)**: `http://localhost:8000/docs`
- **n8n**: `http://localhost:5678`

## Uso de la Aplicación

1. **Registro de Factura**: En el chat del frontend, escribe un mensaje como: *"Ayer gasté 50.000 en el supermercado por la cena"*.
2. **Procesamiento**: La IA extraerá los datos y los guardará en la base de datos PostgreSQL.
3. **Actualización**: Haz clic en el botón "Actualizar tabla" para ver el nuevo registro reflejado en la lista y en el gráfico de "Resumen por Categoría".

## Automatización y Reportes (n8n)

El proyecto incluye un workflow preconfigurado de n8n que consulta tu base de datos periódicamente, envía los datos a OpenAI para generar un análisis financiero personalizado de tus gastos semanales; el análisis se envia por correo electrónico con diseño HTML.

### **¿Cómo instalar el Workflow?**
1. Ingresa a la interfaz de n8n en `http://localhost:5678`.
2. Si es tu primera vez, crea una cuenta local de administrador.
3. En el menú principal, ve a la sección **Workflows** y haz clic en **Add Workflow**.
4. En la esquina superior derecha, selecciona el menú de opciones (...) y haz clic en **Import from File**.
5. Selecciona el archivo `analizador_facturas_reporte.json` que se encuentra en la carpeta `n8n_workflow`.
6. Configura las credenciales dentro de los nodos (PostgreSQL, OpenAI y Gmail) puedes ingresarlas manualmente o configurarlas mediante variables de entorno.
7. Haz clic en el boton Publish (o pon el switch en **Active**) en la esquina superior derecha par que el disparador automático (`Schedule Trigger`) comience a funcionar.

## Estructura del Proyecto

- `/main.py`: Lógica del servidor FastAPI y conexión con OpenAI.
- `/frontend/app/app.py`: Interfaz de usuario y lógica de estado construida con Reflex.
- `docker-compose.yml`: Configuración de los contenedores de la infraestructura.
- `n8n_workflow/analizador_facturas_reporte.json`: Workflow de n8n listo para importar.

## Futuras consideraciones
- Mejorar el front.
- Probar con diferentes modelos de IA; en busca de mejores resultados o ahorro de tokens.
- Implementar mejoras de seguridad.
