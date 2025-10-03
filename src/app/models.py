from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

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