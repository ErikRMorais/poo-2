# SCEE - Sistema de Comércio Eletrônico de Eletrônicos

Sistema completo de e-commerce desenvolvido em Python com Flask, seguindo rigorosamente os princípios de Programação Orientada a Objetos (POO) e o padrão arquitetural MVC (Model-View-Controller).

## Características Principais

- **Arquitetura MVC**: Separação clara entre Model, View e Controller
- **POO Rigorosa**: Encapsulamento, Herança e Polimorfismo aplicados
- **ORM SQLAlchemy**: Abstração completa do banco de dados
- **Camada de Repositório**: Isolamento da lógica de persistência
- **Segurança**: Senhas criptografadas com Argon2 (hash + salt)
- **Responsivo**: Interface adaptável para desktop e mobile

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
│   └── pedido_controller.py
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
├── requirements.txt        # Dependências Python
└── README.md
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

1. Execute a aplicação:

```bash
python app.py
```

2. Acesse no navegador:

```
http://localhost:5000
```

## Funcionalidades

### Para Clientes

- **Registro e Login**: Cadastro com validação de CPF, e-mail único e senha forte
- **Catálogo de Produtos**: Listagem paginada, busca e filtros por categoria/preço
- **Carrinho de Compras**: Adicionar, remover e atualizar quantidades
- **Checkout**: Processo em 3 etapas (Identificação, Endereço, Pagamento)
- **Minha Conta**: Gerenciar perfil, endereços e visualizar pedidos

### Para Administradores

- **Gerenciamento de Produtos**: CRUD completo com upload de imagens
- **Gerenciamento de Pedidos**: Visualizar e alterar status dos pedidos
- **Filtros e Paginação**: Ferramentas para facilitar a administração

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

## Princípios de POO Aplicados

### Encapsulamento

- Atributos privados nas classes
- Métodos públicos para acesso controlado
- Separação de responsabilidades

### Herança

- `BaseRepository`: Classe base genérica para repositórios
- Todos os repositórios herdam de `BaseRepository`

### Polimorfismo

- Métodos sobrescritos nos repositórios específicos
- Interface comum para operações CRUD

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

## Testes

Para executar testes unitários (quando implementados):

```bash
python -m pytest tests/
```

## Licença

Este projeto foi desenvolvido para fins educacionais.
