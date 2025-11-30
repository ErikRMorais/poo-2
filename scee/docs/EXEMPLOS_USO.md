# Exemplos de Uso - SCEE

## Guia para Desenvolvedores

Este documento contém exemplos práticos de como usar as classes e métodos do sistema SCEE.

---

## 1. Configuração Inicial

### Importar Módulos

```python
from database import Database
from models import Cliente, Produto, Pedido, Categoria
from repositories import ClienteRepository, ProdutoRepository, PedidoRepository
from controllers import AuthController, ProdutoController, PedidoController
```

### Inicializar Banco de Dados

```python
# Criar instância do banco
db = Database()

# Criar todas as tabelas
db.create_tables()

# Obter sessão
session = db.get_session()
```

---

## 2. Autenticação

### Registrar Novo Cliente

```python
from controllers.auth_controller import AuthController

# Criar controller
auth_controller = AuthController(session)

# Registrar cliente
sucesso, mensagem, cliente = auth_controller.registrar_cliente(
    nome="João Silva",
    email="joao@exemplo.com",
    cpf="12345678909",  # CPF válido
    senha="Senha@123",
    confirmar_senha="Senha@123"
)

if sucesso:
    print(f"Cliente criado: {cliente.nome} (ID: {cliente.id})")
else:
    print(f"Erro: {mensagem}")
```

### Login de Cliente

```python
# Fazer login
sucesso, mensagem, cliente = auth_controller.login_cliente(
    email="joao@exemplo.com",
    senha="Senha@123"
)

if sucesso:
    print(f"Login bem-sucedido: {cliente.nome}")
    cliente_id = cliente.id
else:
    print(f"Erro: {mensagem}")
```

### Criar Admin

```python
from models.admin import Admin
from argon2 import PasswordHasher

ph = PasswordHasher()

admin = Admin(
    nome="Administrador",
    email="admin@scee.com",
    senha_hash=ph.hash("Admin@123")
)

session.add(admin)
session.commit()
print(f"Admin criado: {admin.nome}")
```

---

## 3. Gerenciamento de Produtos

### Criar Categoria

```python
from models.categoria import Categoria

categoria = Categoria(nome="Smartphones")
session.add(categoria)
session.commit()
print(f"Categoria criada: {categoria.nome} (ID: {categoria.id})")
```

### Criar Produto

```python
from controllers.produto_controller import ProdutoController

# Criar controller
produto_controller = ProdutoController(session, upload_folder="static/uploads")

# Criar produto
sucesso, mensagem, produto = produto_controller.criar_produto(
    nome="iPhone 15 Pro",
    sku="IPH15PRO",
    descricao="Smartphone Apple com chip A17 Pro",
    preco=7999.00,
    estoque=10,
    categoria_id=categoria.id,
    imagens=None  # Ou lista de arquivos
)

if sucesso:
    print(f"Produto criado: {produto.nome} (ID: {produto.id})")
else:
    print(f"Erro: {mensagem}")
```

### Buscar Produtos

```python
from repositories.produto_repository import ProdutoRepository

produto_repo = ProdutoRepository(session)

# Buscar por ID
produto = produto_repo.get_by_id(1)
print(f"Produto: {produto.nome} - R$ {produto.preco}")

# Buscar por SKU
produto = produto_repo.get_by_sku("IPH15PRO")

# Buscar todos
produtos = produto_repo.get_all()

# Buscar por categoria
produtos = produto_repo.get_by_categoria(categoria_id=1, limit=12, offset=0)

# Buscar por texto
produtos = produto_repo.search("iPhone", limit=12, offset=0)

# Filtrar por preço
produtos = produto_repo.filter_by_price_range(
    min_price=5000.00,
    max_price=10000.00,
    limit=12,
    offset=0
)
```

### Atualizar Produto

```python
sucesso, mensagem = produto_controller.atualizar_produto(
    produto_id=1,
    nome="iPhone 15 Pro Max",
    descricao="Smartphone Apple com chip A17 Pro e tela maior",
    preco=8999.00,
    estoque=5,
    categoria_id=1
)

if sucesso:
    print("Produto atualizado com sucesso")
```

