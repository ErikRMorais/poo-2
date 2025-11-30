# Diagrama de Classes UML - SCEE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAMADA MODEL (Entidades)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│      Cliente         │
├──────────────────────┤
│ - id: int            │
│ - nome: str          │
│ - email: str         │
│ - cpf: str           │
│ - senha_hash: str    │
├──────────────────────┤
│ + __repr__()         │
└──────────────────────┘
         │ 1
         │
         │ *
┌──────────────────────┐         ┌──────────────────────┐
│      Endereco        │         │       Pedido         │
├──────────────────────┤         ├──────────────────────┤
│ - id: int            │         │ - id: int            │
│ - cliente_id: int    │◄────────│ - cliente_id: int    │
│ - rua: str           │         │ - data_pedido: date  │
│ - numero: str        │         │ - status: str        │
│ - complemento: str   │         │ - total: float       │
│ - bairro: str        │         │ - endereco_entrega   │
│ - cidade: str        │         │ - metodo_pagamento   │
│ - estado: str        │         ├──────────────────────┤
│ - cep: str           │         │ + __repr__()         │
├──────────────────────┤         └──────────────────────┘
│ + __repr__()         │                  │ 1
└──────────────────────┘                  │
                                          │ *
┌──────────────────────┐         ┌──────────────────────┐
│       Admin          │         │    ItemPedido        │
├──────────────────────┤         ├──────────────────────┤
│ - id: int            │         │ - id: int            │
│ - nome: str          │         │ - pedido_id: int     │
│ - email: str         │         │ - produto_id: int    │
│ - senha_hash: str    │         │ - produto_nome: str  │
├──────────────────────┤         │ - quantidade: int    │
│ + __repr__()         │         │ - preco_unitario     │
└──────────────────────┘         │ - subtotal: float    │
                                 ├──────────────────────┤
                                 │ + __repr__()         │
┌──────────────────────┐         └──────────────────────┘
│     Categoria        │                  │
├──────────────────────┤                  │
│ - id: int            │                  │
│ - nome: str          │                  ▼
├──────────────────────┤         ┌──────────────────────┐
│ + __repr__()         │         │      Produto         │
└──────────────────────┘         ├──────────────────────┤
         │ 1                     │ - id: int            │
         │                       │ - nome: str          │
         │ *                     │ - sku: str           │
         └───────────────────────┤ - descricao: str     │
                                 │ - preco: float       │
                                 │ - estoque: int       │
                                 │ - categoria_id: int  │
                                 ├──────────────────────┤
                                 │ + __repr__()         │
                                 └──────────────────────┘
                                          │ 1
                                          │
                                          │ *
                                 ┌──────────────────────┐
                                 │   ImagemProduto      │
                                 ├──────────────────────┤
                                 │ - id: int            │
                                 │ - produto_id: int    │
                                 │ - caminho: str       │
                                 │ - ordem: int         │
                                 ├──────────────────────┤
                                 │ + __repr__()         │
                                 └──────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      CAMADA REPOSITORY (Persistência)                        │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌──────────────────────────┐
                        │   BaseRepository<T>      │
                        ├──────────────────────────┤
                        │ # model: type            │
                        │ # session: Session       │
                        ├──────────────────────────┤
                        │ + create(entity: T): T   │
                        │ + get_by_id(id): T       │
                        │ + get_all(): List[T]     │
                        │ + update(entity: T): T   │
                        │ + delete(entity: T)      │
                        └──────────────────────────┘
                                    △
                    ┌───────────────┼───────────────┐
                    │               │               │
        ┌───────────────────┐ ┌──────────────┐ ┌──────────────┐
        │ClienteRepository  │ │ProdutoRepo   │ │PedidoRepo    │
        ├───────────────────┤ ├──────────────┤ ├──────────────┤
        │+get_by_email()    │ │+get_by_sku() │ │+get_by_      │
        │+get_by_cpf()      │ │+search()     │ │ cliente()    │
        │+email_exists()    │ │+filter_by_   │ │+get_by_      │
        │+cpf_exists()      │ │ price_range()│ │ status()     │
        └───────────────────┘ └──────────────┘ └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAMADA CONTROLLER (Lógica de Negócios)                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│    AuthController        │  │   ClienteController      │
