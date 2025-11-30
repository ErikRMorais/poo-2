"""Módulo contendo a classe Pedido."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Pedido(Base):
    """
    Representa um pedido de compra.
    
    Attributes:
        id (int): Identificador único do pedido.
        cliente_id (int): ID do cliente.
        data_pedido (datetime): Data e hora do pedido.
        status (str): Status do pedido.
        total (float): Valor total do pedido.
        endereco_entrega (str): Endereço de entrega completo.
        metodo_pagamento (str): Método de pagamento utilizado.
        cliente (Cliente): Referência ao cliente.
        itens (list): Lista de itens do pedido.
    """
    
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data_pedido = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), default='Pendente', nullable=False)
    total = Column(Float, nullable=False)
    endereco_entrega = Column(String(500), nullable=False)
    metodo_pagamento = Column(String(50), nullable=False)
    
    cliente = relationship('Cliente', back_populates='pedidos')
    itens = relationship('ItemPedido', back_populates='pedido', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, status='{self.status}')>"