### Deletar Produto

```python
sucesso, mensagem = produto_controller.remover_produto(produto_id=1)

if sucesso:
    print("Produto removido com sucesso")
```

---

## 4. Gerenciamento de Endereços

### Adicionar Endereço

```python
from controllers.cliente_controller import ClienteController

cliente_controller = ClienteController(session)

sucesso, mensagem, endereco = cliente_controller.adicionar_endereco(
    cliente_id=cliente_id,
    rua="Rua das Flores",
    numero="123",
    complemento="Apto 45",
    bairro="Centro",
    cidade="São Paulo",
    estado="SP",
    cep="01234567"
)

if sucesso:
    print(f"Endereço adicionado: {endereco.rua}, {endereco.numero}")
```

### Listar Endereços

```python
enderecos = cliente_controller.listar_enderecos(cliente_id)

for endereco in enderecos:
    print(f"{endereco.rua}, {endereco.numero} - {endereco.cidade}/{endereco.estado}")
```

### Atualizar Endereço

```python
sucesso, mensagem = cliente_controller.atualizar_endereco(
    endereco_id=1,
    rua="Rua das Palmeiras",
    numero="456",
    complemento="Casa",
    bairro="Jardim",
    cidade="São Paulo",
    estado="SP",
    cep="01234567"
)
```

### Remover Endereço

```python
sucesso, mensagem = cliente_controller.remover_endereco(endereco_id=1)
```

---

## 5. Carrinho de Compras

### Criar Carrinho

```python
from controllers.carrinho_controller import CarrinhoController

carrinho = CarrinhoController()
```

### Adicionar Item ao Carrinho

```python
sucesso, mensagem = carrinho.adicionar_item(
    produto_id=1,
    nome="iPhone 15 Pro",
    preco=7999.00,
    quantidade=2
)

if sucesso:
    print("Item adicionado ao carrinho")
```

### Atualizar Quantidade

```python
sucesso, mensagem = carrinho.atualizar_quantidade(
    produto_id=1,
    quantidade=3
)
```

### Remover Item

```python
sucesso, mensagem = carrinho.remover_item(produto_id=1)
```

### Calcular Total

```python
total = carrinho.calcular_total()
print(f"Total do carrinho: R$ {total:.2f}")
```

### Obter Itens

```python
itens = carrinho.obter_itens()

for item in itens:
    print(f"{item.nome} - Qtd: {item.quantidade} - Subtotal: R$ {item.subtotal:.2f}")
```

---

## 6. Criação de Pedido

### Criar Pedido (Transação Atômica)

```python
from controllers.pedido_controller import PedidoController

pedido_controller = PedidoController(session)

# Obter itens do carrinho
itens_carrinho = carrinho.obter_itens()

# Criar pedido
sucesso, mensagem, pedido = pedido_controller.criar_pedido(
    cliente_id=cliente_id,
    itens_carrinho=itens_carrinho,
    endereco_id=1,
    metodo_pagamento="Cartão"
)

if sucesso:
    print(f"Pedido #{pedido.id} criado com sucesso!")
    print(f"Total: R$ {pedido.total:.2f}")
    print(f"Status: {pedido.status}")
    
    # Limpar carrinho
    carrinho.limpar()
else:
    print(f"Erro ao criar pedido: {mensagem}")
```

### Listar Pedidos do Cliente

```python
pedidos = pedido_controller.listar_pedidos_cliente(cliente_id)

for pedido in pedidos:
    print(f"Pedido #{pedido.id} - {pedido.data_pedido} - R$ {pedido.total:.2f} - {pedido.status}")
```

### Obter Detalhes do Pedido

