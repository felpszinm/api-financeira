from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

app = FastAPI()


DATABASE_URL=os.getenv("DATABASE_URL")
@app.get("/")
def read_root():
    return {"message": "API running with sucessfull"}

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

### =============== Modelos do Banco de Dados =============== ###
#* São as tabelas do seu banco.

# Criando a classe de usuario
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    #* define a relação entre as tabelas User e Transaction no SQLAlchemy.
    transactions = relationship("Transaction", back_populates="owner")

#* Criando a classe de Transação
class Transaction(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    #? Chave estrangeira que conecta a transação ao usuário:
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")

#* Criando as tabelas do banco:
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal() # Classe do Alchemy (Cria uma nova sessão do banco)
    try:
        yield db() # Ele entrega a sessão do banco para fazermos um crud após pausa-la
    finally:
        db.close() # Fecha a sessão do banco
