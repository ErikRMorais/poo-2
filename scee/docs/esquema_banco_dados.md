# Esquema do Banco de Dados - SCEE

## Arquivo: scee_loja.db (SQLite 3)

---

## Tabelas

### 1. clientes

Armazena informações dos clientes cadastrados.

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_cpf ON clientes(cpf);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `nome`: Nome completo do cliente
- `email`: E-mail único (índice para busca rápida)
- `cpf`: CPF único com 11 dígitos (índice para busca rápida)
- `senha_hash`: Senha criptografada com Argon2 (hash + salt)

**Restrições:**
- E-mail e CPF devem ser únicos
- Todos os campos são obrigatórios (NOT NULL)

---

### 2. admins

Armazena informações dos administradores do sistema.

```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE INDEX idx_admins_email ON admins(email);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `nome`: Nome do administrador
- `email`: E-mail único (índice para busca rápida)
- `senha_hash`: Senha criptografada com Argon2

**Restrições:**
- E-mail deve ser único
- Todos os campos são obrigatórios

---

### 3. enderecos

Armazena endereços de entrega dos clientes.

```sql
CREATE TABLE enderecos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    rua VARCHAR(200) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    complemento VARCHAR(100),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR(8) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `cliente_id`: Referência ao cliente (chave estrangeira)
- `rua`: Nome da rua
- `numero`: Número do imóvel
- `complemento`: Complemento (opcional)
- `bairro`: Bairro
- `cidade`: Cidade
- `estado`: UF com 2 caracteres
- `cep`: CEP com 8 dígitos

**Restrições:**
- `cliente_id` é chave estrangeira para `clientes(id)`
- DELETE CASCADE: ao deletar cliente, seus endereços são removidos
- Complemento é opcional, demais campos obrigatórios

---

### 4. categorias

Armazena categorias de produtos.

```sql
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE
);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `nome`: Nome da categoria (único)

**Restrições:**
- Nome deve ser único

---

### 5. produtos

Armazena informações dos produtos do catálogo.

```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    CHECK (preco > 0),
    CHECK (estoque >= 0)
);

CREATE INDEX idx_produtos_sku ON produtos(sku);
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `nome`: Nome do produto
- `sku`: SKU único (índice para busca rápida)
- `descricao`: Descrição detalhada
- `preco`: Preço unitário (deve ser > 0)
- `estoque`: Quantidade em estoque (deve ser >= 0)
- `categoria_id`: Referência à categoria (chave estrangeira)

**Restrições:**
- SKU deve ser único
- Preço deve ser maior que zero (CHECK)
- Estoque não pode ser negativo (CHECK)
- `categoria_id` é chave estrangeira para `categorias(id)`

---

### 6. imagens_produto

Armazena caminhos das imagens dos produtos.

```sql
CREATE TABLE imagens_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    ordem INTEGER DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `produto_id`: Referência ao produto (chave estrangeira)
- `caminho`: Caminho do arquivo de imagem
- `ordem`: Ordem de exibição (0 = primeira imagem)

**Restrições:**
- `produto_id` é chave estrangeira para `produtos(id)`
- DELETE CASCADE: ao deletar produto, suas imagens são removidas
- Máximo de 5 imagens por produto (validado na aplicação)

---

### 7. pedidos

Armazena informações dos pedidos realizados.

```sql
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    total REAL NOT NULL,
    endereco_entrega VARCHAR(500) NOT NULL,
    metodo_pagamento VARCHAR(50) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CHECK (total > 0)
);

CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_status ON pedidos(status);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `cliente_id`: Referência ao cliente (chave estrangeira)
- `data_pedido`: Data e hora do pedido (timestamp automático)
- `status`: Status do pedido (Pendente, Processando, Enviado, Entregue, Cancelado)
- `total`: Valor total do pedido (deve ser > 0)
- `endereco_entrega`: Endereço completo de entrega (texto)
- `metodo_pagamento`: Método de pagamento (Cartão ou Pix)

**Restrições:**
- `cliente_id` é chave estrangeira para `clientes(id)`
- Total deve ser maior que zero (CHECK)
- Índices em cliente_id e status para buscas rápidas

---

### 8. itens_pedido

Armazena os itens de cada pedido.

```sql
CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    produto_nome VARCHAR(200) NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    CHECK (quantidade > 0),
    CHECK (preco_unitario > 0),
    CHECK (subtotal > 0)
);

CREATE INDEX idx_itens_pedido ON itens_pedido(pedido_id);
```

**Campos:**
- `id`: Identificador único (chave primária)
- `pedido_id`: Referência ao pedido (chave estrangeira)
- `produto_id`: Referência ao produto (chave estrangeira)
- `produto_nome`: Nome do produto no momento da compra (snapshot)
- `quantidade`: Quantidade comprada
- `preco_unitario`: Preço unitário no momento da compra (snapshot)
- `subtotal`: Subtotal do item (quantidade × preço_unitario)

**Restrições:**
- `pedido_id` é chave estrangeira para `pedidos(id)`
- DELETE CASCADE: ao deletar pedido, seus itens são removidos
- `produto_id` é chave estrangeira para `produtos(id)`
- Quantidade, preço unitário e subtotal devem ser > 0 (CHECK)
- Armazena snapshot do nome e preço para histórico

---

## Relacionamentos

### Diagrama ER (Entity-Relationship)

