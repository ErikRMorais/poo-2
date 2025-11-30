"""Módulo contendo o repositório de Cliente."""

from typing import Optional
from sqlalchemy.orm import Session
from models.cliente import Cliente
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    """
    Repositório para operações com Cliente.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Cliente.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Cliente, session)
    
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca um cliente por e-mail.
        
        Args:
            email: E-mail do cliente.
            
        Returns:
            Cliente encontrado ou None.
        """
        return self.session.query(Cliente).filter(Cliente.email == email).first()
    
    def get_by_cpf(self, cpf: str) -> Optional[Cliente]:
        """
        Busca um cliente por CPF.
        
        Args:
            cpf: CPF do cliente.
            
        Returns:
            Cliente encontrado ou None.
        """
        return self.session.query(Cliente).filter(Cliente.cpf == cpf).first()
    
    def email_exists(self, email: str) -> bool:
        """
        Verifica se um e-mail já está cadastrado.
        
        Args:
            email: E-mail a verificar.
            
        Returns:
            True se existe, False caso contrário.
        """
        return self.session.query(Cliente).filter(Cliente.email == email).count() > 0
    
    def cpf_exists(self, cpf: str) -> bool:
        """
        Verifica se um CPF já está cadastrado.
        
        Args:
            cpf: CPF a verificar.
            
        Returns:
            True se existe, False caso contrário.
        """
        return self.session.query(Cliente).filter(Cliente.cpf == cpf).count() > 0