```python
pedido = pedido_controller.obter_pedido(pedido_id=1)

if pedido:
    print(f"Pedido #{pedido.id}")
    print(f"Cliente: {pedido.cliente.nome}")
    print(f"Data: {pedido.data_pedido}")
    print(f"Status: {pedido.status}")
    print(f"Total: R$ {pedido.total:.2f}")
    print(f"Endereço: {pedido.endereco_entrega}")
    print(f"Pagamento: {pedido.metodo_pagamento}")
    
    print("\nItens:")
    for item in pedido.itens:
        print(f"  - {item.produto_nome} x{item.quantidade} = R$ {item.subtotal:.2f}")
```

---

## 7. Gerenciamento de Pedidos (Admin)

### Listar Todos os Pedidos

```python
pedidos, total, total_pages = pedido_controller.listar_todos_pedidos(
    page=1,
    per_page=50
)

print(f"Total de pedidos: {total}")
print(f"Total de páginas: {total_pages}")

for pedido in pedidos:
    print(f"Pedido #{pedido.id} - Cliente: {pedido.cliente.nome} - Status: {pedido.status}")
```

### Filtrar por Status

```python
pedidos, total, total_pages = pedido_controller.filtrar_por_status(
    status="Pendente",
    page=1,
    per_page=50
)

print(f"Pedidos pendentes: {total}")
```

### Atualizar Status do Pedido

```python
sucesso, mensagem = pedido_controller.atualizar_status(
    pedido_id=1,
    novo_status="Processando"
)

if sucesso:
    print("Status atualizado com sucesso")
```

**Status válidos:**
- Pendente
- Processando
- Enviado
- Entregue
- Cancelado

---

## 8. Validações

### Validar E-mail

```python
email_valido = auth_controller.validar_email("usuario@exemplo.com")
print(f"E-mail válido: {email_valido}")
```

### Validar CPF

```python
cpf_valido = auth_controller.validar_cpf("12345678909")
print(f"CPF válido: {cpf_valido}")
```

### Validar Senha Forte

```python
valida, mensagem = auth_controller.validar_senha_forte("Senha@123")

if valida:
    print("Senha válida")
else:
    print(f"Senha inválida: {mensagem}")
```

---

## 9. Consultas Avançadas

### Contar Produtos

```python
total_produtos = produto_repo.count_all()
print(f"Total de produtos: {total_produtos}")

total_categoria = produto_repo.count_by_categoria(categoria_id=1)
print(f"Produtos na categoria: {total_categoria}")
```

### Contar Pedidos

```python
from repositories.pedido_repository import PedidoRepository

pedido_repo = PedidoRepository(session)

total_pedidos = pedido_repo.count_all()
print(f"Total de pedidos: {total_pedidos}")

total_pendentes = pedido_repo.count_by_status("Pendente")
print(f"Pedidos pendentes: {total_pendentes}")
```

### Verificar Existência

```python
# Verificar se e-mail existe
email_existe = cliente_repo.email_exists("joao@exemplo.com")

# Verificar se CPF existe
cpf_existe = cliente_repo.cpf_exists("12345678909")

# Verificar se SKU existe
sku_existe = produto_repo.sku_exists("IPH15PRO")
```

---

## 10. Tratamento de Erros

### Exemplo com Try-Except

```python
try:
    sucesso, mensagem, pedido = pedido_controller.criar_pedido(
        cliente_id=cliente_id,
        itens_carrinho=itens_carrinho,
        endereco_id=1,
        metodo_pagamento="Cartão"
    )
    
    if sucesso:
        print(f"Pedido criado: #{pedido.id}")
    else:
        print(f"Erro: {mensagem}")
        
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
    session.rollback()
```

---

## 11. Paginação

### Produtos com Paginação

```python
page = 1
per_page = 12

produtos, total, total_pages = produto_controller.listar_produtos(
    page=page,
    per_page=per_page
)

print(f"Página {page} de {total_pages}")
print(f"Total de produtos: {total}")

for produto in produtos:
    print(f"- {produto.nome} (R$ {produto.preco:.2f})")
```

### Pedidos com Paginação

