"""Módulo contendo o controlador de Produto."""

import os
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from models.produto import Produto
from models.imagem_produto import ImagemProduto
from repositories.produto_repository import ProdutoRepository
from repositories.categoria_repository import CategoriaRepository


class ProdutoController:
    """
    Controlador para gerenciamento de produtos.
    """
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    MAX_IMAGES = 5
    
    def __init__(self, session: Session, upload_folder: str):
        """
        Inicializa o controlador de produto.
        
        Args:
            session: Sessão do SQLAlchemy.
            upload_folder: Pasta para upload de imagens.
        """
        self.session = session
        self.produto_repo = ProdutoRepository(session)
        self.categoria_repo = CategoriaRepository(session)
        self.upload_folder = upload_folder
    
    def validar_extensao(self, filename: str) -> bool:
        """
        Valida a extensão do arquivo.
        
        Args:
            filename: Nome do arquivo.
            
        Returns:
            True se válido, False caso contrário.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def criar_produto(self, nome: str, sku: str, descricao: str, preco: float,
                     estoque: int, categoria_id: int, imagens: list = None) -> tuple[bool, str, Produto]:
        """
        Cria um novo produto.
        
        Args:
            nome: Nome do produto.
            sku: SKU único.
            descricao: Descrição.
            preco: Preço unitário.
            estoque: Quantidade em estoque.
            categoria_id: ID da categoria.
            imagens: Lista de arquivos de imagem.
            
        Returns:
            Tupla (sucesso, mensagem, produto).
        """
        if not all([nome, sku, descricao]):
            return False, "Nome, SKU e descrição são obrigatórios", None
        
        if preco <= 0:
            return False, "Preço deve ser maior que zero", None
        
        if estoque < 0:
            return False, "Estoque não pode ser negativo", None
        
        if self.produto_repo.sku_exists(sku):
            return False, "SKU já cadastrado", None
        
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            return False, "Categoria não encontrada", None
        
        produto = Produto(
            nome=nome,
            sku=sku,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            categoria_id=categoria_id
        )
        
        produto = self.produto_repo.create(produto)
        
        if imagens:
            self._salvar_imagens(produto, imagens)
        
        return True, "Produto criado com sucesso", produto
    
    def _salvar_imagens(self, produto: Produto, imagens: list) -> None:
        """
        Salva imagens do produto.
        
        Args:
            produto: Produto.
            imagens: Lista de arquivos de imagem.
        """
        for i, imagem in enumerate(imagens[:self.MAX_IMAGES]):
            if imagem and self.validar_extensao(imagem.filename):
                filename = secure_filename(f"{produto.sku}_{i}_{imagem.filename}")
                filepath = os.path.join(self.upload_folder, filename)
                imagem.save(filepath)
                
                # Salvar apenas o caminho relativo (uploads/filename)
                caminho_relativo = f"uploads/{filename}"
                
                img_produto = ImagemProduto(
                    produto_id=produto.id,
                    caminho=caminho_relativo,
                    ordem=i
                )
                self.session.add(img_produto)
        
        self.session.commit()
    
    def atualizar_produto(self, produto_id: int, nome: str, descricao: str, preco: float,
                         estoque: int, categoria_id: int, novas_imagens: list = None) -> tuple[bool, str]:
        """
        Atualiza um produto existente.
        
        Args:
            produto_id: ID do produto.
            nome: Nome do produto.
            descricao: Descrição.
            preco: Preço unitário.
            estoque: Quantidade em estoque.
            categoria_id: ID da categoria.
            novas_imagens: Lista opcional de novas imagens para adicionar.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        produto = self.produto_repo.get_by_id(produto_id)
        if not produto:
            return False, "Produto não encontrado"
        
        if not all([nome, descricao]):
            return False, "Nome e descrição são obrigatórios"
        
        if preco <= 0:
            return False, "Preço deve ser maior que zero"
        
        if estoque < 0:
            return False, "Estoque não pode ser negativo"
        
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            return False, "Categoria não encontrada"
        
        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.estoque = estoque
        produto.categoria_id = categoria_id
        
        self.produto_repo.update(produto)
        
        # Adicionar novas imagens se fornecidas
        if novas_imagens:
            self._adicionar_imagens(produto, novas_imagens)
        
        return True, "Produto atualizado com sucesso"
    
    def remover_produto(self, produto_id: int) -> tuple[bool, str]:
        """
        Remove um produto.
        
        Args:
            produto_id: ID do produto.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        produto = self.produto_repo.get_by_id(produto_id)
        if not produto:
            return False, "Produto não encontrado"
        
        self.produto_repo.delete(produto)
        return True, "Produto removido com sucesso"
    
    def listar_produtos(self, page: int = 1, per_page: int = 12):
        """
        Lista produtos com paginação.
        
        Args:
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Tupla (produtos, total, páginas).
        """
        offset = (page - 1) * per_page
        produtos = self.produto_repo.get_paginated(limit=per_page, offset=offset)
        total = self.produto_repo.count_all()
        total_pages = (total + per_page - 1) // per_page
        return produtos, total, total_pages
    
    def listar_por_categoria(self, categoria_id: int, page: int = 1, per_page: int = 12):
        """
        Lista produtos por categoria com paginação.
        
        Args:
            categoria_id: ID da categoria.
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Tupla (produtos, total, páginas).
        """
        offset = (page - 1) * per_page
        produtos = self.produto_repo.get_by_categoria(categoria_id, limit=per_page, offset=offset)
        total = self.produto_repo.count_by_categoria(categoria_id)
        total_pages = (total + per_page - 1) // per_page
        return produtos, total, total_pages
    
    def buscar_produtos(self, query: str, page: int = 1, per_page: int = 12):
        """
        Busca produtos por texto.
        
        Args:
            query: Texto de busca.
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Lista de produtos.
        """
        offset = (page - 1) * per_page
        return self.produto_repo.search(query, limit=per_page, offset=offset)
    
    def filtrar_por_preco(self, min_price: float, max_price: float, page: int = 1, per_page: int = 12):
        """
        Filtra produtos por faixa de preço.
        
        Args:
            min_price: Preço mínimo.
            max_price: Preço máximo.
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Lista de produtos.
        """
        offset = (page - 1) * per_page
        return self.produto_repo.filter_by_price_range(min_price, max_price, limit=per_page, offset=offset)
    
    def filtrar_por_categoria_e_preco(self, categoria_id: int, min_price: float, max_price: float, 
                                      page: int = 1, per_page: int = 12):
        """
        Filtra produtos por categoria E faixa de preço simultaneamente.
        
        Args:
            categoria_id: ID da categoria.
            min_price: Preço mínimo.
            max_price: Preço máximo.
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Lista de produtos.
        """
        offset = (page - 1) * per_page
        return self.produto_repo.filter_by_categoria_and_price(
            categoria_id, min_price, max_price, limit=per_page, offset=offset
        )
    
    def _adicionar_imagens(self, produto: Produto, imagens: list) -> None:
        """
        Adiciona novas imagens a um produto existente.
        
        Args:
            produto: Produto.
            imagens: Lista de arquivos de imagem.
        """
        # Contar imagens existentes
        imagens_existentes = len(produto.imagens)
        
        # Calcular quantas imagens podemos adicionar
        espaco_disponivel = self.MAX_IMAGES - imagens_existentes
        
        if espaco_disponivel <= 0:
            return  # Já tem 5 imagens
        
        # Adicionar novas imagens
        for i, imagem in enumerate(imagens[:espaco_disponivel]):
            if imagem and self.validar_extensao(imagem.filename):
                ordem = imagens_existentes + i
                filename = secure_filename(f"{produto.sku}_{ordem}_{imagem.filename}")
                filepath = os.path.join(self.upload_folder, filename)
                imagem.save(filepath)
                
                caminho_relativo = f"uploads/{filename}"
                
                img_produto = ImagemProduto(
                    produto_id=produto.id,
                    caminho=caminho_relativo,
                    ordem=ordem
                )
                self.session.add(img_produto)
        
        self.session.commit()
    
    def remover_imagem(self, imagem_id: int) -> tuple[bool, str]:
        """
        Remove uma imagem de produto.
        
        Args:
            imagem_id: ID da imagem.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        imagem = self.session.query(ImagemProduto).filter(
            ImagemProduto.id == imagem_id
        ).first()
        
        if not imagem:
            return False, "Imagem não encontrada"
        
        # Remover arquivo físico
        try:
            filepath = os.path.join('static', imagem.caminho)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Erro ao remover arquivo: {e}")
        
        # Remover do banco
        self.session.delete(imagem)
        self.session.commit()
        
        return True, "Imagem removida com sucesso"
