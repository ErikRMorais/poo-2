"""Módulo contendo o repositório de Endereco."""

from typing import List
from sqlalchemy.orm import Session
from models.endereco import Endereco
from .base_repository import BaseRepository


class EnderecoRepository(BaseRepository[Endereco]):
    """
    Repositório para operações com Endereco.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Endereco.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Endereco, session)
    
    def get_by_cliente(self, cliente_id: int) -> List[Endereco]:
        """
        Busca todos os endereços de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            
        Returns:
            Lista de endereços do cliente.
        """
        return self.session.query(Endereco).filter(Endereco.cliente_id == cliente_id).all()
