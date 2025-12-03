# 🗄️ DIAGRAMA DO BANCO DE DADOS - SCEE

Esquema completo do banco de dados SQLite com relacionamentos.

---

## 📊 VISÃO GERAL

**Banco:** SQLite (`scee_loja.db`)  
**ORM:** SQLAlchemy 2.0.35  
**Total de Tabelas:** 8

---

## 📋 TABELAS E RELACIONAMENTOS

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  clientes   │ 1     N │  enderecos  │         │   admins    │
│─────────────│◄────────│─────────────│         │─────────────│
│ id (PK)     │         │ id (PK)     │         │ id (PK)     │
│ nome        │         │ cliente_id  │         │ nome        │
│ email       │         │ rua         │         │ email       │
│ cpf         │         │ numero      │         │ senha_hash  │
│ senha_hash  │         │ complemento │         └─────────────┘
└─────────────┘         │ bairro      │
       │                │ cidade      │
       │ 1              │ estado      │
       │                │ cep         │
       │                └─────────────┘
       │
       │ N
       ↓
┌─────────────┐
│   pedidos   │
│─────────────│
│ id (PK)     │
│ cliente_id  │
│ data_pedido │
│ status      │
│ total       │
│ endereco_   │
│   entrega   │
│ metodo_     │
│   pagamento │
│ tipo_frete  │
│ valor_frete │
│ prazo_      │
│   entrega   │
└─────────────┘
       │ 1
       │
       │ N
       ↓
┌─────────────┐         ┌─────────────┐
│ itens_      │ N     1 │  produtos   │
│   pedido    │────────►│─────────────│
│─────────────│         │ id (PK)     │
│ id (PK)     │         │ nome        │
│ pedido_id   │         │ sku         │
│ produto_id  │         │ descricao   │
│ quantidade  │         │ preco       │
│ preco_      │         │ estoque     │
│   unitario  │         │ categoria_id│
└─────────────┘         └─────────────┘
                               │ N
                               │
                               │ 1
                               ↓
                        ┌─────────────┐
                        │ categorias  │
                        │─────────────│
                        │ id (PK)     │
                        │ nome        │
                        └─────────────┘

┌─────────────┐
│  produtos   │ 1
│─────────────│
│ id (PK)     │
└─────────────┘
       │
       │ N
       ↓