```python
page = 1
per_page = 50

pedidos, total, total_pages = pedido_controller.listar_todos_pedidos(
    page=page,
    per_page=per_page
)

print(f"Página {page} de {total_pages}")
print(f"Total de pedidos: {total}")
```

---

## 12. Relacionamentos

### Acessar Relacionamentos

```python
# Cliente -> Endereços
cliente = cliente_repo.get_by_id(1)
for endereco in cliente.enderecos:
    print(f"Endereço: {endereco.rua}, {endereco.numero}")

# Cliente -> Pedidos
for pedido in cliente.pedidos:
    print(f"Pedido #{pedido.id} - R$ {pedido.total:.2f}")

# Produto -> Categoria
produto = produto_repo.get_by_id(1)
print(f"Categoria: {produto.categoria.nome}")

# Produto -> Imagens
for imagem in produto.imagens:
    print(f"Imagem: {imagem.caminho}")

# Pedido -> Itens
pedido = pedido_repo.get_by_id(1)
for item in pedido.itens:
    print(f"Item: {item.produto_nome} x{item.quantidade}")
```

---

## 13. Fechar Sessão

### Sempre Fechar a Sessão

```python
# Ao final do uso
db.close_session()
```

---

## 14. Script Completo de Exemplo

```python
from database import Database
from controllers.auth_controller import AuthController
from controllers.produto_controller import ProdutoController
from controllers.carrinho_controller import CarrinhoController
from controllers.pedido_controller import PedidoController
from models.categoria import Categoria

# Inicializar
db = Database()
db.create_tables()
session = db.get_session()

# 1. Criar categoria
categoria = Categoria(nome="Smartphones")
session.add(categoria)
session.commit()

# 2. Registrar cliente
auth_controller = AuthController(session)
sucesso, msg, cliente = auth_controller.registrar_cliente(
    "João Silva", "joao@teste.com", "12345678909", "Senha@123", "Senha@123"
)
print(f"Cliente: {cliente.nome}")

# 3. Criar produto
produto_controller = ProdutoController(session, "static/uploads")
sucesso, msg, produto = produto_controller.criar_produto(
    "iPhone 15", "IPH15", "Smartphone Apple", 5999.00, 10, categoria.id
)
print(f"Produto: {produto.nome}")

# 4. Adicionar ao carrinho
carrinho = CarrinhoController()
carrinho.adicionar_item(produto.id, produto.nome, produto.preco, 2)
print(f"Total carrinho: R$ {carrinho.calcular_total():.2f}")

# 5. Adicionar endereço
from controllers.cliente_controller import ClienteController
cliente_controller = ClienteController(session)
sucesso, msg, endereco = cliente_controller.adicionar_endereco(
    cliente.id, "Rua A", "123", "", "Centro", "São Paulo", "SP", "01234567"
)

# 6. Criar pedido
pedido_controller = PedidoController(session)
itens = carrinho.obter_itens()
sucesso, msg, pedido = pedido_controller.criar_pedido(
    cliente.id, itens, endereco.id, "Cartão"
)
print(f"Pedido #{pedido.id} criado - R$ {pedido.total:.2f}")

# Fechar
db.close_session()
```

---

## 15. Dicas e Boas Práticas

### Use Context Manager (Recomendado)

```python
from contextlib import contextmanager

@contextmanager
def get_db_session():
    db = Database()
    session = db.get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        db.close_session()

# Uso
with get_db_session() as session:
    cliente_repo = ClienteRepository(session)
    cliente = cliente_repo.get_by_id(1)
    print(cliente.nome)
```

### Validar Antes de Salvar

```python
# Sempre valide dados antes de criar entidades
if not auth_controller.validar_email(email):
    print("E-mail inválido")
    return

if not auth_controller.validar_cpf(cpf):
    print("CPF inválido")
    return
```

### Tratar Transações

```python
try:
    session.begin_nested()
    # Operações
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Erro: {e}")
```

---

**Este guia cobre os principais casos de uso do sistema SCEE.**  
**Para mais detalhes, consulte os docstrings no código-fonte.**
