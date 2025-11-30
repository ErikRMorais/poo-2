"""Módulo contendo o repositório de Produto."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.produto import Produto
from .base_repository import BaseRepository


class ProdutoRepository(BaseRepository[Produto]):
    """
    Repositório para operações com Produto.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o repositório de Produto.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        super().__init__(Produto, session)
    
    def get_by_sku(self, sku: str) -> Optional[Produto]:
        """
        Busca um produto por SKU.
        
        Args:
            sku: SKU do produto.
            
        Returns:
            Produto encontrado ou None.
        """
        return self.session.query(Produto).filter(Produto.sku == sku).first()
    
    def sku_exists(self, sku: str) -> bool:
        """
        Verifica se um SKU já está cadastrado.
        
        Args:
            sku: SKU a verificar.
            
        Returns:
            True se existe, False caso contrário.
        """
        return self.session.query(Produto).filter(Produto.sku == sku).count() > 0
    
    def get_by_categoria(self, categoria_id: int, limit: int = 12, offset: int = 0) -> List[Produto]:
        """
        Busca produtos por categoria com paginação.
        
        Args:
            categoria_id: ID da categoria.
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de produtos.
        """
        return self.session.query(Produto).filter(
            Produto.categoria_id == categoria_id
        ).limit(limit).offset(offset).all()
    
    def search(self, query: str, limit: int = 12, offset: int = 0) -> List[Produto]:
        """
        Busca produtos por texto no nome ou descrição.
        
        Args:
            query: Texto de busca.
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de produtos.
        """
        search_pattern = f"%{query}%"
        return self.session.query(Produto).filter(
            or_(
                Produto.nome.ilike(search_pattern),
                Produto.descricao.ilike(search_pattern)
            )
        ).limit(limit).offset(offset).all()
    
    def filter_by_price_range(self, min_price: float, max_price: float, limit: int = 12, offset: int = 0) -> List[Produto]:
        """
        Filtra produtos por faixa de preço.
        
        Args:
            min_price: Preço mínimo.
            max_price: Preço máximo.
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de produtos.
        """
        return self.session.query(Produto).filter(
            Produto.preco >= min_price,
            Produto.preco <= max_price
        ).limit(limit).offset(offset).all()
    
    def get_paginated(self, limit: int = 12, offset: int = 0) -> List[Produto]:
        """
        Retorna produtos paginados.
        
        Args:
            limit: Número máximo de resultados.
            offset: Deslocamento para paginação.
            
        Returns:
            Lista de produtos.
        """
        return self.session.query(Produto).limit(limit).offset(offset).all()
    
    def count_all(self) -> int:
        """
        Conta o total de produtos.
        
        Returns:
            Número total de produtos.
        """
        return self.session.query(Produto).count()
    
    def count_by_categoria(self, categoria_id: int) -> int:
        """
        Conta produtos por categoria.
        
        Args:
            categoria_id: ID da categoria.
            
        Returns:
            Número de produtos na categoria.
        """
        return self.session.query(Produto).filter(Produto.categoria_id == categoria_id).count()
