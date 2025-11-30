"""Módulo de integração com serviços externos (Polimorfismo)."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class GatewayPagamentoBase(ABC):
    """
    Classe abstrata base para gateways de pagamento.
    
    Demonstra o princípio de Polimorfismo da POO, permitindo que diferentes
    implementações de pagamento (PagSeguro, Stripe, etc.) compartilhem a mesma interface.
    """
    
    @abstractmethod
    def processar_pagamento(self, valor: float, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Processa um pagamento.
        
        Args:
            valor: Valor total do pagamento.
            dados_pagamento: Dicionário com dados do pagamento (cartão, titular, etc.).
            
        Returns:
            Tupla (sucesso: bool, mensagem: str).
        """
        pass
    
    @abstractmethod
    def validar_dados_pagamento(self, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Valida os dados de pagamento antes de processar.
        
        Args:
            dados_pagamento: Dicionário com dados do pagamento.
            
        Returns:
            Tupla (valido: bool, mensagem: str).
        """
        pass


class PagamentoCartao(GatewayPagamentoBase):
    """
    Implementação concreta para pagamento via Cartão de Crédito.
    
    Demonstra Polimorfismo: herda de GatewayPagamentoBase e implementa
    seus métodos abstratos de forma específica para cartão.
    """
    
    def processar_pagamento(self, valor: float, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Processa pagamento via cartão de crédito.
        
        Args:
            valor: Valor total.
            dados_pagamento: Deve conter 'numero_cartao', 'cvv', 'validade', 'titular'.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        # Validar dados primeiro
        valido, mensagem = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, mensagem
        
        # Simulação de processamento (em produção, chamaria API do gateway)
        # Aqui apenas simulamos aprovação se o valor for menor que 10000
        if valor > 10000:
            return False, "Pagamento recusado: valor acima do limite"
        
        return True, "Pagamento aprovado"
    
    def validar_dados_pagamento(self, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Valida dados do cartão.
        
        Args:
            dados_pagamento: Dicionário com dados do cartão.
            
        Returns:
            Tupla (valido, mensagem).
        """
        campos_obrigatorios = ['numero_cartao', 'cvv', 'validade', 'titular']
        
        for campo in campos_obrigatorios:
            if campo not in dados_pagamento or not dados_pagamento[campo]:
                return False, f"Campo obrigatório ausente: {campo}"
        
        # Validar número do cartão (deve ter 16 dígitos)
        numero_cartao = str(dados_pagamento['numero_cartao']).replace(' ', '')
        if not numero_cartao.isdigit() or len(numero_cartao) != 16:
            return False, "Número do cartão inválido"
        
        # Validar CVV (3 ou 4 dígitos)
        cvv = str(dados_pagamento['cvv'])
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            return False, "CVV inválido"
        
        return True, "Dados válidos"


class PagamentoPix(GatewayPagamentoBase):
    """
    Implementação concreta para pagamento via Pix.
    
    Demonstra Polimorfismo: mesma interface que PagamentoCartao,
    mas comportamento diferente.
    """
    
    def processar_pagamento(self, valor: float, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Processa pagamento via Pix.
        
        Args:
            valor: Valor total.
            dados_pagamento: Deve conter 'cpf_pagador'.
            
        Returns:
            Tupla (sucesso, mensagem).
        """
        valido, mensagem = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, mensagem
        
        # Simulação: Pix sempre aprovado (em produção, geraria QR Code e aguardaria confirmação)
        return True, "Pagamento via Pix aprovado"
    
    def validar_dados_pagamento(self, dados_pagamento: Dict[str, Any]) -> tuple[bool, str]:
        """
        Valida dados do Pix.
        
        Args:
            dados_pagamento: Dicionário com CPF do pagador.
            
        Returns:
            Tupla (valido, mensagem).
        """
        if 'cpf_pagador' not in dados_pagamento or not dados_pagamento['cpf_pagador']:
            return False, "CPF do pagador é obrigatório"
        
        cpf = str(dados_pagamento['cpf_pagador']).replace('.', '').replace('-', '')
        if not cpf.isdigit() or len(cpf) != 11:
            return False, "CPF inválido"
        
        return True, "Dados válidos"


class CalculadoraFreteBase(ABC):
    """
    Classe abstrata base para cálculo de frete.
    
    Demonstra Polimorfismo: permite diferentes estratégias de cálculo
    (frete fixo, Correios, transportadora) com a mesma interface.
    """
    
    @abstractmethod
    def calcular_frete(self, cep_destino: str, peso_kg: float, valor_produtos: float) -> tuple[float, int]:
        """
        Calcula o valor e prazo de entrega do frete.
        
        Args:
            cep_destino: CEP de destino (apenas números).
            peso_kg: Peso total dos produtos em kg.
            valor_produtos: Valor total dos produtos.
            
        Returns:
            Tupla (valor_frete: float, prazo_dias: int).
        """
        pass


class FreteFixo(CalculadoraFreteBase):
    """
    Implementação de frete com valor fixo.
    
    Demonstra Polimorfismo: implementação simples de cálculo de frete.
    """
    
    def __init__(self, valor_fixo: float = 15.00, prazo_fixo: int = 7):
        """
        Inicializa calculadora de frete fixo.
        
        Args:
            valor_fixo: Valor fixo do frete.
            prazo_fixo: Prazo fixo de entrega em dias.
        """
        self.valor_fixo = valor_fixo
        self.prazo_fixo = prazo_fixo
    
    def calcular_frete(self, cep_destino: str, peso_kg: float, valor_produtos: float) -> tuple[float, int]:
        """
        Retorna frete fixo independente do destino.
        
        Args:
            cep_destino: CEP de destino.
            peso_kg: Peso total.
            valor_produtos: Valor dos produtos.
            
        Returns:
            Tupla (valor_frete, prazo_dias).
        """
        # Frete grátis para compras acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, self.prazo_fixo
        
        return self.valor_fixo, self.prazo_fixo


class FreteCorreios(CalculadoraFreteBase):
    """
    Implementação de cálculo de frete via Correios (simulado).
    
    Demonstra Polimorfismo: implementação mais complexa que considera
    distância e peso.
    """
    
    def calcular_frete(self, cep_destino: str, peso_kg: float, valor_produtos: float) -> tuple[float, int]:
        """
        Calcula frete baseado em CEP e peso (simulação).
        
        Args:
            cep_destino: CEP de destino.
            peso_kg: Peso total.
            valor_produtos: Valor dos produtos.
            
        Returns:
            Tupla (valor_frete, prazo_dias).
        """
        # Simulação simples baseada no primeiro dígito do CEP
        # Em produção, chamaria API dos Correios
        cep_limpo = cep_destino.replace('-', '').replace('.', '')
        
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            # CEP inválido, retorna frete padrão
            return 20.0, 10
        
        primeiro_digito = int(cep_limpo[0])
        
        # Simular distância baseada no primeiro dígito do CEP
        # 0-3: Sudeste (mais próximo), 4-6: Sul/Centro-Oeste, 7-9: Norte/Nordeste
        if primeiro_digito <= 3:
            valor_base = 15.0
            prazo_base = 5
        elif primeiro_digito <= 6:
            valor_base = 25.0
            prazo_base = 8
        else:
            valor_base = 35.0
            prazo_base = 12
        
        # Adicionar custo por peso (R$ 2 por kg adicional após 1kg)
        if peso_kg > 1:
            valor_base += (peso_kg - 1) * 2.0
        
        # Frete grátis para compras acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, prazo_base
        
        return round(valor_base, 2), prazo_base


class IntegracaoController:
    """
    Controller para gerenciar integrações com serviços externos.
    
    Demonstra o uso de Polimorfismo: trabalha com interfaces abstratas
    (GatewayPagamentoBase, CalculadoraFreteBase) sem conhecer as implementações concretas.
    """
    
    def __init__(self, gateway_pagamento: GatewayPagamentoBase, calculadora_frete: CalculadoraFreteBase):
        """
        Inicializa o controller de integração.
        
        Args:
            gateway_pagamento: Instância de um gateway de pagamento.
            calculadora_frete: Instância de uma calculadora de frete.
        """
        self.gateway_pagamento = gateway_pagamento
        self.calculadora_frete = calculadora_frete
    
    def processar_checkout(
        self,
        valor_produtos: float,
        dados_pagamento: Dict[str, Any],
        cep_destino: str,
        peso_total_kg: float
    ) -> tuple[bool, str, float, int]:
        """
        Processa checkout completo: calcula frete e processa pagamento.
        
        Args:
            valor_produtos: Valor total dos produtos.
            dados_pagamento: Dados do pagamento.
            cep_destino: CEP de entrega.
            peso_total_kg: Peso total dos produtos.
            
        Returns:
            Tupla (sucesso, mensagem, valor_frete, prazo_entrega).
        """
        # Calcular frete
        valor_frete, prazo_entrega = self.calculadora_frete.calcular_frete(
            cep_destino, peso_total_kg, valor_produtos
        )
        
        # Calcular total com frete
        valor_total = valor_produtos + valor_frete
        
        # Processar pagamento
        sucesso, mensagem = self.gateway_pagamento.processar_pagamento(valor_total, dados_pagamento)
        
        return sucesso, mensagem, valor_frete, prazo_entrega
