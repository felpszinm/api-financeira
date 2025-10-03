from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função de Dependência (Usada pelos endpoints)
def get_db():
    db = SessionLocal() # Classe do Alchemy (Cria uma nova sessão do banco)
    try:
        yield db # Ele entrega a sessão do banco para fazermos um crud após pausa-la
    finally:
        db.close() # Fecha a sessão do banco