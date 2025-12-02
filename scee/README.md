# 🛒 SCEE - Sistema de Comércio Eletrônico

Sistema completo de e-commerce desenvolvido em Python com Flask, demonstrando na prática os **4 pilares da Programação Orientada a Objetos** e seguindo o padrão arquitetural **MVC** (Model-View-Controller).

## ⭐ Características Principais

- **Arquitetura MVC**: Separação clara entre Model, View e Controller
- **4 Pilares da POO**: Herança, Polimorfismo, Encapsulamento e Abstração
- **ORM SQLAlchemy**: Abstração completa do banco de dados
- **Padrão Repository**: Isolamento da lógica de persistência
- **Segurança**: Senhas com Argon2 (vencedor do Password Hashing Competition)
- **3 Opções de Frete**: Fixo, Correios e Expresso (Polimorfismo)
- **3 Métodos de Pagamento**: Cartão, Pix e Boleto
- **Controle de Estoque**: Automático com validações
- **Interface Responsiva**: Design moderno e adaptável

## Estrutura do Projeto

```
scee/
├── models/                 # Camada Model (Entidades ORM)
│   ├── base.py
│   ├── cliente.py
│   ├── admin.py
│   ├── endereco.py
│   ├── categoria.py
│   ├── produto.py
│   ├── imagem_produto.py
│   ├── pedido.py
│   └── item_pedido.py
├── repositories/           # Camada de Repositório
│   ├── base_repository.py
│   ├── cliente_repository.py
│   ├── admin_repository.py
│   ├── produto_repository.py
│   ├── categoria_repository.py
│   ├── endereco_repository.py
│   └── pedido_repository.py
├── controllers/            # Camada Controller (Lógica de Negócios)
│   ├── auth_controller.py
│   ├── cliente_controller.py
│   ├── produto_controller.py
│   ├── carrinho_controller.py
│   ├── pedido_controller.py
│   └── integracao_controller.py  # Fretes e Pagamentos (Polimorfismo)
├── templates/              # Camada View (Templates HTML)
│   ├── base.html
│   ├── index.html
│   ├── registro.html
│   ├── login.html
│   ├── produtos.html
│   ├── produto_detalhe.html
│   ├── carrinho.html
│   ├── checkout.html
│   ├── minha_conta.html
│   └── admin/
│       ├── dashboard.html
│       ├── produtos.html
│       ├── produto_form.html
│       └── pedidos.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── uploads/            # Imagens de produtos
├── database.py             # Configuração do banco de dados
├── app.py                  # Aplicação Flask principal
├── init_db.py              # Script de inicialização do BD
├── requirements.txt        # Dependências Python
├── README.md
└── docs/                   # Documentação completa
    ├── DOCUMENTACAO_COMPLETA.md
    ├── FUNCIONALIDADES_DETALHADAS.md
    ├── SCRIPT_APRESENTACAO_10MIN.md
    └── RELATORIO_REVISAO_POO.md
```

## Requisitos

- Python 3.10 ou superior
- SQLite 3 ou superior

## Instalação

1. Clone ou extraia o projeto:

```bash
cd scee
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/Mac:

```bash
source venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Inicialização

1. Inicialize o banco de dados:

```bash
python init_db.py
```

Isso irá:
- Criar o banco de dados `scee_loja.db`
- Criar todas as tabelas
- Criar categorias padrão
- Criar admin padrão (`admin@scee.com` / `Admin@123`)

2. Execute a aplicação:

```bash
python app.py
```

3. Acesse no navegador:

```
http://localhost:5000
```

4. Área administrativa:

```
http://localhost:5000/admin
Login: admin@scee.com
Senha: Admin@123
```

## Funcionalidades

### Para Clientes

- ✅ **Registro e Login**: Cadastro com validação de CPF, e-mail único e senha forte
- ✅ **Catálogo de Produtos**: Listagem com filtros por categoria e indicadores de estoque
- ✅ **Carrinho de Compras**: Adicionar, remover e atualizar quantidades
- ✅ **Checkout Completo**: 
  - Seleção de endereço de entrega
  - **3 opções de frete** (Fixo, Correios, Expresso)
  - **3 métodos de pagamento** (Cartão, Pix, Boleto)
  - Cálculo automático de frete
- ✅ **Minha Conta**: Gerenciar perfil, endereços e visualizar pedidos
- ✅ **Cancelamento de Pedidos**: Pedidos "Pendente" ou "Processando"
- ✅ **Controle de Estoque**: Produtos sem estoque não podem ser comprados

### Para Administradores

- ✅ **Dashboard**: Estatísticas do sistema
- ✅ **Gerenciamento de Produtos**: CRUD completo com upload de até 5 imagens
- ✅ **Gerenciamento de Categorias**: CRUD completo
- ✅ **Gerenciamento de Pedidos**: Visualizar e alterar status
- ✅ **Visualização de Clientes**: Lista completa de clientes cadastrados

## Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- `clientes`: Dados dos clientes
- `admins`: Dados dos administradores
- `enderecos`: Endereços de entrega
- `categorias`: Categorias de produtos
- `produtos`: Catálogo de produtos
- `imagens_produto`: Imagens dos produtos
- `pedidos`: Pedidos realizados
- `itens_pedido`: Itens de cada pedido

## Segurança

- Senhas criptografadas com Argon2 (hash + salt)
- Validação de CPF com dígitos verificadores
- Validação de e-mail único
- Proteção contra race conditions no estoque
- Transações atômicas para criação de pedidos

