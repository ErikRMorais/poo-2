"""Módulo contendo a classe Admin."""

from sqlalchemy import Column, Integer, String
from .base import Base


class Admin(Base):
    """
    Representa um administrador do sistema.
    
    Attributes:
        id (int): Identificador único do admin.
        nome (str): Nome do administrador.
        email (str): E-mail único do administrador.
        senha_hash (str): Hash da senha do administrador.
    """
    
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<Admin(id={self.id}, nome='{self.nome}', email='{self.email}')>"
