"""Módulo contendo a classe Endereco."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Endereco(Base):
    """
    Representa um endereço de entrega de um cliente.
    
    Attributes:
        id (int): Identificador único do endereço.
        cliente_id (int): ID do cliente proprietário.
        rua (str): Nome da rua.
        numero (str): Número do imóvel.
        complemento (str): Complemento do endereço.
        bairro (str): Bairro.
        cidade (str): Cidade.
        estado (str): Estado (UF).
        cep (str): CEP.
        cliente (Cliente): Referência ao cliente.
    """
    
    __tablename__ = 'enderecos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False)
    rua = Column(String(200), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(8), nullable=False)
    
    cliente = relationship('Cliente', back_populates='enderecos')
    
    def __repr__(self):
        return f"<Endereco(id={self.id}, rua='{self.rua}', numero='{self.numero}')>"
