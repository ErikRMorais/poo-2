"""Módulo contendo o controlador de Carrinho."""

from typing import Dict


class ItemCarrinho:
    """
    Representa um item no carrinho de compras.
    
    Attributes:
        produto_id (int): ID do produto.
        nome (str): Nome do produto.
        preco (float): Preço unitário.
        quantidade (int): Quantidade.
        subtotal (float): Subtotal do item.
    """
    
    def __init__(self, produto_id: int, nome: str, preco: float, quantidade: int):
        """
        Inicializa um item do carrinho.
        
        Args:
            produto_id: ID do produto.
            nome: Nome do produto.
            preco: Preço unitário.
            quantidade: Quantidade.
        """
        self.produto_id = produto_id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.subtotal = preco * quantidade
    
    def atualizar_quantidade(self, quantidade: int) -> None:
        """
        Atualiza a quantidade e recalcula o subtotal.
        
        Args:
            quantidade: Nova quantidade.
        """
        self.quantidade = quantidade
        self.subtotal = self.preco * quantidade


class CarrinhoController:
    """
    Controlador para gerenciamento do carrinho de compras.
    """
    
    def __init__(self):
        """
        Inicializa o controlador de carrinho.
        """
        self.itens: Dict[int, ItemCarrinho] = {}
    
    def adicionar_item(self, produto_id: int, nome: str, preco: float, quantidade: int = 1) -> tuple[bool, str]:
        """
        Adiciona um item ao carrinho.
        
        Args:
            produto_id: ID do produto.
            nome: Nome do produto.
            preco: Preço unitário.
            quantidade: Quantidade a adicionar.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero"
        
        if produto_id in self.itens:
            self.itens[produto_id].atualizar_quantidade(
                self.itens[produto_id].quantidade + quantidade
            )
        else:
            self.itens[produto_id] = ItemCarrinho(produto_id, nome, preco, quantidade)
        
        return True, "Item adicionado ao carrinho"
    
    def remover_item(self, produto_id: int) -> tuple[bool, str]:
        """
        Remove um item do carrinho.
        
        Args:
            produto_id: ID do produto.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        if produto_id not in self.itens:
            return False, "Item não encontrado no carrinho"
        
        del self.itens[produto_id]
        return True, "Item removido do carrinho"
    
    def atualizar_quantidade(self, produto_id: int, quantidade: int) -> tuple[bool, str]:
        """
        Atualiza a quantidade de um item.
        
        Args:
            produto_id: ID do produto.
            quantidade: Nova quantidade.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        if produto_id not in self.itens:
            return False, "Item não encontrado no carrinho"
        
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero"
        
        self.itens[produto_id].atualizar_quantidade(quantidade)
        return True, "Quantidade atualizada"
    
    def calcular_total(self) -> float:
        """
        Calcula o total do carrinho.
        
        Returns:
            Valor total.
        """
        return sum(item.subtotal for item in self.itens.values())
    
    def obter_itens(self) -> list:
        """
        Retorna todos os itens do carrinho.
        
        Returns:
            Lista de itens.
        """
        return list(self.itens.values())
    
    def limpar(self) -> None:
        """
        Limpa todos os itens do carrinho.
        """
        self.itens.clear()
    
    def quantidade_itens(self) -> int:
        """
        Retorna a quantidade total de itens.
        
        Returns:
            Quantidade de itens.
        """
        return sum(item.quantidade for item in self.itens.values())