```
clientes (1) ──────< (N) enderecos
    │
    │ (1)
    │
    └──────< (N) pedidos
                  │
                  │ (1)
                  │
                  └──────< (N) itens_pedido
                                │
                                │ (N)
                                │
                                └──────> (1) produtos
                                              │
                                              │ (N)
                                              │
                                    ┌─────────┴─────────┐
                                    │                   │
                                    ▼ (1)               ▼ (1)
                              categorias        imagens_produto (N)
```

### Cardinalidades

1. **Cliente → Endereço**: 1:N
   - Um cliente pode ter múltiplos endereços
   - Um endereço pertence a um único cliente

2. **Cliente → Pedido**: 1:N
   - Um cliente pode ter múltiplos pedidos
   - Um pedido pertence a um único cliente

3. **Pedido → ItemPedido**: 1:N
   - Um pedido contém múltiplos itens
   - Um item pertence a um único pedido

4. **Produto → ItemPedido**: 1:N
   - Um produto pode estar em múltiplos itens de pedido
   - Um item de pedido referencia um único produto

5. **Categoria → Produto**: 1:N
   - Uma categoria contém múltiplos produtos
   - Um produto pertence a uma única categoria

6. **Produto → ImagemProduto**: 1:N
   - Um produto pode ter múltiplas imagens (máx. 5)
   - Uma imagem pertence a um único produto

---

## Integridade Referencial

### Chaves Estrangeiras com DELETE CASCADE

- `enderecos.cliente_id` → `clientes.id` (CASCADE)
- `imagens_produto.produto_id` → `produtos.id` (CASCADE)
- `itens_pedido.pedido_id` → `pedidos.id` (CASCADE)

**Comportamento:**
- Ao deletar um cliente, todos os seus endereços são removidos automaticamente
- Ao deletar um produto, todas as suas imagens são removidas automaticamente
- Ao deletar um pedido, todos os seus itens são removidos automaticamente

### Chaves Estrangeiras sem CASCADE

- `produtos.categoria_id` → `categorias.id`
- `pedidos.cliente_id` → `clientes.id`
- `itens_pedido.produto_id` → `produtos.id`

**Comportamento:**
- Não permite deletar categoria que possui produtos
- Não permite deletar cliente que possui pedidos
- Não permite deletar produto que está em itens de pedido

---

## Índices

Índices criados para otimizar consultas frequentes:

1. `idx_clientes_email`: Busca rápida de clientes por e-mail (login)
2. `idx_clientes_cpf`: Busca rápida de clientes por CPF (validação)
3. `idx_admins_email`: Busca rápida de admins por e-mail (login)
4. `idx_produtos_sku`: Busca rápida de produtos por SKU (validação)
5. `idx_produtos_categoria`: Listagem rápida de produtos por categoria
6. `idx_pedidos_cliente`: Listagem rápida de pedidos por cliente
7. `idx_pedidos_status`: Filtragem rápida de pedidos por status
8. `idx_itens_pedido`: Busca rápida de itens por pedido

---

## Constraints (Restrições)

### CHECK Constraints

- `produtos.preco > 0`: Preço deve ser positivo
- `produtos.estoque >= 0`: Estoque não pode ser negativo
- `pedidos.total > 0`: Total do pedido deve ser positivo
- `itens_pedido.quantidade > 0`: Quantidade deve ser positiva
- `itens_pedido.preco_unitario > 0`: Preço unitário deve ser positivo
- `itens_pedido.subtotal > 0`: Subtotal deve ser positivo

### UNIQUE Constraints

- `clientes.email`: E-mail único por cliente
- `clientes.cpf`: CPF único por cliente
- `admins.email`: E-mail único por admin
- `categorias.nome`: Nome único por categoria
- `produtos.sku`: SKU único por produto

---

## Transações Atômicas

### Criação de Pedido

A criação de um pedido é realizada em uma transação atômica para garantir consistência:

```sql
BEGIN TRANSACTION;

-- 1. Verificar estoque de todos os produtos
SELECT estoque FROM produtos WHERE id IN (...);

-- 2. Criar pedido
INSERT INTO pedidos (...) VALUES (...);

-- 3. Criar itens do pedido
INSERT INTO itens_pedido (...) VALUES (...);

-- 4. Abater estoque
UPDATE produtos SET estoque = estoque - ? WHERE id = ?;

COMMIT;
-- Em caso de erro: ROLLBACK;
```

**Garantias:**
- Se qualquer etapa falhar, toda a transação é revertida (ROLLBACK)
- Evita race conditions no estoque
- Garante integridade entre pedido, itens e estoque

---

## Segurança

### Criptografia de Senhas

- Algoritmo: **Argon2** (vencedor do Password Hashing Competition)
- Método: Hash + Salt automático
- Biblioteca: `argon2-cffi`
- Armazenamento: Campo `senha_hash` (255 caracteres)

**Exemplo de hash Argon2:**
```
$argon2id$v=19$m=65536,t=3,p=4$randomsalt$hashedpassword
```

### Validações

1. **E-mail**: Formato válido (regex)
2. **CPF**: 11 dígitos + validação de dígitos verificadores
3. **Senha Forte**: 
   - Mínimo 8 caracteres
   - Pelo menos 1 maiúscula
   - Pelo menos 1 minúscula
   - Pelo menos 1 número

---

## Inicialização

Para criar o banco de dados com dados iniciais:

```bash
python init_db.py
```

Isso criará:
- Todas as tabelas com restrições
- Categorias padrão (Smartphones, Notebooks, etc.)
- Admin padrão (admin@scee.com / Admin@123)
