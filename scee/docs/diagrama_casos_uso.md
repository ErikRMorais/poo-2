# Diagrama de Casos de Uso UML - SCEE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SISTEMA SCEE - CASOS DE USO                               │
└─────────────────────────────────────────────────────────────────────────────┘


        ┌──────────┐
        │ Cliente  │
        └────┬─────┘
             │
             │
    ┌────────┼────────────────────────────────────────────────────┐
    │        │                                                    │
    │        │                                                    │
    ▼        ▼                                                    ▼
┌────────────────┐                                      ┌──────────────────┐
│ UC01: Registrar│                                      │ UC02: Fazer Login│
│     Conta      │                                      │                  │
└────────────────┘                                      └──────────────────┘
    │                                                            │
    │ <<include>>                                               │
    ▼                                                            ▼
┌────────────────┐                                      ┌──────────────────┐
│ Validar E-mail │                                      │   Autenticar     │
│   e CPF        │                                      │   Credenciais    │
└────────────────┘                                      └──────────────────┘
    │
    │ <<include>>
    ▼
┌────────────────┐
│ Validar Senha  │
│     Forte      │
└────────────────┘


        ┌──────────┐
        │ Cliente  │
        └────┬─────┘
             │
    ┌────────┼────────────────────────────────────────┐
    │        │                                        │
    ▼        ▼                                        ▼
┌────────────────┐  ┌──────────────────┐    ┌──────────────────┐
│ UC03: Visualizar│  │ UC04: Buscar     │    │ UC05: Filtrar    │
│    Produtos    │  │    Produtos      │    │    Produtos      │
└────────────────┘  └──────────────────┘    └──────────────────┘
         │                   │                        │
         │                   │                        │
         └───────────────────┴────────────────────────┘
                             │
                             │ <<extend>>
                             ▼
                    ┌──────────────────┐
                    │ Filtrar por Faixa│
                    │    de Preço      │
                    └──────────────────┘


        ┌──────────┐
        │ Cliente  │
        └────┬─────┘
             │
    ┌────────┼────────────────────────────────────────┐
    │        │                                        │
    ▼        ▼                                        ▼
┌────────────────┐  ┌──────────────────┐    ┌──────────────────┐
│ UC06: Adicionar│  │ UC07: Remover    │    │ UC08: Atualizar  │
│  ao Carrinho   │  │  do Carrinho     │    │   Quantidade     │
└────────────────┘  └──────────────────┘    └──────────────────┘
         │                   │                        │
         │                   │                        │
         └───────────────────┴────────────────────────┘
                             │
                             │ <<include>>
                             ▼
                    ┌──────────────────┐
                    │ Recalcular Total │
                    └──────────────────┘


        ┌──────────┐
        │ Cliente  │
        └────┬─────┘
             │
             │
             ▼
    ┌──────────────────┐
    │ UC09: Finalizar  │
    │      Compra      │
    │   (Checkout)     │
    └──────────────────┘
             │
             │ <<include>>
    ┌────────┼────────────────────────┐
    │        │                        │
    ▼        ▼                        ▼
┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Selecionar     │  │ Selecionar Método│  │ Criar Pedido     │
│   Endereço     │  │  de Pagamento    │  │                  │
└────────────────┘  └──────────────────┘  └──────────────────┘
                                                   │
                                                   │ <<include>>
                                          ┌────────┼────────────┐
                                          │        │            │
                                          ▼        ▼            ▼
                                    ┌─────────┐ ┌──────┐ ┌──────────┐
                                    │Verificar│ │Abater│ │  Enviar  │
                                    │ Estoque │ │Estoque│ │  E-mail  │
                                    └─────────┘ └──────┘ └──────────┘


        ┌──────────┐
        │ Cliente  │
        └────┬─────┘
             │
    ┌────────┼────────────────────────────────────────┐
    │        │                                        │
    ▼        ▼                                        ▼
┌────────────────┐  ┌──────────────────┐    ┌──────────────────┐
│ UC10: Gerenciar│  │ UC11: Adicionar  │    │ UC12: Atualizar  │
│     Perfil     │  │    Endereço      │    │    Endereço      │
└────────────────┘  └──────────────────┘    └──────────────────┘
         │                                            │
         │                                            │
         ▼                                            ▼
┌────────────────┐                          ┌──────────────────┐
│ UC13: Remover  │                          │ UC14: Visualizar │
│    Endereço    │                          │     Pedidos      │
└────────────────┘                          └──────────────────┘


        ┌──────────┐
        │  Admin   │
        └────┬─────┘
             │
    ┌────────┼────────────────────────────────────────┐
    │        │                                        │
    ▼        ▼                                        ▼
┌────────────────┐  ┌──────────────────┐    ┌──────────────────┐
│ UC15: Criar    │  │ UC16: Editar     │    │ UC17: Deletar    │
│    Produto     │  │    Produto       │    │    Produto       │
└────────────────┘  └──────────────────┘    └──────────────────┘
         │
         │ <<include>>
         ▼