## 🎓 Princípios de POO Aplicados

### 1️⃣ Herança

- **BaseRepository**: Classe base genérica com CRUD
- Todos os repositórios herdam de `BaseRepository`
- Reutilização de código e manutenção centralizada

```python
class BaseRepository(Generic[T]):
    def create(self, entity: T) -> T
    def get_by_id(self, entity_id: int)
    def get_all(self) -> List[T]
    def update(self, entity: T) -> T
    def delete(self, entity: T) -> None
```

### 2️⃣ Polimorfismo ⭐

**Sistema de Frete** (3 implementações):

```python
class CalculadoraFreteBase(ABC):
    @abstractmethod
    def calcular_frete(self, cep, peso, valor) -> tuple[float, int]

class FreteFixo(CalculadoraFreteBase):
    # R$ 15,00 - 7 dias
    
class FreteCorreios(CalculadoraFreteBase):
    # R$ 15-35 - 5-12 dias (varia por CEP)
    
class FreteExpresso(CalculadoraFreteBase):
    # R$ 30-60 - 2-5 dias (mais rápido)
```

**Sistema de Pagamento** (2 implementações):

```python
class GatewayPagamentoBase(ABC):
    @abstractmethod
    def processar_pagamento(self, valor, dados) -> tuple[bool, str]

class PagamentoCartao(GatewayPagamentoBase)
class PagamentoPix(GatewayPagamentoBase)
```

### 3️⃣ Encapsulamento

- Atributos privados/protegidos nas classes
- Acesso controlado via métodos públicos
- Validações internas garantidas
- Exemplo: `CarrinhoController` com `self.itens` encapsulado

### 4️⃣ Abstração

- Classes abstratas (ABC) definem contratos
- `CalculadoraFreteBase` e `GatewayPagamentoBase`
- Subclasses implementam detalhes
- Interface simples, complexidade escondida

## Padrão MVC

### Model

- Entidades ORM (SQLAlchemy)
- Mapeamento objeto-relacional
- Definição de relacionamentos

### View

- Templates HTML (Jinja2)
- CSS responsivo
- Interface do usuário

### Controller

- Lógica de negócios
- Validações
- Orquestração entre Model e View

## 📚 Documentação

O projeto possui documentação completa:

- **DOCUMENTACAO_COMPLETA.md**: Documentação técnica detalhada
- **FUNCIONALIDADES_DETALHADAS.md**: Análise de cada funcionalidade
- **SCRIPT_APRESENTACAO_10MIN.md**: Script para apresentação de 10 minutos
- **RELATORIO_REVISAO_POO.md**: Análise dos conceitos de POO aplicados

## 📊 Estatísticas do Projeto

- **Linhas de código**: 3.500+
- **Arquivos Python**: 28
- **Templates HTML**: 15
- **Modelos**: 8
- **Repositórios**: 7
- **Controllers**: 6
- **Classes abstratas**: 2
- **Implementações polimórficas**: 5

## 🎯 Conceitos Demonstrados

- ✅ **Herança** - BaseRepository genérico
- ✅ **Polimorfismo** - Fretes e Pagamentos
- ✅ **Encapsulamento** - Controllers e modelos
- ✅ **Abstração** - Classes ABC
- ✅ **Padrão MVC** - Arquitetura em camadas
- ✅ **Padrão Repository** - Acesso a dados
- ✅ **Dependency Injection** - Session nos controllers
- ✅ **Transações Atômicas** - Consistência de dados

---

## 🔧 Resolução de Problemas

### Erro: SQLAlchemy com Python 3.13

**Problema:**
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

**Causa:** Incompatibilidade entre Python 3.13 (muito recente) e SQLAlchemy 2.0.36.

**Solução 1: Downgrade do SQLAlchemy (RECOMENDADO)**

```powershell
# Ativar ambiente virtual
venv\Scripts\activate

# Desinstalar SQLAlchemy atual
pip uninstall sqlalchemy -y

# Instalar versão compatível
pip install SQLAlchemy==2.0.35

# Executar aplicação
python app.py
```

**Solução 2: Usar Python 3.11 ou 3.12**

```powershell
# Remover ambiente virtual antigo
Remove-Item -Recurse -Force venv

# Criar novo com Python 3.12
py -3.12 -m venv venv

# Ativar
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python app.py
```

### Erro: ModuleNotFoundError: No module named 'database'

**Problema:** Arquivo `database.py` não encontrado.

**Solução:** O arquivo já está criado. Tente:

```powershell
# Limpar cache do Python
Remove-Item -Recurse -Force __pycache__

# Fechar e reabrir terminal
# Executar novamente
python app.py
```

### Erro: Filtros não funcionam corretamente

**Problema:** Ao selecionar categoria + preço, mostra produtos de todas as categorias.

**Solução:** Já corrigido na versão atual. Se persistir:

1. Verifique se está usando a versão mais recente do código
2. Reinicie o servidor Flask (`CTRL+C` e `python app.py`)
3. Limpe o cache do navegador (`CTRL+SHIFT+DEL`)

### Erro: Banco de dados não inicializado

**Problema:** Tabelas não existem ou admin não foi criado.

**Solução:**

```powershell
# Executar script de inicialização
python init_db.py
```

Isso irá:
- Criar banco `scee_loja.db`
- Criar todas as tabelas
- Criar categorias padrão
- Criar admin: `admin@scee.com` / `Admin@123`

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais, demonstrando conceitos de Programação Orientada a Objetos.
