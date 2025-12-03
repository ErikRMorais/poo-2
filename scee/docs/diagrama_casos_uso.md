# 📋 DIAGRAMA DE CASOS DE USO - SCEE

Representação dos casos de uso do sistema por tipo de usuário.

---

## 👥 ATORES

1. **Cliente** - Usuário que compra produtos
2. **Administrador** - Gerencia o sistema
3. **Sistema** - Processos automáticos

---

## 🎭 CASOS DE USO POR ATOR

### 👤 CLIENTE

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC01       │    │   UC02       │    │   UC03       │
│ Registrar    │    │ Fazer Login  │    │ Navegar      │
│ Conta        │    │              │    │ Produtos     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC04       │    │   UC05       │    │   UC06       │
│ Filtrar      │    │ Ver Detalhes │    │ Adicionar ao │
│ Produtos     │    │ Produto      │    │ Carrinho     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC07       │    │   UC08       │    │   UC09       │
│ Gerenciar    │    │ Finalizar    │    │ Escolher     │
│ Carrinho     │    │ Compra       │    │ Frete        │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC10       │    │   UC11       │    │   UC12       │
│ Gerenciar    │    │ Gerenciar    │    │ Ver          │
│ Perfil       │    │ Endereços    │    │ Pedidos      │
└──────────────┘    └──────────────┘    └──────────────┘
        │
        │
        ↓
┌──────────────┐
│   UC13       │
│ Cancelar     │
│ Pedido       │
└──────────────┘
```

---

### 👨‍💼 ADMINISTRADOR

```
┌─────────────────────────────────────────────────────────────┐
│                      ADMINISTRADOR                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC14       │    │   UC15       │    │   UC16       │
│ Fazer Login  │    │ Acessar      │    │ Gerenciar    │
│ Admin        │    │ Dashboard    │    │ Produtos     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC17       │    │   UC18       │    │   UC19       │
│ Criar        │    │ Editar       │    │ Deletar      │
│ Produto      │    │ Produto      │    │ Produto      │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC20       │    │   UC21       │    │   UC22       │
│ Gerenciar    │    │ Gerenciar    │    │ Atualizar    │
│ Imagens      │    │ Categorias   │    │ Status       │
│ Produto      │    │              │    │ Pedido       │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   UC23       │    │   UC24       │    │   UC25       │
│ Visualizar   │    │ Visualizar   │    │ Filtrar      │
│ Pedidos      │    │ Clientes     │    │ Pedidos      │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 📝 DETALHAMENTO DOS CASOS DE USO

### UC01: Registrar Conta
**Ator:** Cliente  
**Descrição:** Cliente cria nova conta no sistema  
**Pré-condições:** Nenhuma  
**Fluxo Principal:**
1. Cliente acessa página de registro
2. Preenche: nome, email, CPF, senha
3. Sistema valida CPF
4. Sistema valida email único
5. Sistema valida senha forte
6. Sistema cria conta com senha hash (Argon2)
7. Cliente é redirecionado para área logada

**Pós-condições:** Cliente cadastrado e logado

---

### UC02: Fazer Login
**Ator:** Cliente  
**Descrição:** Cliente acessa sua conta  
**Pré-condições:** Cliente cadastrado  
**Fluxo Principal:**
1. Cliente acessa página de login
2. Informa email e senha
3. Sistema valida credenciais
4. Sistema cria sessão
5. Cliente é redirecionado para página inicial

**Pós-condições:** Cliente autenticado

---

### UC03: Navegar Produtos
**Ator:** Cliente  
**Descrição:** Cliente visualiza catálogo de produtos  
**Pré-condições:** Nenhuma  
**Fluxo Principal:**
1. Cliente acessa página de produtos
2. Sistema lista produtos com paginação
3. Cliente visualiza: nome, preço, categoria, estoque

**Pós-condições:** Produtos exibidos

---

### UC04: Filtrar Produtos
**Ator:** Cliente  
**Descrição:** Cliente filtra produtos por critérios  
**Pré-condições:** Estar na página de produtos  
**Fluxo Principal:**
1. Cliente seleciona filtros:
   - Por categoria
   - Por faixa de preço
   - Por busca textual
2. Sistema aplica filtros
3. Sistema exibe produtos filtrados

**Pós-condições:** Produtos filtrados exibidos

---

