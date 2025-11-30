"""Módulo contendo o controlador de Pedido."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository
from repositories.endereco_repository import EnderecoRepository


class PedidoController:
    """
    Controlador para gerenciamento de pedidos.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o controlador de pedido.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        self.session = session
        self.pedido_repo = PedidoRepository(session)
        self.produto_repo = ProdutoRepository(session)
        self.endereco_repo = EnderecoRepository(session)
    
    def criar_pedido(self, cliente_id: int, itens_carrinho: list, endereco_id: int,
                    metodo_pagamento: str) -> tuple[bool, str, Pedido]:
        """
        Cria um novo pedido de forma atômica.
        
        Args:
            cliente_id: ID do cliente.
            itens_carrinho: Lista de itens do carrinho.
            endereco_id: ID do endereço de entrega.
            metodo_pagamento: Método de pagamento (Cartão/Pix).
            
        Returns:
            Tupla (sucesso, mensagem, pedido).
        """
        if not itens_carrinho:
            return False, "Carrinho vazio", None
        
        if metodo_pagamento not in ['Cartão', 'Pix']:
            return False, "Método de pagamento inválido", None
        
        endereco = self.endereco_repo.get_by_id(endereco_id)
        if not endereco or endereco.cliente_id != cliente_id:
            return False, "Endereço inválido", None
        
        try:
            self.session.begin_nested()
            
            total = 0
            itens_pedido = []
            
            for item in itens_carrinho:
                produto = self.produto_repo.get_by_id(item.produto_id)
                
                if not produto:
                    self.session.rollback()
                    return False, f"Produto {item.nome} não encontrado", None
                
                if produto.estoque < item.quantidade:
                    self.session.rollback()
                    return False, f"Estoque insuficiente para {produto.nome}", None
                
                produto.estoque -= item.quantidade
                
                subtotal = produto.preco * item.quantidade
                total += subtotal
                
                item_pedido = ItemPedido(
                    produto_id=produto.id,
                    produto_nome=produto.nome,
                    quantidade=item.quantidade,
                    preco_unitario=produto.preco,
                    subtotal=subtotal
                )
                itens_pedido.append(item_pedido)
            
            endereco_completo = f"{endereco.rua}, {endereco.numero}, {endereco.bairro}, {endereco.cidade}/{endereco.estado}, CEP: {endereco.cep}"
            if endereco.complemento:
                endereco_completo = f"{endereco.rua}, {endereco.numero} ({endereco.complemento}), {endereco.bairro}, {endereco.cidade}/{endereco.estado}, CEP: {endereco.cep}"
            
            pedido = Pedido(
                cliente_id=cliente_id,
                total=total,
                endereco_entrega=endereco_completo,
                metodo_pagamento=metodo_pagamento,
                status='Pendente'
            )
            
            pedido = self.pedido_repo.create(pedido)
            
            for item in itens_pedido:
                item.pedido_id = pedido.id
                self.session.add(item)
            
            self.session.commit()
            
            return True, "Pedido criado com sucesso", pedido
            
        except SQLAlchemyError as e:
            self.session.rollback()
            return False, f"Erro ao criar pedido: {str(e)}", None
    
    def listar_pedidos_cliente(self, cliente_id: int):
        """
        Lista todos os pedidos de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            
        Returns:
            Lista de pedidos.
        """
        return self.pedido_repo.get_by_cliente(cliente_id)
    
    def listar_todos_pedidos(self, page: int = 1, per_page: int = 50):
        """
        Lista todos os pedidos com paginação (admin).
        
        Args:
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Tupla (pedidos, total, páginas).
        """
        offset = (page - 1) * per_page
        pedidos = self.pedido_repo.get_paginated(limit=per_page, offset=offset)
        total = self.pedido_repo.count_all()
        total_pages = (total + per_page - 1) // per_page
        return pedidos, total, total_pages
    
    def filtrar_por_status(self, status: str, page: int = 1, per_page: int = 50):
        """
        Filtra pedidos por status (admin).
        
        Args:
            status: Status do pedido.
            page: Número da página.
            per_page: Itens por página.
            
        Returns:
            Tupla (pedidos, total, páginas).
        """
        offset = (page - 1) * per_page
        pedidos = self.pedido_repo.get_by_status(status, limit=per_page, offset=offset)
        total = self.pedido_repo.count_by_status(status)
        total_pages = (total + per_page - 1) // per_page
        return pedidos, total, total_pages
    
    def atualizar_status(self, pedido_id: int, novo_status: str) -> tuple[bool, str]:
        """
        Atualiza o status de um pedido (admin).
        
        Args:
            pedido_id: ID do pedido.
            novo_status: Novo status.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        status_validos = ['Pendente', 'Processando', 'Enviado', 'Entregue', 'Cancelado']
        
        if novo_status not in status_validos:
            return False, "Status inválido"
        
        pedido = self.pedido_repo.get_by_id(pedido_id)
        if not pedido:
            return False, "Pedido não encontrado"
        
        pedido.status = novo_status
        self.pedido_repo.update(pedido)
        return True, "Status atualizado com sucesso"
    
    def obter_pedido(self, pedido_id: int):
        """
        Obtém um pedido por ID.
        
        Args:
            pedido_id: ID do pedido.
            
        Returns:
            Pedido ou None.
        """
        return self.pedido_repo.get_by_id(pedido_id)
