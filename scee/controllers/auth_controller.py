"""Módulo contendo o controlador de autenticação."""

import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session
from models.cliente import Cliente
from models.admin import Admin
from repositories.cliente_repository import ClienteRepository
from repositories.admin_repository import AdminRepository


class AuthController:
    """
    Controlador para autenticação e gerenciamento de contas.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o controlador de autenticação.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        self.session = session
        self.cliente_repo = ClienteRepository(session)
        self.admin_repo = AdminRepository(session)
        self.ph = PasswordHasher()
    
    def validar_email(self, email: str) -> bool:
        """
        Valida formato de e-mail.
        
        Args:
            email: E-mail a validar.
            
        Returns:
            True se válido, False caso contrário.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validar_cpf(self, cpf: str) -> bool:
        """
        Valida formato e dígitos verificadores do CPF.
        
        Args:
            cpf: CPF a validar (apenas números).
            
        Returns:
            True se válido, False caso contrário.
        """
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
        if int(cpf[9]) != digito1:
            return False
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        return int(cpf[10]) == digito2
    
    def validar_senha_forte(self, senha: str) -> tuple[bool, str]:
        """
        Valida se a senha é forte.
        
        Args:
            senha: Senha a validar.
            
        Returns:
            Tupla (válida, mensagem de erro).
        """
        if len(senha) < 8:
            return False, "Senha deve ter no mínimo 8 caracteres"
        if not re.search(r'[A-Z]', senha):
            return False, "Senha deve conter ao menos uma letra maiúscula"
        if not re.search(r'[a-z]', senha):
            return False, "Senha deve conter ao menos uma letra minúscula"
        if not re.search(r'[0-9]', senha):
            return False, "Senha deve conter ao menos um número"
        return True, ""
    
    def registrar_cliente(self, nome: str, email: str, cpf: str, senha: str, confirmar_senha: str) -> tuple[bool, str, Cliente]:
        """
        Registra um novo cliente.
        
        Args:
            nome: Nome completo.
            email: E-mail.
            cpf: CPF (apenas números).
            senha: Senha.
            confirmar_senha: Confirmação da senha.
            
        Returns:
            Tupla (sucesso, mensagem, cliente).
        """
        if not nome or not email or not cpf or not senha:
            return False, "Todos os campos são obrigatórios", None
        
        if senha != confirmar_senha:
            return False, "As senhas não coincidem", None
        
        if not self.validar_email(email):
            return False, "E-mail inválido", None
        
        if not self.validar_cpf(cpf):
            return False, "CPF inválido", None
        
        valida_senha, msg_senha = self.validar_senha_forte(senha)
        if not valida_senha:
            return False, msg_senha, None
        
        if self.cliente_repo.email_exists(email):
            return False, "E-mail já cadastrado", None
        
        if self.cliente_repo.cpf_exists(cpf):
            return False, "CPF já cadastrado", None
        
        senha_hash = self.ph.hash(senha)
        
        cliente = Cliente(
            nome=nome,
            email=email,
            cpf=cpf,
            senha_hash=senha_hash
        )
        
        cliente = self.cliente_repo.create(cliente)
        return True, "Cliente registrado com sucesso", cliente
    
    def login_cliente(self, email: str, senha: str) -> tuple[bool, str, Cliente]:
        """
        Autentica um cliente.
        
        Args:
            email: E-mail do cliente.
            senha: Senha do cliente.
            
        Returns:
            Tupla (sucesso, mensagem, cliente).
        """
        if not email or not senha:
            return False, "E-mail e senha são obrigatórios", None
        
        cliente = self.cliente_repo.get_by_email(email)
        if not cliente:
            return False, "E-mail ou senha incorretos", None
        
        try:
            self.ph.verify(cliente.senha_hash, senha)
            return True, "Login realizado com sucesso", cliente
        except VerifyMismatchError:
            return False, "E-mail ou senha incorretos", None
    
    def login_admin(self, email: str, senha: str) -> tuple[bool, str, Admin]:
        """
        Autentica um administrador.
        
        Args:
            email: E-mail do admin.
            senha: Senha do admin.
            
        Returns:
            Tupla (sucesso, mensagem, admin).
        """
        if not email or not senha:
            return False, "E-mail e senha são obrigatórios", None
        
        admin = self.admin_repo.get_by_email(email)
        if not admin:
            return False, "E-mail ou senha incorretos", None
        
        try:
            self.ph.verify(admin.senha_hash, senha)
            return True, "Login realizado com sucesso", admin
        except VerifyMismatchError:
            return False, "E-mail ou senha incorretos", None