┌─────────────┐
│ imagens_    │
│   produto   │
│─────────────│
│ id (PK)     │
│ produto_id  │
│ caminho     │
│ ordem       │
└─────────────┘
```

---

## 📝 DETALHAMENTO DAS TABELAS

### 1. **clientes**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(200) | NOT NULL | Nome completo |
| email | VARCHAR(200) | NOT NULL, UNIQUE | Email único |
| cpf | VARCHAR(14) | NOT NULL, UNIQUE | CPF único |
| senha_hash | VARCHAR(255) | NOT NULL | Senha com Argon2 |

**Relacionamentos:**
- 1:N com `enderecos`
- 1:N com `pedidos`

**Índices:**
- PRIMARY KEY (id)
- UNIQUE (email)
- UNIQUE (cpf)

---

### 2. **admins**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(200) | NOT NULL | Nome completo |
| email | VARCHAR(200) | NOT NULL, UNIQUE | Email único |
| senha_hash | VARCHAR(255) | NOT NULL | Senha com Argon2 |

**Relacionamentos:** Nenhum

**Índices:**
- PRIMARY KEY (id)
- UNIQUE (email)

**Dados Padrão:**
- Email: admin@scee.com
- Senha: Admin@123

---

### 3. **enderecos**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| cliente_id | INTEGER | FK, NOT NULL | Referência ao cliente |
| rua | VARCHAR(200) | NOT NULL | Nome da rua |
| numero | VARCHAR(20) | NOT NULL | Número |
| complemento | VARCHAR(100) | NULL | Complemento opcional |
| bairro | VARCHAR(100) | NOT NULL | Bairro |
| cidade | VARCHAR(100) | NOT NULL | Cidade |
| estado | VARCHAR(2) | NOT NULL | UF (2 letras) |
| cep | VARCHAR(9) | NOT NULL | CEP (formato: 00000-000) |

**Relacionamentos:**
- N:1 com `clientes`

**Índices:**
- PRIMARY KEY (id)
- FOREIGN KEY (cliente_id) REFERENCES clientes(id)
- INDEX (cliente_id)

---

### 4. **categorias**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(100) | NOT NULL, UNIQUE | Nome da categoria |

**Relacionamentos:**
- 1:N com `produtos`

**Índices:**
- PRIMARY KEY (id)
- UNIQUE (nome)

**Dados Padrão:**
1. Smartphones
2. Notebooks
3. Periféricos
4. Componentes
5. Áudio
6. Tablets
7. Smartwatches
8. Câmeras
9. Games
10. Acessórios

---

### 5. **produtos**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| nome | VARCHAR(200) | NOT NULL | Nome do produto |
| sku | VARCHAR(50) | NOT NULL, UNIQUE | Código único |
| descricao | TEXT | NOT NULL | Descrição detalhada |
| preco | FLOAT | NOT NULL | Preço unitário |
| estoque | INTEGER | NOT NULL, DEFAULT 0 | Quantidade em estoque |
| categoria_id | INTEGER | FK, NOT NULL | Referência à categoria |

**Relacionamentos:**
- N:1 com `categorias`
- 1:N com `imagens_produto`
- 1:N com `itens_pedido`

**Índices:**
- PRIMARY KEY (id)
- UNIQUE (sku)
- FOREIGN KEY (categoria_id) REFERENCES categorias(id)
- INDEX (categoria_id)
- INDEX (preco)

**Validações:**
- preco > 0
- estoque >= 0

---

### 6. **imagens_produto**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| produto_id | INTEGER | FK, NOT NULL | Referência ao produto |
| caminho | VARCHAR(500) | NOT NULL | Caminho da imagem |
| ordem | INTEGER | NOT NULL, DEFAULT 0 | Ordem de exibição |

**Relacionamentos:**
- N:1 com `produtos`

**Índices:**
- PRIMARY KEY (id)
- FOREIGN KEY (produto_id) REFERENCES produtos(id)
- INDEX (produto_id)

**Regras:**
- Máximo 5 imagens por produto
- Formatos aceitos: JPG, JPEG, PNG
- Tamanho máximo: 2MB por imagem

---

### 7. **pedidos**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| cliente_id | INTEGER | FK, NOT NULL | Referência ao cliente |
| data_pedido | DATETIME | NOT NULL, DEFAULT NOW | Data/hora do pedido |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'Pendente' | Status atual |
| total | FLOAT | NOT NULL | Valor total |
| endereco_entrega | VARCHAR(500) | NOT NULL | Endereço completo |
| metodo_pagamento | VARCHAR(50) | NOT NULL | Método escolhido |
| tipo_frete | VARCHAR(50) | NOT NULL, DEFAULT 'Fixo' | Tipo de frete |
| valor_frete | FLOAT | NOT NULL, DEFAULT 0.0 | Valor do frete |
| prazo_entrega | INTEGER | NOT NULL, DEFAULT 7 | Prazo em dias |

**Relacionamentos:**
- N:1 com `clientes`
- 1:N com `itens_pedido`

**Índices:**
- PRIMARY KEY (id)
- FOREIGN KEY (cliente_id) REFERENCES clientes(id)
- INDEX (cliente_id)
- INDEX (status)
- INDEX (data_pedido)

**Status Possíveis:**
- Pendente
- Processando
- Enviado
- Entregue
- Cancelado

**Métodos de Pagamento:**
- Cartão
- Pix
- Boleto

**Tipos de Frete:**
- Fixo (R$ 15,00 - 7 dias)
- Correios (R$ 15-35 - 5-12 dias)
- Expresso (R$ 30-60 - 2-5 dias)

---

### 8. **itens_pedido**

| Coluna | Tipo | Restrições | Descrição |
|--------|------|------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| pedido_id | INTEGER | FK, NOT NULL | Referência ao pedido |
| produto_id | INTEGER | FK, NOT NULL | Referência ao produto |
| quantidade | INTEGER | NOT NULL | Quantidade comprada |
| preco_unitario | FLOAT | NOT NULL | Preço no momento da compra |

**Relacionamentos:**
- N:1 com `pedidos`
- N:1 com `produtos`

**Índices:**
- PRIMARY KEY (id)
- FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
- FOREIGN KEY (produto_id) REFERENCES produtos(id)
- INDEX (pedido_id)
- INDEX (produto_id)

**Validações:**
- quantidade > 0
- preco_unitario > 0

---

## 🔗 RELACIONAMENTOS DETALHADOS

### Cliente → Endereço (1:N)
```sql
clientes.id ──┐
              │ 1:N
              └──► enderecos.cliente_id
