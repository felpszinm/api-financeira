from fastapi import FastAPI, Depends, HTTPException, status
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


#===============================================================#
### =============== Modelos do Banco de Dados =============== ###
#===============================================================#

# São as tabelas do seu banco.

#* Criando a classe de usuario (Tabela de usuários no banco)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    #* define a relação entre as tabelas User e Transaction no SQLAlchemy.
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")

#* Criando a classe de Transação (Tabela de transações no banco)
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    #? Chave estrangeira que conecta a transação ao usuário:
    #* Se caso algum usuario ou categoria for excluida, todas transações são excluidas que tenham conexão.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    #? Relacionametos
    owner = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


#* Criando a classe de Categorias (Tabela de categorias no banco)
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relacionamento: uma categoria pode ter várias transações.
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")

#* Criando as tabelas do banco:
Base.metadata.create_all(bind=engine)


#=============================================#
### =============== Funções =============== ###
#=============================================#

''' #! Função descontinuada (Até o momento)
#* Função de validar filtragens dentro do banco e retornar para a API
def raise_http_exception(parameter, message: str):
    if not parameter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=message
        )
'''

def get_db():
    db = SessionLocal() # Classe do Alchemy (Cria uma nova sessão do banco)
    try:
        yield db # Ele entrega a sessão do banco para fazermos um crud após pausa-la
    finally:
        db.close() # Fecha a sessão do banco


#===================================================================#
### =============== Modelos de Validação de Dados =============== ###
#===================================================================#

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

#* Atualiza os dados dos usuários para a API: 
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# ---

#* Define o tipo dos dados pra Transaction:
class TransactionCreate(BaseModel):
    description: str
    amount: float
    category_id: int # Sincroniza com a categoria

#* Formata os dados (Saída) de Transação para a API:
class TransactionSchema(BaseModel):
    id: int
    description: str
    amount: float
    created_at: datetime
    owner_id: int # Sincroniza com usuario
    category_id: int # Sincroniza com a categoria

    class Config:
        #* Faz a manipulação de dados para JSON
        orm_mode = True

