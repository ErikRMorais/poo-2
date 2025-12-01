"""Configuração do banco de dados SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base

class Database:
    """Classe para gerenciar a conexão com o banco de dados."""
    
    def __init__(self, db_url='sqlite:///scee_loja.db'):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_url: URL de conexão do banco de dados
        """
        self.engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def create_tables(self):
        """Cria todas as tabelas no banco de dados."""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Retorna uma nova sessão do banco de dados.
        
        Returns:
            Session: Sessão do SQLAlchemy
        """
        return self.Session()
    
    def close_session(self):
        """Fecha a sessão atual."""
        self.Session.remove()