┌────────────────┐
│ Upload Imagens │
│  (máx. 5)      │
└────────────────┘


        ┌──────────┐
        │  Admin   │
        └────┬─────┘
             │
    ┌────────┼────────────────────────────────────────┐
    │        │                                        │
    ▼        ▼                                        ▼
┌────────────────┐  ┌──────────────────┐    ┌──────────────────┐
│ UC18: Listar   │  │ UC19: Filtrar    │    │ UC20: Atualizar  │
│    Pedidos     │  │  por Status      │    │  Status Pedido   │
└────────────────┘  └──────────────────┘    └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        DESCRIÇÃO DOS CASOS DE USO                            │
└─────────────────────────────────────────────────────────────────────────────┘

MÓDULO DE AUTENTICAÇÃO E CONTAS
════════════════════════════════

UC01: Registrar Conta
─────────────────────
Ator: Cliente
Descrição: Cliente cria uma nova conta no sistema
Pré-condições: Nenhuma
Fluxo Principal:
  1. Cliente acessa página de registro
  2. Sistema exibe formulário
  3. Cliente preenche: Nome, E-mail, CPF, Senha, Confirmação de Senha
  4. Sistema valida e-mail único (include)
  5. Sistema valida CPF único e dígitos verificadores (include)
  6. Sistema valida senha forte (include)
  7. Sistema criptografa senha com Argon2
  8. Sistema cria conta e autentica automaticamente
Pós-condições: Cliente autenticado e redirecionado para "Minha Conta"

UC02: Fazer Login
─────────────────
Ator: Cliente ou Admin
Descrição: Usuário autentica-se no sistema
Pré-condições: Conta existente
Fluxo Principal:
  1. Usuário acessa página de login
  2. Sistema exibe formulário
  3. Usuário informa E-mail, Senha e Tipo (Cliente/Admin)
  4. Sistema autentica credenciais (include)
  5. Sistema redireciona conforme tipo de usuário
Pós-condições: Usuário autenticado


MÓDULO DE CATÁLOGO E PRODUTOS
══════════════════════════════

UC03: Visualizar Produtos
─────────────────────────
Ator: Cliente
Descrição: Cliente visualiza catálogo de produtos
Pré-condições: Nenhuma
Fluxo Principal:
  1. Cliente acessa página de produtos
  2. Sistema exibe grade paginada (12 por página)
  3. Cliente navega entre páginas
Pós-condições: Produtos exibidos

UC04: Buscar Produtos
─────────────────────
Ator: Cliente
Descrição: Cliente busca produtos por texto
Pré-condições: Nenhuma
Fluxo Principal:
  1. Cliente insere texto de busca
  2. Sistema busca em nome e descrição
  3. Sistema exibe resultados
Pós-condições: Resultados exibidos

UC05: Filtrar Produtos
──────────────────────
Ator: Cliente
Descrição: Cliente filtra produtos por categoria ou preço
Pré-condições: Nenhuma
Fluxo Principal:
  1. Cliente seleciona filtros
  2. Sistema aplica filtros
  3. Sistema exibe resultados filtrados
Extensões:
  - Filtrar por Faixa de Preço (extend)
Pós-condições: Produtos filtrados exibidos


MÓDULO DE CARRINHO
══════════════════

UC06: Adicionar ao Carrinho
───────────────────────────
Ator: Cliente
Descrição: Cliente adiciona produto ao carrinho
Pré-condições: Produto com estoque disponível
Fluxo Principal:
  1. Cliente seleciona produto e quantidade
  2. Sistema verifica estoque
  3. Sistema adiciona ao carrinho
  4. Sistema recalcula total (include)
Pós-condições: Produto adicionado ao carrinho

UC07: Remover do Carrinho
─────────────────────────
Ator: Cliente
Descrição: Cliente remove produto do carrinho
Pré-condições: Item no carrinho
Fluxo Principal:
  1. Cliente seleciona item para remover
  2. Sistema remove item
  3. Sistema recalcula total (include)
Pós-condições: Item removido

UC08: Atualizar Quantidade
──────────────────────────
Ator: Cliente
Descrição: Cliente altera quantidade de item no carrinho
Pré-condições: Item no carrinho
Fluxo Principal:
  1. Cliente altera quantidade
  2. Sistema atualiza quantidade
  3. Sistema recalcula total (include)
Pós-condições: Quantidade atualizada


MÓDULO DE CHECKOUT E PEDIDOS
════════════════════════════

UC09: Finalizar Compra (Checkout)
─────────────────────────────────
Ator: Cliente
Descrição: Cliente finaliza compra criando pedido
Pré-condições: Cliente autenticado, carrinho não vazio
Fluxo Principal:
  1. Cliente acessa checkout
  2. Sistema exibe resumo do pedido
  3. Cliente seleciona endereço de entrega (include)
  4. Cliente seleciona método de pagamento (include)
  5. Sistema cria pedido em transação atômica (include)
  6. Sistema verifica estoque (include)
  7. Sistema abate estoque (include)
  8. Sistema envia e-mail transacional (include)
  9. Sistema limpa carrinho
