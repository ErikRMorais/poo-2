"""Módulo contendo a classe ItemPedido."""

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base


class ItemPedido(Base):
    """
    Representa um item dentro de um pedido.
    
    Attributes:
        id (int): Identificador único do item.
        pedido_id (int): ID do pedido.
        produto_id (int): ID do produto.
        produto_nome (str): Nome do produto no momento da compra.
        quantidade (int): Quantidade comprada.
        preco_unitario (float): Preço unitário no momento da compra.
        subtotal (float): Subtotal do item.
        pedido (Pedido): Referência ao pedido.
        produto (Produto): Referência ao produto.
    """
    
    __tablename__ = 'itens_pedido'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    produto_nome = Column(String(200), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    pedido = relationship('Pedido', back_populates='itens')
    produto = relationship('Produto')
    
    def __repr__(self):
        return f"<ItemPedido(id={self.id}, pedido_id={self.pedido_id}, produto_nome='{self.produto_nome}')>"
