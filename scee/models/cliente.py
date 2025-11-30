"""Módulo contendo a classe Cliente."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Cliente(Base):
    """
    Representa um cliente do sistema.
    
    Attributes:
        id (int): Identificador único do cliente.
        nome (str): Nome completo do cliente.
        email (str): E-mail único do cliente.
        cpf (str): CPF único do cliente.
        senha_hash (str): Hash da senha do cliente.
        enderecos (list): Lista de endereços do cliente.
        pedidos (list): Lista de pedidos do cliente.
    """
    
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    
    enderecos = relationship('Endereco', back_populates='cliente', cascade='all, delete-orphan')
    pedidos = relationship('Pedido', back_populates='cliente')
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"