Pós-condições: Pedido criado, estoque atualizado

UC14: Visualizar Pedidos
───────────────────────
Ator: Cliente
Descrição: Cliente visualiza histórico de pedidos
Pré-condições: Cliente autenticado
Fluxo Principal:
  1. Cliente acessa "Minha Conta"
  2. Sistema exibe lista de pedidos
Pós-condições: Pedidos exibidos


MÓDULO DE PERFIL
════════════════

UC10: Gerenciar Perfil
─────────────────────
Ator: Cliente
Descrição: Cliente atualiza informações do perfil
Pré-condições: Cliente autenticado
Fluxo Principal:
  1. Cliente acessa "Minha Conta"
  2. Cliente atualiza nome
  3. Sistema salva alterações
Pós-condições: Perfil atualizado

UC11: Adicionar Endereço
───────────────────────
Ator: Cliente
Descrição: Cliente adiciona novo endereço de entrega
Pré-condições: Cliente autenticado
Fluxo Principal:
  1. Cliente preenche dados do endereço
  2. Sistema valida CEP e UF
  3. Sistema salva endereço
Pós-condições: Endereço adicionado

UC12: Atualizar Endereço
───────────────────────
Ator: Cliente
Descrição: Cliente atualiza endereço existente
Pré-condições: Cliente autenticado, endereço existente
Fluxo Principal:
  1. Cliente altera dados do endereço
  2. Sistema valida dados
  3. Sistema atualiza endereço
Pós-condições: Endereço atualizado

UC13: Remover Endereço
─────────────────────
Ator: Cliente
Descrição: Cliente remove endereço
Pré-condições: Cliente autenticado, endereço existente
Fluxo Principal:
  1. Cliente seleciona endereço para remover
  2. Sistema remove endereço
Pós-condições: Endereço removido


MÓDULO ADMINISTRATIVO - PRODUTOS
═════════════════════════════════

UC15: Criar Produto
──────────────────
Ator: Admin
Descrição: Admin cria novo produto no catálogo
Pré-condições: Admin autenticado
Fluxo Principal:
  1. Admin acessa formulário de criação
  2. Admin preenche: Nome, SKU, Descrição, Preço, Estoque, Categoria
  3. Admin faz upload de imagens (include, máx. 5)
  4. Sistema valida SKU único
  5. Sistema valida preço > 0
  6. Sistema cria produto
Pós-condições: Produto criado

UC16: Editar Produto
───────────────────
Ator: Admin
Descrição: Admin atualiza produto existente
Pré-condições: Admin autenticado, produto existente
Fluxo Principal:
  1. Admin seleciona produto
  2. Admin altera dados
  3. Sistema valida dados
  4. Sistema atualiza produto
Pós-condições: Produto atualizado

UC17: Deletar Produto
────────────────────
Ator: Admin
Descrição: Admin remove produto do catálogo
Pré-condições: Admin autenticado, produto existente
Fluxo Principal:
  1. Admin seleciona produto
  2. Admin confirma exclusão
  3. Sistema remove produto
Pós-condições: Produto removido


MÓDULO ADMINISTRATIVO - PEDIDOS
════════════════════════════════

UC18: Listar Pedidos
───────────────────
Ator: Admin
Descrição: Admin visualiza todos os pedidos
Pré-condições: Admin autenticado
Fluxo Principal:
  1. Admin acessa página de pedidos
  2. Sistema exibe lista paginada (50 por página)
Pós-condições: Pedidos exibidos

UC19: Filtrar por Status
───────────────────────
Ator: Admin
Descrição: Admin filtra pedidos por status
Pré-condições: Admin autenticado
Fluxo Principal:
  1. Admin seleciona status
  2. Sistema filtra pedidos
  3. Sistema exibe resultados
Pós-condições: Pedidos filtrados exibidos

UC20: Atualizar Status Pedido
─────────────────────────────
Ator: Admin
Descrição: Admin altera status de um pedido
Pré-condições: Admin autenticado, pedido existente
Fluxo Principal:
  1. Admin seleciona pedido
  2. Admin seleciona novo status
  3. Sistema atualiza status
Pós-condições: Status do pedido atualizado


┌─────────────────────────────────────────────────────────────────────────────┐
│                          RELACIONAMENTOS                                     │
└─────────────────────────────────────────────────────────────────────────────┘

<<include>>: Relacionamento obrigatório
- Validar E-mail e CPF é parte obrigatória de Registrar Conta
- Validar Senha Forte é parte obrigatória de Registrar Conta
- Recalcular Total é parte obrigatória das operações de carrinho
- Verificar/Abater Estoque é parte obrigatória de Criar Pedido

<<extend>>: Relacionamento opcional
- Filtrar por Faixa de Preço é uma extensão opcional de Filtrar Produtos
```