├──────────────────────────┤  ├──────────────────────────┤
│ - session: Session       │  │ - session: Session       │
│ - cliente_repo           │  │ - cliente_repo           │
│ - admin_repo             │  │ - endereco_repo          │
│ - ph: PasswordHasher     │  ├──────────────────────────┤
├──────────────────────────┤  │ + atualizar_nome()       │
│ + validar_email()        │  │ + adicionar_endereco()   │
│ + validar_cpf()          │  │ + listar_enderecos()     │
│ + validar_senha_forte()  │  │ + atualizar_endereco()   │
│ + registrar_cliente()    │  │ + remover_endereco()     │
│ + login_cliente()        │  └──────────────────────────┘
│ + login_admin()          │
└──────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│   ProdutoController      │  │   CarrinhoController     │
├──────────────────────────┤  ├──────────────────────────┤
│ - session: Session       │  │ - itens: Dict            │
│ - produto_repo           │  ├──────────────────────────┤
│ - categoria_repo         │  │ + adicionar_item()       │
│ - upload_folder          │  │ + remover_item()         │
├──────────────────────────┤  │ + atualizar_quantidade() │
│ + validar_extensao()     │  │ + calcular_total()       │
│ + criar_produto()        │  │ + obter_itens()          │
│ + atualizar_produto()    │  │ + limpar()               │
│ + remover_produto()      │  │ + quantidade_itens()     │
│ + listar_produtos()      │  └──────────────────────────┘
│ + buscar_produtos()      │
│ + filtrar_por_preco()    │  ┌──────────────────────────┐
└──────────────────────────┘  │    ItemCarrinho          │
                              ├──────────────────────────┤
┌──────────────────────────┐  │ - produto_id: int        │
│    PedidoController      │  │ - nome: str              │
├──────────────────────────┤  │ - preco: float           │
│ - session: Session       │  │ - quantidade: int        │
│ - pedido_repo            │  │ - subtotal: float        │
│ - produto_repo           │  ├──────────────────────────┤
│ - endereco_repo          │  │ + atualizar_quantidade() │
├──────────────────────────┤  └──────────────────────────┘
│ + criar_pedido()         │
│ + listar_pedidos_        │
│   cliente()              │
│ + listar_todos_pedidos() │
│ + filtrar_por_status()   │
│ + atualizar_status()     │
│ + obter_pedido()         │
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          CAMADA VIEW (Flask App)                             │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌──────────────────────┐
                        │      Flask App       │
                        ├──────────────────────┤
                        │ Routes:              │
                        │ - /                  │
                        │ - /registro          │
                        │ - /login             │
                        │ - /produtos          │
                        │ - /carrinho          │
                        │ - /checkout          │
                        │ - /minha-conta       │
                        │ - /admin/*           │
                        └──────────────────────┘

RELACIONAMENTOS:
═══════════════

1. Cliente 1──* Endereco (Um cliente possui múltiplos endereços)
2. Cliente 1──* Pedido (Um cliente possui múltiplos pedidos)
3. Pedido 1──* ItemPedido (Um pedido possui múltiplos itens)
4. Produto 1──* ItemPedido (Um produto pode estar em múltiplos itens)
5. Categoria 1──* Produto (Uma categoria possui múltiplos produtos)
6. Produto 1──* ImagemProduto (Um produto possui múltiplas imagens)

HERANÇA:
════════

BaseRepository<T> é herdado por:
- ClienteRepository
- AdminRepository
- ProdutoRepository
- CategoriaRepository
- EnderecoRepository
- PedidoRepository

PRINCÍPIOS POO APLICADOS:
═════════════════════════

1. ENCAPSULAMENTO:
   - Atributos privados (prefixo -)
   - Métodos públicos (prefixo +)
   - Acesso controlado via métodos

2. HERANÇA:
   - BaseRepository como classe base genérica
   - Repositórios específicos herdam funcionalidades comuns

3. POLIMORFISMO:
   - Métodos sobrescritos nos repositórios
   - Interface comum para operações CRUD

4. ABSTRAÇÃO:
   - Camada de Repositório abstrai persistência
   - Controllers abstraem lógica de negócios
   - Models abstraem estrutura de dados
```
