# 🛒 SCEE - Sistema de Comércio Eletrônico

Sistema completo de e-commerce desenvolvido em Python com Flask, demonstrando os **4 pilares da Programação Orientada a Objetos**.

---

## 📋 Informações do Projeto

**Linguagem:** Python 3.11+  
**Framework:** Flask 3.1.0  
**Banco de Dados:** SQLite  
**Padrão Arquitetural:** MVC (Model-View-Controller)

---

## ⭐ Funcionalidades

### Para Clientes:
- ✅ Registro e login com validação
- ✅ Catálogo de produtos com filtros
- ✅ Carrinho de compras
- ✅ Checkout com 3 opções de frete
- ✅ Gerenciamento de perfil e endereços
- ✅ Histórico de pedidos

### Para Administradores:
- ✅ Dashboard administrativo
- ✅ CRUD de produtos (com até 5 imagens)
- ✅ CRUD de categorias
- ✅ Gerenciamento de pedidos
- ✅ Visualização de clientes

---

## 🎓 Conceitos de POO Aplicados

### 1. **Herança**
```python
# BaseRepository (classe pai)
class BaseRepository(Generic[T]):
    def create(self, entity: T)
    def get_by_id(self, entity_id: int)
    def get_all(self) -> List[T]

# Repositórios específicos herdam
class ProdutoRepository(BaseRepository[Produto])
class ClienteRepository(BaseRepository[Cliente])
```

### 2. **Polimorfismo**
```python
# Classes abstratas para fretes
class CalculadoraFreteBase(ABC):
    @abstractmethod
    def calcular_frete(self, cep, peso, valor)

# Implementações diferentes
class FreteFixo(CalculadoraFreteBase)      # R$ 15,00 - 7 dias
class FreteCorreios(CalculadoraFreteBase)  # R$ 15-35 - 5-12 dias
class FreteExpresso(CalculadoraFreteBase)  # R$ 30-60 - 2-5 dias
```

### 3. **Encapsulamento**
```python
# Lógica encapsulada nos controllers
class CarrinhoController:
    def __init__(self):
        self.itens = {}  # Atributo privado
    
    def adicionar_item(self, produto_id, nome, preco, quantidade):
        # Lógica interna protegida
```

### 4. **Abstração**
```python
# Interface abstrata para pagamentos
class GatewayPagamentoBase(ABC):
    @abstractmethod
    def processar_pagamento(self, valor, dados)

# Implementações concretas
class PagamentoCartao(GatewayPagamentoBase)
class PagamentoPix(GatewayPagamentoBase)
```

---

## 📁 Estrutura do Projeto

```
scee/
├── models/                 # Modelos (Entidades do banco)
│   ├── base.py
│   ├── cliente.py
│   ├── produto.py
│   ├── pedido.py
│   └── ...
├── repositories/           # Acesso a dados (Padrão Repository)
│   ├── base_repository.py
│   ├── produto_repository.py
│   └── ...
├── controllers/            # Lógica de negócios
│   ├── auth_controller.py
│   ├── produto_controller.py
│   ├── pedido_controller.py
│   └── integracao_controller.py
├── templates/              # Views (HTML)
├── static/                 # CSS, JS, Imagens
├── app.py                  # Aplicação Flask (Rotas)
├── database.py             # Configuração do banco
├── init_db.py              # Script de inicialização
└── requirements.txt        # Dependências
```

---

## 🚀 Instalação e Execução

### 1. **Pré-requisitos**
- Python 3.11 ou 3.12 (recomendado)
- pip (gerenciador de pacotes)

### 2. **Clonar/Baixar o Projeto**
```bash
cd scee
```

### 3. **Criar Ambiente Virtual**
```bash
python -m venv venv
```

### 4. **Ativar Ambiente Virtual**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 5. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 6. **Inicializar Banco de Dados**
```bash
python init_db.py
```

**Isso irá:**
- Criar o banco `scee_loja.db`
- Criar todas as tabelas
- Criar 10 categorias padrão
- Criar usuário admin: `admin@scee.com` / `Admin@123`

### 7. **Executar Aplicação**
```bash
python app.py
```

### 8. **Acessar no Navegador**
```
http://localhost:5000
```

**Área Admin:**
```
http://localhost:5000/admin
Login: admin@scee.com
Senha: Admin@123
```

---

## 🔧 Resolução de Problemas

### ❌ Erro: SQLAlchemy com Python 3.13

**Sintoma:**
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

**Causa:** Python 3.13 é muito recente e incompatível com SQLAlchemy 2.0.36

**Solução 1 (Rápida):**
```bash
pip uninstall sqlalchemy -y
pip install SQLAlchemy==2.0.35
```

**Solução 2 (Recomendada):**
Usar Python 3.11 ou 3.12

---

### ❌ Erro: ModuleNotFoundError

**Sintoma:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solução:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

### ❌ Erro: Banco não inicializado

**Sintoma:**
```
sqlalchemy.exc.OperationalError: no such table: clientes
```

**Solução:**
```bash
python init_db.py
```

---

### ❌ Erro: Porta 5000 em uso

**Sintoma:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solução:**
```bash
# Encontrar processo
netstat -ano | findstr :5000

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

---

## 📊 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| Flask | 3.1.0 | Framework web |
| SQLAlchemy | 2.0.35 | ORM |
| SQLite | 3.x | Banco de dados |
| Argon2 | 23.1.0 | Hash de senhas |
| Jinja2 | 3.1.4 | Templates |

---

## 📈 Estatísticas

- **Linhas de código:** ~3.500
- **Arquivos Python:** 28
- **Templates HTML:** 20
- **Rotas:** 33
- **Modelos:** 8
- **Repositórios:** 7
- **Controllers:** 6

---

## 🎯 Padrões de Projeto

- ✅ **MVC** - Separação de responsabilidades
- ✅ **Repository Pattern** - Acesso a dados
- ✅ **Dependency Injection** - Injeção de dependências
- ✅ **Strategy Pattern** - Polimorfismo (fretes/pagamentos)
- ✅ **Factory Pattern** - Criação de objetos

---

## 📝 Credenciais Padrão

### Admin:
- **Email:** admin@scee.com
- **Senha:** Admin@123

### Cliente (criar novo):
- Registrar em: http://localhost:5000/registro

---

## 🔒 Segurança

- ✅ Senhas com Argon2 (vencedor do Password Hashing Competition)
- ✅ Validação de CPF
- ✅ Validação de email único
- ✅ Senha forte obrigatória
- ✅ Controle de sessões
- ✅ Proteção de rotas admin

---

## 📚 Documentação Adicional

Para mais detalhes, consulte:
- `RELATORIO_POO.md` - Análise dos conceitos de POO aplicados

---

## 💡 Dicas de Uso

### Para Testar o Sistema:

1. **Como Cliente:**
   - Registrar nova conta
   - Navegar pelos produtos
   - Adicionar ao carrinho
   - Finalizar compra (escolher frete)
   - Ver pedidos em "Minha Conta"

2. **Como Admin:**
   - Login: admin@scee.com / Admin@123
   - Criar categorias
   - Criar produtos (com imagens)
   - Gerenciar pedidos
   - Ver clientes

---

## 🎓 Desenvolvido para fins educacionais

Este projeto demonstra a aplicação prática dos conceitos de Programação Orientada a Objetos em um sistema real e funcional.

---

**© 2025 SCEE - Sistema de Comércio Eletrônico**
