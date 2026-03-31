import os
import httpx
from fastapi import FastAPI, Depends
from pydantic import BaseModel #Librería que define de que forma recibe los datos la API
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


# ==========================================
# 0. CONFIGURACIÓN VARIABLES DE ENTORNO
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
URL_N8N = os.getenv("URL_N8N")

# ==========================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================
engine = create_engine(DATABASE_URL) #Base de datos a utilizar 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Gestor de sesiones de la API
Base = declarative_base()

# ==========================================
# 2. CONFIGURACIÓN SQLALCHEMY (La Tabla)
# ==========================================
class GastoDB(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    valor = Column(Float)
    categoria = Column(String)
    id_usuario = Column(Integer)

Base.metadata.create_all(bind=engine) #Crea la estructura de la base de datos en caso de que no exista

# ==========================================
# 3. CONFIGURACIÓN DE FASTAPI Y PYDANTIC
# ==========================================
app = FastAPI()

class Gasto(BaseModel):
    fecha: date
    valor: float
    categoria: str
    id_usuario: int

class FacturaRecibida(BaseModel):
    texto: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# ==========================================
# 4. RUTAS DE LA API
# ==========================================
@app.get("/")
def ruta_principal():
    return {"mensaje" : "API del analizador de Gastos activa"}

@app.post("/factura/")
def procesar_factura(factura: FacturaRecibida):
    n8n_data = {"texto_factura": factura.texto}
    try:
        n8n_response = httpx.post(URL_N8N, json=n8n_data)
        if n8n_response.status_code == 200:
            return {"mensaje" : f"Factura: {factura.texto} - Recibida"}
        else:
            return {"mensaje" : f"Error en n8n: Código {n8n_response.status_code}"}
    except Exception as e:
        return {"mensaje" : f"Fallo al intentar conectar con n8n: {str(e)}"}
            
@app.post("/gastos/")
def crear_gasto(nuevo_gasto: Gasto, db: Session = Depends(get_db)):
    #Empaquetado de los datos para la base de datos
    gasto_db = GastoDB(
        fecha=nuevo_gasto.fecha,
        valor=nuevo_gasto.valor,
        categoria=nuevo_gasto.categoria,
        id_usuario=nuevo_gasto.id_usuario
    )
    #Guardado de datos en PostgreSQL
    db.add(gasto_db)
    db.commit()
    db.refresh(gasto_db)
    return {"mensaje" : "Gasto guardado con éxito", "gasto": gasto_db}

@app.get("/gastos/")
def obtener_gastos(db: Session = Depends(get_db)):
    #Obtenemos los datos de postgress
    gastos = db.query(GastoDB).all()
    return gastos