```
- Um cliente pode ter vários endereços
- Um endereço pertence a apenas um cliente
- Cascade: DELETE (deletar cliente deleta endereços)

### Cliente → Pedido (1:N)
```sql
clientes.id ──┐
              │ 1:N
              └──► pedidos.cliente_id
```
- Um cliente pode ter vários pedidos
- Um pedido pertence a apenas um cliente
- Cascade: RESTRICT (não pode deletar cliente com pedidos)

### Categoria → Produto (1:N)
```sql
categorias.id ──┐
                │ 1:N
                └──► produtos.categoria_id
```
- Uma categoria pode ter vários produtos
- Um produto pertence a apenas uma categoria
- Cascade: RESTRICT (não pode deletar categoria com produtos)

### Produto → ImagemProduto (1:N)
```sql
produtos.id ──┐
              │ 1:N (máx. 5)
              └──► imagens_produto.produto_id
```
- Um produto pode ter até 5 imagens
- Uma imagem pertence a apenas um produto
- Cascade: DELETE (deletar produto deleta imagens)

### Pedido → ItemPedido (1:N)
```sql
pedidos.id ──┐
             │ 1:N
             └──► itens_pedido.pedido_id
```
- Um pedido pode ter vários itens
- Um item pertence a apenas um pedido
- Cascade: DELETE (deletar pedido deleta itens)

### Produto → ItemPedido (1:N)
```sql
produtos.id ──┐
              │ 1:N
              └──► itens_pedido.produto_id
```
- Um produto pode estar em vários pedidos
- Um item de pedido referencia um produto
- Cascade: RESTRICT (não pode deletar produto em pedidos)

---

## 📊 ESTATÍSTICAS

### Tamanhos Estimados:
- **clientes:** ~50 bytes por registro
- **enderecos:** ~100 bytes por registro
- **produtos:** ~200 bytes por registro
- **pedidos:** ~150 bytes por registro
- **itens_pedido:** ~30 bytes por registro

### Crescimento Esperado:
- **clientes:** Crescimento linear
- **produtos:** Crescimento controlado (admin)
- **pedidos:** Crescimento exponencial
- **itens_pedido:** Crescimento exponencial

---

## 🔒 SEGURANÇA

### Senhas:
- **Hash:** Argon2 (vencedor do Password Hashing Competition)
- **Salt:** Automático por registro
- **Custo:** Padrão (seguro)

### Validações:
- **CPF:** Validação de formato e dígitos verificadores
- **Email:** Validação de formato e unicidade
- **CEP:** Validação de formato (00000-000)
- **Senha:** Mínimo 8 caracteres, maiúscula, minúscula, número, especial

---

## 🎯 INTEGRIDADE REFERENCIAL

### Chaves Estrangeiras:
- ✅ Todas as FKs configuradas
- ✅ Cascades apropriados
- ✅ Índices em FKs para performance

### Constraints:
- ✅ NOT NULL onde necessário
- ✅ UNIQUE para emails, CPF, SKU
- ✅ DEFAULT values apropriados
- ✅ CHECK constraints (via SQLAlchemy)

---

## 📝 SCRIPTS SQL

### Criar Banco:
```sql
-- Executado automaticamente por init_db.py
-- Usa SQLAlchemy ORM para criar tabelas
```

### Backup:
```bash
# Backup do banco SQLite
cp scee_loja.db scee_loja_backup.db
```

### Resetar Banco:
```bash
# Deletar banco e recriar
rm scee_loja.db
python init_db.py
```

---

**Diagrama completo do banco de dados SCEE** 🗄️
