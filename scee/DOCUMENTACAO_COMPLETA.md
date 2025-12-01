# 📚 DOCUMENTAÇÃO COMPLETA - SCEE

**Sistema de Comércio Eletrônico**  
**Versão:** 1.0  
**Data:** Novembro 2024

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Conceitos de POO Aplicados](#conceitos-de-poo-aplicados)
4. [Estrutura de Diretórios](#estrutura-de-diretórios)
5. [Modelos (Models)](#modelos-models)
6. [Repositórios (Repositories)](#repositórios-repositories)
7. [Controladores (Controllers)](#controladores-controllers)
8. [Funcionalidades Principais](#funcionalidades-principais)
9. [Fluxos de Uso](#fluxos-de-uso)
10. [Banco de Dados](#banco-de-dados)
11. [Segurança](#segurança)
12. [Como Executar](#como-executar)

---

## 🎯 VISÃO GERAL

### O que é o SCEE?

O **SCEE (Sistema de Comércio Eletrônico)** é uma aplicação web completa de e-commerce desenvolvida em Python com Flask, demonstrando a aplicação prática dos **4 pilares da Programação Orientada a Objetos**:

- ✅ **Herança**
- ✅ **Polimorfismo**
- ✅ **Encapsulamento**
- ✅ **Abstração**

### Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.13+ | Linguagem principal |
| Flask | 3.1.0 | Framework web |
| SQLAlchemy | 2.0.36 | ORM para banco de dados |
| SQLite | 3.x | Banco de dados |
| Argon2 | 23.1.0 | Hash de senhas |
| Jinja2 | 3.1.4 | Template engine |

### Características Principais

- 🛒 **E-commerce completo** com carrinho de compras
- 👤 **Autenticação** de clientes e administradores
- 📦 **Gestão de produtos** com imagens múltiplas
- 🚚 **3 opções de frete** (Fixo, Correios, Expresso)
- 💳 **3 métodos de pagamento** (Cartão, Pix, Boleto)
- 📊 **Controle de estoque** automático
- 🔒 **Segurança** com hash Argon2
- 📱 **Interface responsiva** e moderna

---

## 🏗️ ARQUITETURA DO SISTEMA

### Padrão MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────────┐
│                    CAMADA VIEW                      │
│  Templates HTML + Jinja2 + CSS                      │
│  - Apresentação dos dados                           │
│  - Interface do usuário                             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                 CAMADA CONTROLLER                   │
│  Lógica de Negócio                                  │
│  ┌─────────────────────────────────────────────┐   │
│  │ AuthController      - Autenticação          │   │
│  │ ProdutoController   - Gestão de produtos    │   │
│  │ PedidoController    - Gestão de pedidos     │   │
│  │ CarrinhoController  - Carrinho de compras   │   │
│  │ ClienteController   - Gestão de clientes    │   │
│  │ IntegracaoController- Pagamentos e fretes   │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│               CAMADA REPOSITORY                     │
│  Acesso a Dados (Padrão Repository)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │ BaseRepository      - CRUD genérico         │   │
│  │ ClienteRepository   - Operações de cliente  │   │
│  │ ProdutoRepository   - Operações de produto  │   │
│  │ PedidoRepository    - Operações de pedido   │   │
│  │ CategoriaRepository - Operações de categoria│   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                  CAMADA MODEL                       │
│  Entidades do Domínio (SQLAlchemy ORM)              │
│  ┌─────────────────────────────────────────────┐   │
│  │ Cliente, Admin, Produto, Pedido             │   │
│  │ Categoria, Endereco, ItemPedido             │   │
│  │ ImagemProduto                               │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                 BANCO DE DADOS                      │
│  SQLite - scee_loja.db                              │
└─────────────────────────────────────────────────────┘
```

### Benefícios da Arquitetura

1. **Separação de Responsabilidades** - Cada camada tem função específica
2. **Manutenibilidade** - Fácil localizar e corrigir problemas
3. **Testabilidade** - Camadas podem ser testadas independentemente
4. **Escalabilidade** - Fácil adicionar novas funcionalidades
5. **Reutilização** - Código pode ser reutilizado em diferentes contextos

---

## 🎓 CONCEITOS DE POO APLICADOS

### 1️⃣ HERANÇA (Inheritance)

#### 1.1 Herança em Repositórios

**Classe Base Genérica:**
```python
class BaseRepository(Generic[T]):
    """Repositório base com operações CRUD genéricas."""
    
    def __init__(self, model: type, session: Session):
        self.model = model
        self.session = session
    
    def create(self, entity: T) -> T:
        """Cria uma nova entidade."""
        self.session.add(entity)
        self.session.commit()
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Busca por ID."""
        return self.session.query(self.model).filter(
            self.model.id == entity_id
        ).first()
    
    def get_all(self) -> List[T]:
        """Retorna todas as entidades."""
        return self.session.query(self.model).all()
    
    def update(self, entity: T) -> T:
        """Atualiza entidade."""
        self.session.commit()
        return entity
    
    def delete(self, entity: T) -> None:
        """Remove entidade."""
        self.session.delete(entity)
        self.session.commit()
```

**Repositórios Específicos Herdam:**
```python
class ClienteRepository(BaseRepository):
    """Herda CRUD + métodos específicos de Cliente."""
    
    def __init__(self, session: Session):
        super().__init__(Cliente, session)
    
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Método específico de Cliente."""
        return self.session.query(Cliente).filter(
            Cliente.email == email
        ).first()

class ProdutoRepository(BaseRepository):
    """Herda CRUD + métodos específicos de Produto."""
    
    def __init__(self, session: Session):
        super().__init__(Produto, session)
    
    def get_by_categoria(self, categoria_id: int) -> List[Produto]:
        """Método específico de Produto."""
        return self.session.query(Produto).filter(
            Produto.categoria_id == categoria_id
        ).all()
```

**Benefícios:**
- ✅ Evita duplicação de código CRUD
- ✅ Manutenção centralizada
- ✅ Fácil adicionar novos repositórios

#### 1.2 Herança em Modelos

```python
# Todos os modelos herdam de Base (SQLAlchemy)
class Cliente(Base):
    __tablename__ = 'clientes'
    # ... campos

class Produto(Base):
    __tablename__ = 'produtos'
    # ... campos

class Pedido(Base):
    __tablename__ = 'pedidos'
    # ... campos
```

---

### 2️⃣ POLIMORFISMO (Polymorphism)

#### 2.1 Polimorfismo em Cálculo de Frete

**Interface Abstrata:**
```python
from abc import ABC, abstractmethod

class CalculadoraFreteBase(ABC):
    """
    Classe abstrata base para cálculo de frete.
    Define o CONTRATO que todas as calculadoras devem seguir.
    """
    
    @abstractmethod
    def calcular_frete(
        self, 
        cep_destino: str, 
        peso_kg: float, 
        valor_produtos: float
    ) -> tuple[float, int]:
        """
        Calcula valor e prazo do frete.
        
        Returns:
            (valor_frete, prazo_dias)
        """
        pass
```

**Implementação 1 - Frete Fixo:**
```python
class FreteFixo(CalculadoraFreteBase):
    """Frete com valor fixo independente do destino."""
    
    def __init__(self, valor_fixo: float = 15.00, prazo_fixo: int = 7):
        self.valor_fixo = valor_fixo
        self.prazo_fixo = prazo_fixo
    
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        # Frete grátis acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, self.prazo_fixo
        return self.valor_fixo, self.prazo_fixo
```

**Implementação 2 - Frete Correios:**
```python
class FreteCorreios(CalculadoraFreteBase):
    """Frete calculado por CEP e peso (simulação)."""
    
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        cep_limpo = cep_destino.replace('-', '').replace('.', '')
        primeiro_digito = int(cep_limpo[0])
        
        # Simula distância pelo CEP
        if primeiro_digito <= 3:  # Sudeste
            valor_base, prazo = 15.0, 5
        elif primeiro_digito <= 6:  # Sul/Centro-Oeste
            valor_base, prazo = 25.0, 8
        else:  # Norte/Nordeste
            valor_base, prazo = 35.0, 12
        
        # Adiciona custo por peso
        if peso_kg > 1:
            valor_base += (peso_kg - 1) * 2.0
        
        # Frete grátis acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, prazo
        
        return round(valor_base, 2), prazo
```

**Implementação 3 - Frete Expresso:**
```python
class FreteExpresso(CalculadoraFreteBase):
    """Frete premium - mais caro e mais rápido."""
    
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        cep_limpo = cep_destino.replace('-', '').replace('.', '')
        primeiro_digito = int(cep_limpo[0])
        
        # Valores mais altos, prazos menores
        if primeiro_digito <= 3:
            valor_base, prazo = 30.0, 2
        elif primeiro_digito <= 6:
            valor_base, prazo = 45.0, 3
        else:
            valor_base, prazo = 60.0, 5
        
        # Custo por peso
        if peso_kg > 1:
            valor_base += (peso_kg - 1) * 3.0
        
        # 50% de desconto acima de R$ 500 (não grátis)
        if valor_produtos >= 500:
            valor_base *= 0.5
        
        return round(valor_base, 2), prazo
```

**Uso Polimórfico:**
```python
# No PedidoController
if tipo_frete == 'Fixo':
    calculadora = FreteFixo()
elif tipo_frete == 'Correios':
    calculadora = FreteCorreios()
else:
    calculadora = FreteExpresso()

# POLIMORFISMO: Mesma chamada, comportamentos diferentes!
valor_frete, prazo = calculadora.calcular_frete(cep, peso, total)
```

**Benefícios:**
- ✅ Fácil adicionar novos tipos de frete
- ✅ Código desacoplado
- ✅ Mesma interface, comportamentos diferentes

#### 2.2 Polimorfismo em Gateways de Pagamento

**Interface Abstrata:**
```python
class GatewayPagamentoBase(ABC):
    """Classe abstrata para gateways de pagamento."""
    
    @abstractmethod
    def processar_pagamento(
        self, 
        valor: float, 
        dados_pagamento: Dict[str, Any]
    ) -> tuple[bool, str]:
        pass
    
    @abstractmethod
    def validar_dados_pagamento(
        self, 
        dados_pagamento: Dict[str, Any]
    ) -> tuple[bool, str]:
        pass
```

**Implementações:**
```python
class PagamentoCartao(GatewayPagamentoBase):
    """Pagamento via Cartão de Crédito."""
    
    def processar_pagamento(self, valor, dados_pagamento):
        # Valida dados do cartão
        valido, msg = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, msg
        
        # Simula processamento
        if valor > 10000:
            return False, "Valor acima do limite"
        
        return True, "Pagamento aprovado"
    
    def validar_dados_pagamento(self, dados):
        # Valida número, CVV, validade, titular
        # ...
        return True, "Dados válidos"

class PagamentoPix(GatewayPagamentoBase):
    """Pagamento via Pix."""
    
    def processar_pagamento(self, valor, dados_pagamento):
        # Valida CPF
        valido, msg = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, msg
        
        # Pix sempre aprovado (simulação)
        return True, "Pagamento via Pix aprovado"
    
    def validar_dados_pagamento(self, dados):
        # Valida CPF do pagador
        # ...
        return True, "Dados válidos"
```

---

### 3️⃣ ENCAPSULAMENTO (Encapsulation)

#### 3.1 Encapsulamento em Controllers

```python
class CarrinhoController:
    """Controlador do carrinho de compras."""
    
    def __init__(self):
        # Atributo PRIVADO (encapsulado)
        self.itens: Dict[int, ItemCarrinho] = {}
    
    # Acesso CONTROLADO via métodos públicos
    def adicionar_item(self, produto_id, nome, preco, quantidade):
        """Adiciona item com VALIDAÇÃO."""
        if quantidade <= 0:
            return False, "Quantidade inválida"
        
        if produto_id in self.itens:
            # Atualiza quantidade existente
            self.itens[produto_id].atualizar_quantidade(
                self.itens[produto_id].quantidade + quantidade
            )
        else:
            # Cria novo item
            self.itens[produto_id] = ItemCarrinho(
                produto_id, nome, preco, quantidade
            )
        
        return True, "Item adicionado"
    
    def calcular_total(self) -> float:
        """Calcula total SEM expor estrutura interna."""
        return sum(item.subtotal for item in self.itens.values())
```

**Benefícios:**
- ✅ Dados protegidos de acesso direto
- ✅ Validações garantidas
- ✅ Consistência de dados

#### 3.2 Encapsulamento em Modelos

```python
class ItemCarrinho:
    """Item do carrinho com subtotal automático."""
    
    def __init__(self, produto_id, nome, preco, quantidade):
        self.produto_id = produto_id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        # Subtotal CALCULADO automaticamente
        self.subtotal = preco * quantidade
    
    def atualizar_quantidade(self, quantidade):
        """Atualiza quantidade e RECALCULA subtotal."""
        self.quantidade = quantidade
        self.subtotal = self.preco * quantidade  # Sempre consistente
```

---

### 4️⃣ ABSTRAÇÃO (Abstraction)

#### 4.1 Classes Abstratas

```python
from abc import ABC, abstractmethod

# Classe ABSTRATA - não pode ser instanciada
class CalculadoraFreteBase(ABC):
    
    @abstractmethod
    def calcular_frete(self, cep, peso, valor):
        """Método ABSTRATO - deve ser implementado."""
        pass

# Tentativa de instanciar classe abstrata gera ERRO
# calculadora = CalculadoraFreteBase()  # ❌ TypeError!

# Deve usar implementação concreta
calculadora = FreteFixo()  # ✅ OK
```

#### 4.2 Abstração em Camadas

**Controller abstrai complexidade:**
```python
class PedidoController:
    """Abstrai toda lógica de criação de pedido."""
    
    def criar_pedido(self, cliente_id, itens, endereco_id, 
                     pagamento, frete):
        """
        Método público SIMPLES.
        Abstrai complexidade interna:
        - Validações
        - Cálculo de frete
        - Atualização de estoque
        - Criação de pedido
        - Transações atômicas
        """
        # Usuário não precisa saber dos detalhes
        # ...
        return True, "Pedido criado", pedido
```

**Benefícios:**
- ✅ Esconde complexidade
- ✅ Interface simples
- ✅ Fácil de usar

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
scee/
│
├── app.py                          # Aplicação Flask principal
├── init_db.py                      # Script de inicialização do BD
├── database.py                     # Configuração do banco
├── scee_loja.db                    # Banco de dados SQLite
│
├── models/                         # 📦 MODELOS (Entidades)
│   ├── __init__.py
│   ├── base.py                     # Classe base SQLAlchemy
│   ├── cliente.py                  # Modelo Cliente
│   ├── admin.py                    # Modelo Admin
│   ├── produto.py                  # Modelo Produto
│   ├── pedido.py                   # Modelo Pedido
│   ├── item_pedido.py              # Modelo ItemPedido
│   ├── categoria.py                # Modelo Categoria
│   ├── endereco.py                 # Modelo Endereco
│   └── imagem_produto.py           # Modelo ImagemProduto
│
├── repositories/                   # 🗄️ REPOSITÓRIOS (Acesso a Dados)
│   ├── __init__.py
│   ├── base_repository.py          # Repositório base genérico
│   ├── cliente_repository.py       # Repositório de Cliente
│   ├── admin_repository.py         # Repositório de Admin
│   ├── produto_repository.py       # Repositório de Produto
│   ├── pedido_repository.py        # Repositório de Pedido
│   ├── categoria_repository.py     # Repositório de Categoria
│   └── endereco_repository.py      # Repositório de Endereco
│
├── controllers/                    # 🎮 CONTROLADORES (Lógica de Negócio)
│   ├── __init__.py
│   ├── auth_controller.py          # Autenticação
│   ├── produto_controller.py       # Gestão de produtos
│   ├── pedido_controller.py        # Gestão de pedidos
│   ├── carrinho_controller.py      # Carrinho de compras
│   ├── cliente_controller.py       # Gestão de clientes
│   └── integracao_controller.py    # Pagamentos e fretes
│
├── templates/                      # 🎨 VIEWS (Interface)
│   ├── base.html                   # Template base
│   ├── index.html                  # Página inicial
│   ├── login.html                  # Login
│   ├── registro.html               # Registro
│   ├── produtos.html               # Listagem de produtos
│   ├── produto_detalhe.html        # Detalhes do produto
│   ├── carrinho.html               # Carrinho
│   ├── checkout.html               # Finalização
│   ├── minha_conta.html            # Conta do cliente
│   └── admin/                      # Templates admin
│       ├── dashboard.html
│       ├── produtos.html
│       ├── categorias.html
│       └── ...
│
├── static/                         # 📂 ARQUIVOS ESTÁTICOS
│   ├── css/
│   │   └── style.css               # Estilos
│   └── uploads/                    # Imagens de produtos
│
└── docs/                           # 📚 DOCUMENTAÇÃO
    ├── DOCUMENTACAO_COMPLETA.md
    ├── SCRIPT_APRESENTACAO.md
    ├── RELATORIO_REVISAO_POO.md
    └── ...
```

---

## 📦 MODELOS (Models)

### Cliente
```python
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    
    # Relacionamentos
    enderecos = relationship('Endereco', back_populates='cliente')
    pedidos = relationship('Pedido', back_populates='cliente')
```

### Produto
```python
class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    
    # Relacionamentos
    categoria = relationship('Categoria', back_populates='produtos')
    imagens = relationship('ImagemProduto', back_populates='produto')
```

### Pedido
```python
class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    data_pedido = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='Pendente')
    total = Column(Float, nullable=False)
    endereco_entrega = Column(String(500), nullable=False)
    metodo_pagamento = Column(String(50), nullable=False)
    
    # Campos de frete
    tipo_frete = Column(String(50), default='Fixo')
    valor_frete = Column(Float, default=0.0)
    prazo_entrega = Column(Integer, default=7)
    
    # Relacionamentos
    cliente = relationship('Cliente', back_populates='pedidos')
    itens = relationship('ItemPedido', back_populates='pedido')
```

---

## 🗄️ REPOSITÓRIOS (Repositories)

### Padrão Repository

O padrão Repository abstrai o acesso a dados, fornecendo uma interface de coleção para acessar objetos de domínio.

**Benefícios:**
- ✅ Separa lógica de negócio da lógica de acesso a dados
- ✅ Facilita testes (pode usar mock)
- ✅ Centraliza queries
- ✅ Reutilização de código

### BaseRepository (Genérico)

```python
class BaseRepository(Generic[T]):
    """Repositório base com CRUD genérico."""
    
    def create(self, entity: T) -> T:
        """Cria entidade."""
        
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Busca por ID."""
        
    def get_all(self) -> List[T]:
        """Lista todas."""
        
    def update(self, entity: T) -> T:
        """Atualiza entidade."""
        
    def delete(self, entity: T) -> None:
        """Remove entidade."""
```

---

## 🎮 CONTROLADORES (Controllers)

### AuthController
**Responsabilidade:** Autenticação e registro

**Métodos principais:**
- `registrar_cliente()` - Registra novo cliente
- `login_cliente()` - Autentica cliente
- `login_admin()` - Autentica admin
- `validar_email()` - Valida formato de email
- `validar_cpf()` - Valida CPF com dígitos verificadores
- `validar_senha_forte()` - Valida força da senha

### ProdutoController
**Responsabilidade:** Gestão de produtos

**Métodos principais:**
- `criar_produto()` - Cria produto com imagens
- `atualizar_produto()` - Atualiza produto
- `remover_produto()` - Remove produto
- `listar_produtos()` - Lista produtos
- `buscar_por_categoria()` - Filtra por categoria

### PedidoController
**Responsabilidade:** Gestão de pedidos

**Métodos principais:**
- `criar_pedido()` - Cria pedido com frete
- `cancelar_pedido()` - Cancela pedido (Pendente/Processando)
- `atualizar_status()` - Atualiza status do pedido
- `listar_pedidos_cliente()` - Lista pedidos do cliente

### CarrinhoController
**Responsabilidade:** Carrinho de compras

**Métodos principais:**
- `adicionar_item()` - Adiciona produto
- `remover_item()` - Remove produto
- `atualizar_quantidade()` - Atualiza quantidade
- `calcular_total()` - Calcula total
- `limpar()` - Limpa carrinho

### IntegracaoController
**Responsabilidade:** Integrações externas

**Classes:**
- `GatewayPagamentoBase` (Abstrata)
  - `PagamentoCartao`
  - `PagamentoPix`
- `CalculadoraFreteBase` (Abstrata)
  - `FreteFixo`
  - `FreteCorreios`
  - `FreteExpresso`

---

## ⚙️ FUNCIONALIDADES PRINCIPAIS

### 1. Autenticação e Registro

**Cliente:**
- Registro com validação de CPF e email
- Senha forte (mínimo 8 caracteres, maiúscula, minúscula, número)
- Hash com Argon2 (segurança máxima)
- Login com sessão

**Admin:**
- Login separado
- Acesso à área administrativa
- Credenciais padrão: `admin@scee.com` / `Admin@123`

### 2. Catálogo de Produtos

**Funcionalidades:**
- Listagem com paginação
- Filtro por categoria
- Busca por nome
- Detalhes do produto
- Múltiplas imagens
- Indicador de estoque

**Controle de Estoque:**
- ✅ Produtos sem estoque não podem ser comprados
- ✅ Validação ao adicionar ao carrinho
- ✅ Atualização automática ao criar pedido
- ✅ Indicadores visuais (✓ Em estoque / ✗ SEM ESTOQUE)

### 3. Carrinho de Compras

**Funcionalidades:**
- Adicionar produtos
- Remover produtos
- Atualizar quantidades
- Cálculo automático de total
- Persistência em sessão
- Validação de estoque

### 4. Sistema de Frete (POLIMORFISMO)

**3 Opções:**

| Tipo | Valor | Prazo | Grátis R$500+ |
|------|-------|-------|---------------|
| **Fixo** | R$ 15 | 7 dias | ✅ 100% |
| **Correios** | R$ 15-35 | 5-12 dias | ✅ 100% |
| **Expresso** | R$ 30-60 | 2-5 dias | ⚠️ 50% |

**Cálculo:**
- Baseado em CEP (distância simulada)
- Considera peso dos produtos
- Frete grátis para compras acima de R$ 500

### 5. Métodos de Pagamento

**3 Opções:**
- 💳 **Cartão de Crédito** - Validação de número, CVV, validade
- 📱 **Pix** - Validação de CPF
- 🧾 **Boleto Bancário** - Geração simulada

### 6. Gestão de Pedidos

**Status:**
- **Pendente** - Aguardando processamento
- **Processando** - Em preparação
- **Enviado** - A caminho
- **Entregue** - Finalizado
- **Cancelado** - Cancelado pelo cliente/admin

**Cancelamento:**
- Cliente pode cancelar pedidos "Pendente" ou "Processando"
- Estoque é devolvido automaticamente

### 7. Área Administrativa

**Funcionalidades:**
- Dashboard com estatísticas
- Gestão de produtos (CRUD)
- Gestão de categorias (CRUD)
- Visualização de clientes
- Gestão de pedidos
- Atualização de status

---

## 🔄 FLUXOS DE USO

### Fluxo 1: Compra Completa

```
1. Cliente acessa site
   ↓
2. Navega pelo catálogo
   ↓
3. Adiciona produtos ao carrinho
   ↓
4. Vai para checkout
   ↓
5. Seleciona endereço de entrega
   ↓
6. Escolhe tipo de frete (Fixo/Correios/Expresso)
   ↓
7. Sistema calcula frete automaticamente
   ↓
8. Escolhe método de pagamento
   ↓
9. Confirma pedido
   ↓
10. Sistema:
    - Valida estoque
    - Calcula frete
    - Atualiza estoque
    - Cria pedido
    - Limpa carrinho
   ↓
11. Cliente visualiza pedido em "Minha Conta"
```

### Fluxo 2: Cancelamento de Pedido

```
1. Cliente acessa "Minha Conta"
   ↓
2. Visualiza pedidos
   ↓
3. Clica em "Cancelar" (se Pendente/Processando)
   ↓
4. Sistema:
    - Valida status
    - Devolve estoque
    - Atualiza status para "Cancelado"
   ↓
5. Cliente recebe confirmação
```

### Fluxo 3: Admin Gerencia Produto

```
1. Admin faz login
   ↓
2. Acessa "Produtos"
   ↓
3. Clica em "Novo Produto"
   ↓
4. Preenche formulário:
    - Nome, SKU, Descrição
    - Preço, Estoque
    - Categoria
    - Imagens (até 5)
   ↓
5. Sistema valida e salva
   ↓
6. Produto aparece no catálogo
```

---

## 💾 BANCO DE DADOS

### Diagrama ER (Entidade-Relacionamento)

```
┌─────────────┐         ┌──────────────┐
│   CLIENTE   │1      N │   ENDERECO   │
│─────────────│◄────────│──────────────│
│ id (PK)     │         │ id (PK)      │
│ nome        │         │ cliente_id(FK│
│ email       │         │ rua          │
│ cpf         │         │ numero       │
│ senha_hash  │         │ cep          │
└──────┬──────┘         └──────────────┘
       │1
       │
       │N
┌──────▼──────┐
│   PEDIDO    │
│─────────────│
│ id (PK)     │
│ cliente_id(FK)
│ total       │
│ status      │
│ tipo_frete  │
│ valor_frete │
└──────┬──────┘
       │1
       │
       │N
┌──────▼──────┐         ┌──────────────┐
│ ITEM_PEDIDO │N      1 │   PRODUTO    │
│─────────────│────────►│──────────────│
│ id (PK)     │         │ id (PK)      │
│ pedido_id(FK)         │ nome         │
│ produto_id(FK)        │ sku          │
│ quantidade  │         │ preco        │
│ preco_unit  │         │ estoque      │
└─────────────┘         │ categoria_id │
                        └──────┬───────┘
                               │N
                               │
                               │1
                        ┌──────▼───────┐
                        │  CATEGORIA   │
                        │──────────────│
                        │ id (PK)      │
                        │ nome         │
                        └──────────────┘
```

### Tabelas Principais

1. **clientes** - Dados dos clientes
2. **admins** - Administradores
3. **produtos** - Catálogo de produtos
4. **categorias** - Categorias de produtos
5. **pedidos** - Pedidos realizados
6. **itens_pedido** - Itens de cada pedido
7. **enderecos** - Endereços de entrega
8. **imagens_produto** - Imagens dos produtos

---

## 🔒 SEGURANÇA

### 1. Hash de Senhas
- **Algoritmo:** Argon2 (vencedor do Password Hashing Competition)
- **Benefícios:** Resistente a ataques de força bruta e GPU

### 2. Validações
- CPF com dígitos verificadores
- Email com regex
- Senha forte (8+ caracteres, maiúscula, minúscula, número)
- CEP (8 dígitos)
- Estoque antes de adicionar ao carrinho

### 3. Sessões
- Sessões Flask seguras
- Separação cliente/admin
- Logout limpa sessão

### 4. SQL Injection
- SQLAlchemy ORM previne SQL injection
- Queries parametrizadas

---

## 🚀 COMO EXECUTAR

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Inicializar Banco de Dados

```bash
python init_db.py
```

**Isso cria:**
- Banco de dados `scee_loja.db`
- Tabelas
- Categorias padrão
- Admin padrão (`admin@scee.com` / `Admin@123`)

### 3. Executar Aplicação

```bash
python app.py
```

### 4. Acessar

```
http://localhost:5000
```

**Área Admin:**
```
http://localhost:5000/admin
```

---

## 📊 ESTATÍSTICAS DO CÓDIGO

- **Linhas de código:** ~3.500
- **Arquivos Python:** 28
- **Templates HTML:** 15
- **Modelos:** 8
- **Repositórios:** 7
- **Controllers:** 6
- **Classes abstratas:** 2
- **Implementações polimórficas:** 5

---

## 🎯 CONCLUSÃO

O SCEE é um sistema completo de e-commerce que demonstra de forma prática e eficiente os **4 pilares da POO**:

1. ✅ **Herança** - BaseRepository, modelos SQLAlchemy
2. ✅ **Polimorfismo** - Fretes e pagamentos
3. ✅ **Encapsulamento** - Controllers e modelos
4. ✅ **Abstração** - Classes abstratas e interfaces

**Arquitetura sólida (MVC)**, **código limpo**, **bem documentado** e **totalmente funcional**.

---

**Desenvolvido com 💙 usando Python e Flask**
