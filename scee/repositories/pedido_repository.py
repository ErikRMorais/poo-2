"""Módulo contendo o repositório de Pedido."""

from typing import List
from sqlalchemy.orm import Session
from models.pedido import Pedido
from .base_repository import BaseRepository


class PedidoRepository(BaseRepository[Pedido]):
    """
    Repositório para operações com Pedido.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Pedido.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Pedido, session)
    
    def get_by_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Busca todos os pedidos de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            
        Returns:
            Lista de pedidos do cliente.
        """
        return self.session.query(Pedido).filter(Pedido.cliente_id == cliente_id).order_by(Pedido.data_pedido.desc()).all()
    
    def get_by_status(self, status: str, limit: int = 50, offset: int = 0) -> List[Pedido]:
        """
        Busca pedidos por status com paginação.
        
        Args:
            status: Status do pedido.
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de pedidos.
        """
        return self.session.query(Pedido).filter(Pedido.status == status).order_by(Pedido.data_pedido.desc()).limit(limit).offset(offset).all()
    
    def get_paginated(self, limit: int = 50, offset: int = 0) -> List[Pedido]:
        """
        Retorna pedidos paginados.
        
        Args:
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de pedidos.
        """
        return self.session.query(Pedido).order_by(Pedido.data_pedido.desc()).limit(limit).offset(offset).all()
    
    def count_all(self) -> int:
        """
        Conta o total de pedidos.
        
        Returns:
            Número total de pedidos.
        """
        return self.session.query(Pedido).count()
    
    def count_by_status(self, status: str) -> int:
        """
        Conta pedidos por status.
        
        Args:
            status: Status do pedido.
            
        Returns:
            Número de pedidos com o status.
        """
        return self.session.query(Pedido).filter(Pedido.status == status).count()
