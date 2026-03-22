from fastapi import FastAPI
from pydantic import BaseModel #Librería que define de que forma recibe los datos la API
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

#Variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

#FastAPI
app= FastAPI()

#Base de datos
Base = declarative_base()
engine = create_engine(DATABASE_URL) #Base de datos a utilizar 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Gestor de sesiones de la API
Base.metadata.create_all(bind=engine) #Crea la estructura de la base de datos en caso de que no exista

class Gasto(BaseModel):
    fecha: date
    valor: float
    categoria: str
    id_usuario: int
    
class GastoDB(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    valor = Column(Float)
    categoria = Column(String)
    id_usuario = Column(Integer)
    

@app.get("/")
def ruta_principal():
    return {"mensaje":"API del analizador de Gastos activa"}

@app.post("/gastos/")
def crear_gasto(nuevo_gasto: Gasto):
    # Añadir conexión con la base de datos
    return {"mensaje": "Gasto recibido correctamente", "gasto": nuevo_gasto}