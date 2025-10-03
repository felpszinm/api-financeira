from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

# Meus módulos externos
from . import crud
from . import schemas # Schemas Pydantic
from . import models # Modelos SQLAlchemy
from .database import get_db, engine # get_db para dependência, engine para criação inicial

app = FastAPI(
    title="Financial Control API",
    version="1.0.1",
    description="API for managing users, transactions and categories"
)

#* Criando as tabelas do banco:
models.Base.metadata.create_all(bind=engine)

# ==================================================== #  
### =============== Endpoints da API =============== ###
# ==================================================== # 


### ======= Endpoints para o recurso 'User' ======= ###


#* Define o Endpoint para pegar as informações de todos usuarios (GET)
@app.get("/api/users/", response_model=List[schemas.UserSchema])
def get_users_endpoint(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    
    return users

#* Define o Endpoint para pegar as informações de usuário por email (GET)
"""#! ROTA ESPECIFICA -> VIR PRIMEIRO SEMPRE #!"""
@app.get("/api/users/by_email/", response_model=schemas.UserSchema)
def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)):
    user_by_email = crud.get_user_by_email(db, email=email)

    if user_by_email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_by_email

#* Define o Endpoint para pegar as informações de 1 User (GET)
@app.get("/api/users/{user_id}/", response_model=schemas.UserSchema)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


#* Define o Endpoint da criação de User (POST)
@app.post("/api/users/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuario ja existe no banco através do email.
    existing_user = crud.get_user_by_email(db, email=user.email)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    # Criando um novo user
    created_user = crud.create_user(db, user=user)
    
    return created_user # Retorna o objeto para a FastAPI

#* Define o Endpoint para atualizar User (PATCH)
@app.patch("/api/users/{user_id}/", response_model=schemas.UserPatch)
def update_user_endpoint(user_id: int, user_update: schemas.UserPatch, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Chamo o crud pra aplicar a atualização
    updated_user = crud.update_user(db, db_user=db_user, user_update=user_update)

    return updated_user

@app.delete("/api/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Se o crud retornar o objeto, o FastAPI vai retornar o status_code 204 definido no decorador
    return


### === Endpoints para o recurso 'Transactions' === ###


@app.get("/api/users/{user_id}/transactions/", response_model=List[schemas.TransactionSchema])
def get_all_transactions_by_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    transactions = crud.get_all_transactions_by_user(db, user_id=user_id)
    
    return transactions

#* Define o Endpoint para pegar as informações de 1 User (GET)
@app.get("/api/users/{user_id}/transactions/{transaction_id}/", response_model=schemas.TransactionSchema)
def get_transaction_by_user_endpoint(user_id: int, transaction_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    transactions = crud.get_transaction_by_user(db, user_id=user_id, transaction_id=transaction_id)
    
    return transactions


#* Define o Endpoint para criar uma nova transação (POST)
@app.post("/api/users/{user_id}/transactions/", response_model=schemas.TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction_endpoint(user_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    user_owner = crud.get_user(db, user_id=user_id)

    # Checagem de usuário
    if user_owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Checagem de categoria
    category_exists = crud.get_category_by_id(db, category_id=transaction.category_id)
    if category_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Criação da transação
    created_transaction = crud.create_transaction(db, transaction=transaction, owner_id=user_id)

    return created_transaction # Retorna o objeto para a FastAPI


#* Define um Endpoint para atualização de uma transação de um usuário (PATCH)
@app.patch("/api/users/{user_id}/transactions/{transaction_id}/", response_model=schemas.TransactionPatch)
def update_transaction_endpoint(user_id: int, transaction_id: int, transaction_update: schemas.TransactionPatch, db: Session = Depends(get_db)):
    
    # Pega as informações do banco por usuario
    db_transaction = crud.get_transactions_for_user(db, user_id=user_id, transaction_id=transaction_id)
    
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found or does not belong to the user.")
    
    # Se caso db_transction retornar o objeto, ele atualiza com o crud
    updated_transaction = crud.update_transaction(db, db_transaction=db_transaction, transaction_update=transaction_update)

    return updated_transaction # Retorna o objeto para a FastAPI


#* Define o Endpoint para deletar uma transação de um usuario (DELETE)
@app.delete("/api/users/{user_id}/transactions/{transaction_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_endpoint(user_id:int, transaction_id:int, db: Session = Depends(get_db)):
    deleted_transaction = crud.delete_transaction(user_id=user_id, transaction_id=transaction_id, db=db)
    if deleted_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found or does not belong to the specified user."
        )
    
    # Se o crud retornar o objeto, o FastAPI vai retornar o status_code 204 definido no decorador
    return 

#=================================================#
## === Endpoints para o recurso 'Categories' === ##
#=================================================#

#* Define o Endpoint para pegar todas categorias (GET)
@app.get("/api/categories/", response_model=List[schemas.CategorySchema])
def get_all_categories_endpoint(db: Session = Depends(get_db)):
    categories = crud.get_all_categories(db)

    return categories

#* Define o Endpoint para pegar uma categoriaa pelo ID (GET)
@app.get("/api/categories/{category_id}/", response_model=schemas.CategorySchema)
def get_category_by_id_endpoint(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category doesn't exist"
        )
    return category

#* Define o Endpoint para criar uma categoria (POST)
@app.post("/api/categories/", response_model=schemas.CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # Valida se categoria ja existe no banco através do nome.
    existing_category = crud.get_category_by_name(db, category_name=category.name)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category {category.name} already registered"
        )
    
    created_category = crud.create_category(db, category=category)

    return created_category

#* Define o Endpoint para atualizar uma categoria (PATCH)
@app.patch("/api/categories/{category_id}/")
def update_category_endpoint(category_id: int, category_update: schemas.CategoryPatch, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)

    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    updated_category = crud.update_category(db, db_category=db_category, category_update=category_update)
    return updated_category

#* Define o Endpoint para deletar uma categoria (DELETE)
@app.delete("/api/categories/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    
    deleted_category = crud.delete_category(db, category_id=category_id)
    if deleted_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist.")
    
    # Se o crud retornar o objeto, o FastAPI vai retornar o status_code 204 definido no decorador
    return