### UC05: Ver Detalhes Produto
**Ator:** Cliente  
**Descrição:** Cliente visualiza detalhes de um produto  
**Pré-condições:** Produto existir  
**Fluxo Principal:**
1. Cliente clica em produto
2. Sistema exibe:
   - Carrossel de imagens
   - Nome, descrição, preço
   - Categoria, SKU
   - Estoque disponível
3. Cliente pode adicionar ao carrinho

**Pós-condições:** Detalhes exibidos

---

### UC06: Adicionar ao Carrinho
**Ator:** Cliente  
**Descrição:** Cliente adiciona produto ao carrinho  
**Pré-condições:** Produto com estoque  
**Fluxo Principal:**
1. Cliente seleciona quantidade
2. Cliente clica em "Adicionar ao Carrinho"
3. Sistema valida estoque
4. Sistema adiciona ao carrinho
5. Sistema exibe mensagem de sucesso

**Pós-condições:** Produto no carrinho

---

### UC07: Gerenciar Carrinho
**Ator:** Cliente  
**Descrição:** Cliente gerencia itens do carrinho  
**Pré-condições:** Ter itens no carrinho  
**Fluxo Principal:**
1. Cliente acessa carrinho
2. Cliente pode:
   - Atualizar quantidade
   - Remover item
   - Ver total
3. Sistema atualiza valores

**Pós-condições:** Carrinho atualizado

---

### UC08: Finalizar Compra
**Ator:** Cliente  
**Descrição:** Cliente finaliza pedido  
**Pré-condições:** Cliente logado, carrinho com itens  
**Fluxo Principal:**
1. Cliente acessa checkout
2. Cliente seleciona endereço de entrega
3. Cliente escolhe tipo de frete:
   - Fixo (R$ 15,00 - 7 dias)
   - Correios (R$ 15-35 - 5-12 dias)
   - Expresso (R$ 30-60 - 2-5 dias)
4. Sistema calcula frete (polimorfismo)
5. Cliente escolhe método de pagamento:
   - Cartão
   - Pix
   - Boleto
6. Sistema cria pedido
7. Sistema atualiza estoque
8. Sistema limpa carrinho

**Pós-condições:** Pedido criado, estoque atualizado

---

### UC09: Escolher Frete
**Ator:** Cliente  
**Descrição:** Cliente escolhe tipo de frete  
**Pré-condições:** Estar no checkout  
**Fluxo Principal:**
1. Sistema exibe opções de frete
2. Cliente seleciona tipo
3. Sistema calcula valor e prazo
4. Sistema exibe total com frete

**Pós-condições:** Frete selecionado

---

### UC10: Gerenciar Perfil
**Ator:** Cliente  
**Descrição:** Cliente edita dados pessoais  
**Pré-condições:** Cliente logado  
**Fluxo Principal:**
1. Cliente acessa "Minha Conta"
2. Cliente edita: nome, email
3. Sistema valida dados
4. Sistema atualiza perfil

**Pós-condições:** Perfil atualizado

---

### UC11: Gerenciar Endereços
**Ator:** Cliente  
**Descrição:** Cliente gerencia endereços de entrega  
**Pré-condições:** Cliente logado  
**Fluxo Principal:**
1. Cliente acessa endereços
2. Cliente pode:
   - Adicionar novo endereço
   - Editar endereço existente
   - Deletar endereço
3. Sistema valida CEP
4. Sistema salva alterações

**Pós-condições:** Endereços atualizados

---

### UC12: Ver Pedidos
**Ator:** Cliente  
**Descrição:** Cliente visualiza histórico de pedidos  
**Pré-condições:** Cliente logado  
**Fluxo Principal:**
1. Cliente acessa "Meus Pedidos"
2. Sistema lista pedidos com:
   - Data, status, total
   - Tipo de frete, valor frete
   - Prazo de entrega
3. Cliente pode ver detalhes

**Pós-condições:** Pedidos exibidos

---

### UC13: Cancelar Pedido
**Ator:** Cliente  
**Descrição:** Cliente cancela pedido  
**Pré-condições:** Pedido em status "Pendente" ou "Processando"  
**Fluxo Principal:**
1. Cliente seleciona pedido
2. Cliente clica em "Cancelar"
3. Sistema valida status
4. Sistema cancela pedido
5. Sistema devolve estoque

**Pós-condições:** Pedido cancelado, estoque devolvido

