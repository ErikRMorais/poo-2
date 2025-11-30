"""Módulo contendo a classe Produto."""

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Produto(Base):
    """
    Representa um produto do catálogo.
    
    Attributes:
        id (int): Identificador único do produto.
        nome (str): Nome do produto.
        sku (str): SKU único do produto.
        descricao (str): Descrição detalhada.
        preco (float): Preço unitário.
        estoque (int): Quantidade em estoque.
        categoria_id (int): ID da categoria.
        categoria (Categoria): Referência à categoria.
        imagens (list): Lista de imagens do produto.
    """
    
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    
    categoria = relationship('Categoria', back_populates='produtos')
    imagens = relationship('ImagemProduto', back_populates='produto', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', sku='{self.sku}')>"
