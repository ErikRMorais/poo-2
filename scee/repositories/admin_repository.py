"""Módulo contendo o repositório de Admin."""

from typing import Optional
from sqlalchemy.orm import Session
from models.admin import Admin
from .base_repository import BaseRepository


class AdminRepository(BaseRepository[Admin]):
    """
    Repositório para operações com Admin.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Admin.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Admin, session)
    
    def get_by_email(self, email: str) -> Optional[Admin]:
        """
        Busca um admin por e-mail.
        
        Args:
            email: E-mail do admin.
            
        Returns:
            Admin encontrado ou None.
        """
        return self.session.query(Admin).filter(Admin.email == email).first()