---

### UC14: Fazer Login Admin
**Ator:** Administrador  
**Descrição:** Admin acessa área administrativa  
**Pré-condições:** Ter conta admin  
**Fluxo Principal:**
1. Admin acessa /admin
2. Informa email e senha
3. Sistema valida credenciais admin
4. Admin é redirecionado para dashboard

**Pós-condições:** Admin autenticado

---

### UC15: Acessar Dashboard
**Ator:** Administrador  
**Descrição:** Admin visualiza painel administrativo  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
1. Admin acessa dashboard
2. Sistema exibe estatísticas:
   - Total de produtos
   - Total de pedidos
   - Total de clientes

**Pós-condições:** Dashboard exibido

---

### UC16-19: Gerenciar Produtos
**Ator:** Administrador  
**Descrição:** Admin gerencia produtos (CRUD)  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
- **Criar:** Admin preenche formulário, adiciona até 5 imagens
- **Editar:** Admin atualiza dados, adiciona/remove imagens
- **Deletar:** Admin remove produto
- **Listar:** Admin visualiza todos os produtos

**Pós-condições:** Produtos gerenciados

---

### UC20: Gerenciar Imagens Produto
**Ator:** Administrador  
**Descrição:** Admin gerencia imagens de produtos  
**Pré-condições:** Admin logado, produto existir  
**Fluxo Principal:**
1. Admin acessa edição de produto
2. Admin visualiza imagens atuais em grid
3. Admin pode:
   - Remover imagem (botão ✕)
   - Adicionar novas (até 5 total)
4. Sistema valida formatos (JPG, PNG)
5. Sistema salva alterações

**Pós-condições:** Imagens atualizadas

---

### UC21: Gerenciar Categorias
**Ator:** Administrador  
**Descrição:** Admin gerencia categorias (CRUD)  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
- **Criar:** Admin adiciona nova categoria
- **Editar:** Admin atualiza nome
- **Deletar:** Admin remove categoria (se sem produtos)
- **Listar:** Admin visualiza todas

**Pós-condições:** Categorias gerenciadas

---

### UC22: Atualizar Status Pedido
**Ator:** Administrador  
**Descrição:** Admin atualiza status de pedido  
**Pré-condições:** Admin logado, pedido existir  
**Fluxo Principal:**
1. Admin acessa pedidos
2. Admin seleciona pedido
3. Admin altera status:
   - Pendente
   - Processando
   - Enviado
   - Entregue
   - Cancelado
4. Sistema atualiza pedido

**Pós-condições:** Status atualizado

---

### UC23: Visualizar Pedidos
**Ator:** Administrador  
**Descrição:** Admin visualiza todos os pedidos  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
1. Admin acessa pedidos
2. Sistema lista pedidos com:
   - Cliente, data, total
   - Status, frete
3. Admin pode filtrar por status

**Pós-condições:** Pedidos exibidos

---

### UC24: Visualizar Clientes
**Ator:** Administrador  
**Descrição:** Admin visualiza clientes cadastrados  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
1. Admin acessa clientes
2. Sistema lista clientes com:
   - Nome, email, CPF
   - Data de cadastro
3. Admin pode ver pedidos do cliente

**Pós-condições:** Clientes exibidos

---

### UC25: Filtrar Pedidos
**Ator:** Administrador  
**Descrição:** Admin filtra pedidos por status  
**Pré-condições:** Admin logado  
**Fluxo Principal:**
1. Admin seleciona status
2. Sistema filtra pedidos
3. Sistema exibe resultados

**Pós-condições:** Pedidos filtrados exibidos

---

## 📊 RESUMO

**Total de Casos de Uso:** 25

### Por Ator:
- **Cliente:** 13 casos de uso
- **Administrador:** 12 casos de uso

### Por Categoria:
- **Autenticação:** 3 (UC01, UC02, UC14)
- **Produtos:** 8 (UC03-UC05, UC16-UC20)
- **Carrinho/Compra:** 4 (UC06-UC09)
- **Perfil/Endereços:** 2 (UC10, UC11)
- **Pedidos:** 5 (UC12, UC13, UC22, UC23, UC25)
- **Categorias:** 1 (UC21)
- **Clientes:** 1 (UC24)
- **Dashboard:** 1 (UC15)

---

**Diagrama completo de casos de uso do SCEE** 📋
