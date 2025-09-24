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

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

### =============== Modelos do Banco de Dados =============== ###
#* São as tabelas do seu banco.

#* Criando a classe de usuario (Tabela de usuários no banco)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    #* define a relação entre as tabelas User e Transaction no SQLAlchemy.
    transactions = relationship("Transaction", back_populates="owner")

#* Criando a classe de Transação (Tabela de transações no banco)
class Transaction(Base):
    __tablename__ = "transactions"
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
        yield db # Ele entrega a sessão do banco para fazermos um crud após pausa-la
    finally:
        db.close() # Fecha a sessão do banco

### =============== Modelos de Validação de Dados =============== ###
# Estrutura dos dados que a API recebe e envia (Pydantic)

#* Define o tipo dos dados pra 'User':
class UserCreate(BaseModel):
    name: str
    email: str

#* Formata os dados (Saída) de 'User' para a API:
class UserSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        #* Faz a manipulação de dados para JSON
        orm_mode = True

#* Define o tipo dos dados pra Transaction:
class TransactionCreate(BaseModel):
    description: str
    amount: float
    owner_id: int

#* Formata os dados (Saída) de Transação para a API:
class TransactionSchema(BaseModel):
    id: int
    description: str
    amount: float
    created_at: datetime
    owner_id: int

    class Config:
        #* Faz a manipulação de dados para JSON
        orm_mode = True

### =============== Endpoints da API =============== ###

#* Define o Endpoint da criação de User (POST)
@app.post("/api/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # Verifica se o usuario ja existe no banco através do email.
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Criando um novo user
    db_user = User(name=user.name, email=user.email)
    db.add(db_user) # Adiciona user ao banco
    db.commit() # Salva os dados de user no banco
    db.refresh(db_user) # Atualiza o Usuario criado no Banco
    return db_user # Retorna o objeto para a FastAPI

#* Define o Endpoint para pegar as transações de um usuario por ID (GET)
@app.get("/api/users/{user_id}/transactions/", response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Criando uma nova transação
    db_transaction = Transaction(description=transaction.description, amount=transaction.amount, owner_id=transaction.owner_id)
    db.add(db_transaction) # Adiciona a transação ao banco
    db.commit() # Salva os dados da transação no banco
    db.refresh(db_transaction) # Atualiza a transação criada no Banco
    return db_transaction # Retorna o objeto para a FastAPI