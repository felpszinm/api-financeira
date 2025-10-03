from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional, Dict, Any



### ============ Funções de CRUD (USER) ============ ###

# Pega todos usuários (GET)
def get_users(db: Session):
    return db.query(models.User).all()

# Pega um usuário específico (GET)
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Pega um usuario pelo email (GET)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Cria um usuario (POST)
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Atualiza um usuario (PATCH)
def update_user(db: Session, db_user: models.User, user_update: schemas.UserPatch) -> Optional[models.User]:
    # Adiciona em um dicionário apenas os campos que vieram preenchidos.
    user_data: Dict[str, Any] = user_update.model_dump(exclude_unset=True)

    # Aplica a atualização
    for key, value in user_data.items():
        setattr(db_user, key, value)

    # Faz a alteração no banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Deleta um usuario (DELETE)
def delete_user(db: Session, user_id: int):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        return None
    
    deleted_user = user
    
    db.delete(user) # Deleta a informação
    db.commit() # Salva no banco
    return deleted_user

### ============ Funções de CRUD (TRANSACTIONS) ============ ###

# Pega todas as transações (GET)
def get_all_transactions_by_user(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.owner_id == user_id).all()

# Pega uma transação de um usuário (GET)
def get_transaction_by_user(db: Session, user_id: int, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.owner_id == user_id, models.Transaction.id == transaction_id).first() # Valida se o user_id é igual ao User.id do banco

# Cria uma transação (POST)
def create_transaction(db: Session, transaction: schemas.TransactionCreate, owner_id: int):

    # Criando uma nova transação
    db_transaction = models.Transaction(
        description=transaction.description,
        amount=transaction.amount,
        owner_id=owner_id,
        category_id=transaction.category_id
    )

    db.add(db_transaction) # Adiciona a transação ao banco
    db.commit() # Salva os dados da transação no banco
    db.refresh(db_transaction) # Atualiza a transação criada no Banco
    return db_transaction # Retorna o objeto para a FastAPI

def update_transaction(db: Session, db_transaction: models.Transaction, transaction_update: schemas.TransactionPatch):
    # Adiciona em um dicionário apenas os campos que vieram preenchidos.
    transaction_data = transaction_update.model_dump(exclude_unset=True, exclude_none=True) 

    # Atualiza os valores
    for key, value in transaction_data.items(): 
        setattr(db_transaction, key, value)

    db.commit() # Salva no banco
    db.refresh(db_transaction) # Atualiza uma transação de um usuário no Banco
    return db_transaction


# Deleta uma transação (DELETE)
def delete_transaction(user_id:int, transaction_id:int, db: Session):
    # Filtra a query do banco pelo id do usuario e id de transação igual ao do Banco.
    transaction = db.query(models.Transaction).filter(
        models.Transaction.owner_id == user_id, 
        models.Transaction.id == transaction_id
        ).first()
    
    if transaction is None:
        return None
    
    del_transaction = transaction

    db.delete(del_transaction) # Deleta a informação
    db.commit() # Salva no banco

    return del_transaction


### ============ Funções de CRUD (CATEGORIES) ============ ###

# Pega todas as categorias (GET)
def get_all_categories(db: Session):
    return db.query(models.Category).all()

# Pega a categoria pelo ID (GET)
def get_category_by_id(db: Session, category_id: int):
    # Busca uma categoria pelo ID
    return db.query(models.Category).filter(models.Category.id == category_id).first()

# Pega a categoria pelo nome (GET)
def get_category_by_name(db: Session, category_name: str):
    # Busca uma categoria pelo ID
    return db.query(models.Category).filter(models.Category.name == category_name).first()

# Cria uma categoria (POST)
def create_category(db: Session, category: schemas.CategoryCreate):
        
    # Criando uma nova categoria
    db_category = models.Category(name=category.name)
    db.add(db_category) # Adiciona a categoria ao banco.
    db.commit() # Salva o banco
    db.refresh(db_category) # Atualiza a categoria dentro do banco 
    return db_category

# Atualiza uma categoria existente (PATCH)
def update_category(db: Session, db_category: models.Category, category_update: schemas.CategoryPatch) -> Optional[models.Category]:
    # Adiciona em um dicionário apenas os campos que vieram preenchidos.
    category_data: Dict[str, Any] = category_update.model_dump(exclude_unset=True)

    # Aplica a atualização
    for key, value in category_data.items(): 
        setattr(db_category, key, value)

    db.commit() # Salva no banco
    db.refresh(db_category) # Atualiza uma alteração de uma categoria no Banco
    return db_category

# Deleta uma categoria (DELETE)
def delete_category(db: Session, category_id: int):
    del_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if del_category is None:
        return None

    deleted_category = del_category
    
    db.delete(del_category)
    db.commit()
    return deleted_category