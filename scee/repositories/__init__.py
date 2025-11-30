"""Módulo de repositórios do SCEE."""

from .base_repository import BaseRepository
from .cliente_repository import ClienteRepository
from .admin_repository import AdminRepository
from .produto_repository import ProdutoRepository
from .categoria_repository import CategoriaRepository
from .endereco_repository import EnderecoRepository
from .pedido_repository import PedidoRepository

__all__ = [
    'BaseRepository',
    'ClienteRepository',
    'AdminRepository',
    'ProdutoRepository',
    'CategoriaRepository',
    'EnderecoRepository',
    'PedidoRepository'
]
