"""Módulo de configuração do banco de dados."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from models.cliente import Cliente
from models.admin import Admin
from models.endereco import Endereco
from models.categoria import Categoria
from models.produto import Produto
from models.imagem_produto import ImagemProduto
from models.pedido import Pedido
from models.item_pedido import ItemPedido


class Database:
    """
    Gerenciador de conexão com o banco de dados SQLite.
    """
    
    def __init__(self, db_path: str = 'scee_loja.db'):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho do arquivo do banco de dados.
        """
        self.engine = create_engine(
            f'sqlite:///{db_path}',
            echo=False,
            connect_args={'check_same_thread': False}
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
    
    def create_tables(self):
        """
        Cria todas as tabelas no banco de dados.
        """
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Retorna uma nova sessão do banco de dados.
        
        Returns:
            Sessão do SQLAlchemy.
        """
        return self.Session()
    
    def close_session(self):
        """
        Fecha a sessão atual.
        """
        self.Session.remove()
