"""Módulo contendo o controlador de Cliente."""

from sqlalchemy.orm import Session
from models.endereco import Endereco
from repositories.cliente_repository import ClienteRepository
from repositories.endereco_repository import EnderecoRepository


class ClienteController:
    """
    Controlador para gerenciamento de perfil de cliente.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o controlador de cliente.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        self.session = session
        self.cliente_repo = ClienteRepository(session)
        self.endereco_repo = EnderecoRepository(session)
    
    def atualizar_nome(self, cliente_id: int, novo_nome: str) -> tuple[bool, str]:
        """
        Atualiza o nome do cliente.
        
        Args:
            cliente_id: ID do cliente.
            novo_nome: Novo nome.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        if not novo_nome:
            return False, "Nome não pode ser vazio"
        
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            return False, "Cliente não encontrado"
        
        cliente.nome = novo_nome
        self.cliente_repo.update(cliente)
        return True, "Nome atualizado com sucesso"
    
    def adicionar_endereco(self, cliente_id: int, rua: str, numero: str, complemento: str,
                          bairro: str, cidade: str, estado: str, cep: str) -> tuple[bool, str, Endereco]:
        """
        Adiciona um novo endereço ao cliente.
        
        Args:
            cliente_id: ID do cliente.
            rua: Nome da rua.
            numero: Número do imóvel.
            complemento: Complemento.
            bairro: Bairro.
            cidade: Cidade.
            estado: Estado (UF).
            cep: CEP (apenas números).
            
        Returns:
            Tupla (sucesso, mensagem, endereco).
        """
        if not all([rua, numero, bairro, cidade, estado, cep]):
            return False, "Todos os campos obrigatórios devem ser preenchidos", None
        
        if len(estado) != 2:
            return False, "Estado deve ter 2 caracteres (UF)", None
        
        if len(cep) != 8 or not cep.isdigit():
            return False, "CEP inválido", None
        
        endereco = Endereco(
            cliente_id=cliente_id,
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado.upper(),
            cep=cep
        )
        
        endereco = self.endereco_repo.create(endereco)
        return True, "Endereço adicionado com sucesso", endereco
    
    def listar_enderecos(self, cliente_id: int):
        """
        Lista todos os endereços de um cliente.
        
        Args:
            cliente_id: ID do cliente.
            
        Returns:
            Lista de endereços.
        """
        return self.endereco_repo.get_by_cliente(cliente_id)
    
    def atualizar_endereco(self, endereco_id: int, rua: str, numero: str, complemento: str,
                          bairro: str, cidade: str, estado: str, cep: str) -> tuple[bool, str]:
        """
        Atualiza um endereço existente.
        
        Args:
            endereco_id: ID do endereço.
            rua: Nome da rua.
            numero: Número do imóvel.
            complemento: Complemento.
            bairro: Bairro.
            cidade: Cidade.
            estado: Estado (UF).
            cep: CEP (apenas números).
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        endereco = self.endereco_repo.get_by_id(endereco_id)
        if not endereco:
            return False, "Endereço não encontrado"
        
        if not all([rua, numero, bairro, cidade, estado, cep]):
            return False, "Todos os campos obrigatórios devem ser preenchidos"
        
        if len(estado) != 2:
            return False, "Estado deve ter 2 caracteres (UF)"
        
        if len(cep) != 8 or not cep.isdigit():
            return False, "CEP inválido"
        
        endereco.rua = rua
        endereco.numero = numero
        endereco.complemento = complemento
        endereco.bairro = bairro
        endereco.cidade = cidade
        endereco.estado = estado.upper()
        endereco.cep = cep
        
        self.endereco_repo.update(endereco)
        return True, "Endereço atualizado com sucesso"
    
    def remover_endereco(self, endereco_id: int) -> tuple[bool, str]:
        """
        Remove um endereço.
        
        Args:
            endereco_id: ID do endereço.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        endereco = self.endereco_repo.get_by_id(endereco_id)
        if not endereco:
            return False, "Endereço não encontrado"
        
        self.endereco_repo.delete(endereco)
        return True, "Endereço removido com sucesso"
