"""Módulo contendo o repositório de Categoria."""

from typing import Optional
from sqlalchemy.orm import Session
from models.categoria import Categoria
from .base_repository import BaseRepository


class CategoriaRepository(BaseRepository[Categoria]):
    """
    Repositório para operações com Categoria.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Categoria.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Categoria, session)
    
    def get_by_nome(self, nome: str) -> Optional[Categoria]:
        """
        Busca uma categoria por nome.
        
        Args:
            nome: Nome da categoria.
            
        Returns:
            Categoria encontrada ou None.
        """
        return self.session.query(Categoria).filter(Categoria.nome == nome).first()
