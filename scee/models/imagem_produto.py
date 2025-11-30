"""Módulo contendo a classe ImagemProduto."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ImagemProduto(Base):
    """
    Representa uma imagem de produto.
    
    Attributes:
        id (int): Identificador único da imagem.
        produto_id (int): ID do produto.
        caminho (str): Caminho do arquivo de imagem.
        ordem (int): Ordem de exibição.
        produto (Produto): Referência ao produto.
    """
    
    __tablename__ = 'imagens_produto'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    caminho = Column(String(500), nullable=False)
    ordem = Column(Integer, default=0)
    
    produto = relationship('Produto', back_populates='imagens')
    
    def __repr__(self):
        return f"<ImagemProduto(id={self.id}, produto_id={self.produto_id})>"
