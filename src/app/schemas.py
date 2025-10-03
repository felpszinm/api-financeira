from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
