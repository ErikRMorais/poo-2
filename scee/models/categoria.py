"""Módulo contendo a classe Categoria."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Categoria(Base):
    """
    Representa uma categoria de produtos.
    
    Attributes:
        id (int): Identificador único da categoria.
        nome (str): Nome da categoria.
        produtos (list): Lista de produtos da categoria.
    """
    
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)
    
    produtos = relationship('Produto', back_populates='categoria')
    
    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"