#* Atualiza os dados da Transação para a API:
class TransactionPatch(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None

# ---

#* Define os tipos de dados pra Category:
class CategoryCreate(BaseModel):
    name: str

#* Formata os dados (Saída) das Categorias para a API:
class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        #* Faz a manipulação de dados para JSON
        orm_mode = True

#* Atualiza os dados das Categorias para a API:
class CategoryPatch(BaseModel):
    name: Optional[str] = None


# ==================================================== #  
### =============== Endpoints da API =============== ###
# ==================================================== # 

#===========================================#
## === Endpoints para o recurso 'User' === ##
#===========================================#
#* Define o Endpoint para pegar as informações de todos usuarios (GET)
@app.get("/api/users/", response_model=List[UserSchema])
def get_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users

#* Define o Endpoint para pegar as informações de 1 User (GET)
@app.get("/api/users/{user_id}/", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

#* Define o Endpoint da criação de User (POST)
@app.post("/api/users/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
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

#* Define o Endpoint para atualizar User (PATCH)
@app.patch("/api/users/{user_id}/", response_model=UserPatch)
def update_user(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_data = user.model_dump(exclude_unset=True, exclude_none=True) # Gera dicts apenas com as informações definidas na requisição

    for key, value in user_data.items(): # Faz a alteração de todos os items que vieram com valores
        setattr(db_user, key, value)
    
    db.commit() # Salva no banco
    db.refresh(db_user) # Atualiza o 'User' no Banco
    return db_user

@app.delete("/api/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found")
    db.delete(user) # Deleta a informação
    db.commit() # Salva no banco
    return {
        "message": "User successfully deleted.",
        "user": user_id
    }

#===================================================#
## === Endpoints para o recurso 'Transactions' === ##
#===================================================#

@app.get("/api/transactions/", response_model=List[TransactionSchema])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transactions

#* Define o Endpoint para pegar as informações de 1 User (GET)
@app.get("/api/users/{user_id}/transactions/", response_model=List[TransactionSchema])
def get_transactions_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first() # Valida se o user_id é igual ao User.id do banco
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    transactions = db.query(Transaction).filter(Transaction.owner_id == user_id).all()
    # Valida se o transaction_id é igual ao Transaction.id do banco
    return transactions


#* Define o Endpoint para criar uma nova transação (POST)
@app.post("/api/users/{user_id}/transactions/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(user_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    user_owner = db.query(User).filter(User.id == user_id).first()
    if not user_owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found")
    
    category_exists = db.query(Category).filter(Category.id == transaction.category_id).first()
    if not category_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Criando uma nova transação
    db_transaction = Transaction(
        description=transaction.description,
        amount=transaction.amount,
        owner_id=user_id,
        category_id=transaction.category_id
    )

    db.add(db_transaction) # Adiciona a transação ao banco
    db.commit() # Salva os dados da transação no banco
    db.refresh(db_transaction) # Atualiza a transação criada no Banco
    return db_transaction # Retorna o objeto para a FastAPI

#* Define um Endpoint para atualização de uma transação de um usuário (PATCH)
@app.patch("/api/users/{user_id}/transactions/{transaction_id}/", response_model=TransactionPatch)
def update_transaction(user_id: int, transaction_id: int, transaction: TransactionPatch, db: Session = Depends(get_db)):
    # Filtra a query do banco pelo id do usuario e id de transação igual ao do Banco.
    db_transaction = db.query(Transaction).filter(
        Transaction.owner_id == user_id, 
        Transaction.id == transaction_id
        ).first()
    
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    transaction_data = transaction.model_dump(exclude_unset=True, exclude_none=True) # Gera dicts apenas com as informações definidas na requisição

    for key, value in transaction_data.items(): # Faz a alteração de todos os items que vieram com valores
        setattr(db_transaction, key, value)

    db.commit() # Salva no banco
    db.refresh(db_transaction) # Atualiza uma transação de um usuário no Banco
    return db_transaction


#* Define o Endpoint para deletar uma transação de um usuario (DELETE)
@app.delete("/api/users/{user_id}/transactions/{transaction_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(user_id:int, transaction_id:int, db: Session = Depends(get_db)):
    # Filtra a query do banco pelo id do usuario e id de transação igual ao do Banco.
    del_transaction = db.query(Transaction).filter(
        Transaction.owner_id == user_id, 
        Transaction.id == transaction_id
        ).first()
    
    if not del_transaction:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction not found or does not belong to the specified user."
        )
    
    db.delete(del_transaction) # Deleta a informação
    db.commit() # Salva no banco

    return {
        "message": " Transaction successfully deleted.",
        "user": user_id,
        "transaction": transaction_id
    }

#=================================================#
## === Endpoints para o recurso 'Categories' === ##
#=================================================#

#* Define o Endpoint para pegar todas categorias (GET)
@app.get("/api/categories/", response_model=List[CategorySchema])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return categories

#* Define o Endpoint para criar uma categoria (POST)
@app.post("/api/categories/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Valida se categoria ja existe no banco através do nome.
    existing_category = db.query(Category).filter(Category.name == category.name).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already registered"
        )
    
    # Criando uma nova categoria
    db_category = Category(name=category.name)
    db.add(db_category) # Adiciona a categoria ao banco.
    db.commit() # Salva o banco
    db.refresh(db_category) # Atualiza a categoria dentro do banco 
    return db_category

@app.patch("/api/categories/{category_id}/")
def update_category(category_id: int, category: CategoryPatch, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category_data = category.model_dump(exclude_unset=True, exclude_none=True) # Gera dicts apenas com as informações definidas na requisição

    for key, value in category_data.items(): # Faz a alteração de todos os items que vieram com valores
        setattr(db_category, key, value)

    db.commit() # Salva no banco
    db.refresh(db_category) # Atualiza uma alteração de uma categoria no Banco
    return db_category

#* Define o Endpoint para deletar uma categoria (DELETE)
@app.delete("/api/categories/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    
    del_category = db.query(Category).filter(Category.id == category_id).first()
    if not del_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category doesn't exist.")

    db.delete(del_category)
    db.commit()

    return {
        "message": "Category successfully deleted.",
    }