import os
import httpx
from fastapi import FastAPI, Depends
from pydantic import BaseModel #Librería que define de que forma recibe los datos la API
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from openai import OpenAI
from datetime import date
import json



# ==========================================
# 0. CONFIGURACIÓN VARIABLES DE ENTORNO
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicialización del cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

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
def procesar_factura(factura: FacturaRecibida, db: Session = Depends(get_db)):
    fecha_actual = date.today().isoformat()
    instrucciones = f"""
    Eres un asistente financiero. Tu único trabajo es extraer ciertos datos de los mensajes del usuario y agregar otros definidos en un formato JSON estricto.
    La fecha actual es: {fecha_actual}
    
    Extrae:
    - fecha (formato YYYY-MM-DD. Si el usuario no menciona una fecha en el texto, asume la fecha actual).
    - valor (solo el número, como float).
    - categoria (una palabra clave que describa el gasto estrictamente dentro de las siguientes categorías: vivienda, alimentacion, servicios, transporte, salud, deudas, ahorro, ocio).
    - id_usuario (usa siempre el número 1).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instrucciones},
                {"role": "user", "content": factura.texto}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        #Convierte el json en un diccionario
        datos_ia = json.loads(response.choices[0].message.content)
        
        nuevo_gasto = GastoDB(
            fecha=datos_ia.get("fecha", fecha_actual),
            valor=float(datos_ia.get("valor", 0.0)),
            categoria=datos_ia.get("categoria", ""),
            id_usuario=int(datos_ia.get("id_usuario", 1))
        )
        
        db.add(nuevo_gasto)
        db.commit()
        db.refresh(nuevo_gasto)
        
        return {
            "mensaje": "Factura procesada y guardada con éxito",
            "datos_extraidos": datos_ia   
        }
    except Exception as e:
        return {"mensaje": f"Error al procesar la factura: {str(e)}"}

@app.get("/gastos/")
def obtener_gastos(db: Session = Depends(get_db)):
    #Obtenemos los datos de postgress
    gastos = db.query(GastoDB).all()
    return gastos