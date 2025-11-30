# Índice de Documentação - SCEE

## 📚 Documentação Completa do Projeto

---

## 1. Documentos Principais

### 📖 README.md
**Descrição:** Documentação principal do projeto  
**Conteúdo:**
- Visão geral do sistema
- Características principais
- Estrutura do projeto
- Requisitos e instalação
- Funcionalidades
- Banco de dados
- Segurança
- Princípios POO e MVC

**Localização:** `/README.md`

---

### 🚀 GUIA_INSTALACAO.md
**Descrição:** Guia passo a passo para instalação e execução  
**Conteúdo:**
- Pré-requisitos
- 8 passos de instalação
- Como executar
- Funcionalidades disponíveis
- Testes do sistema
- Solução de problemas

**Localização:** `/GUIA_INSTALACAO.md`

---

### 📋 RESUMO_PROJETO.md
**Descrição:** Resumo executivo do projeto  
**Conteúdo:**
- Entregáveis completos
- Requisitos implementados
- Arquitetura MVC detalhada
- Princípios POO aplicados
- Estatísticas do projeto
- Diferenciais
- Conformidade com requisitos

**Localização:** `/RESUMO_PROJETO.md`

---

### ✅ CHECKLIST_REQUISITOS.md
**Descrição:** Lista de verificação de todos os requisitos  
**Conteúdo:**
- Diretrizes de implementação
- Restrições técnicas
- Requisitos funcionais (RF01-RF08)
- Requisitos não funcionais (RNF)
- Entregáveis
- Princípios POO
- Status geral

**Localização:** `/CHECKLIST_REQUISITOS.md`

---

## 2. Diagramas UML

### 🏗️ Diagrama de Classes
**Descrição:** Diagrama UML completo de todas as classes  
**Conteúdo:**
- Camada Model (9 entidades)
- Camada Repository (7 repositórios)
- Camada Controller (5 controllers)
- Camada View (Flask App)
- Relacionamentos
- Herança
- Princípios POO aplicados

**Localização:** `/docs/diagrama_classes.md`

**Elementos:**
- Cliente, Admin, Endereco
- Categoria, Produto, ImagemProduto
- Pedido, ItemPedido
- BaseRepository e repositórios específicos
- Controllers (Auth, Cliente, Produto, Carrinho, Pedido)

---

### 📊 Diagrama de Casos de Uso
**Descrição:** Diagrama UML de casos de uso do sistema  
**Conteúdo:**
- 20 casos de uso detalhados
- 2 atores (Cliente e Admin)
- Relacionamentos <<include>> e <<extend>>
- Descrições completas de cada caso de uso
- Pré-condições e pós-condições
- Fluxos principais

**Localização:** `/docs/diagrama_casos_uso.md`

**Módulos:**
- Autenticação e Contas (UC01-UC02)
- Catálogo e Produtos (UC03-UC05)
- Carrinho (UC06-UC08)
- Checkout e Pedidos (UC09, UC14)
- Perfil (UC10-UC13)
- Admin - Produtos (UC15-UC17)
- Admin - Pedidos (UC18-UC20)

---

## 3. Banco de Dados

### 🗄️ Esquema do Banco de Dados
**Descrição:** Documentação completa do banco de dados SQLite  
**Conteúdo:**
- 8 tabelas detalhadas
- Campos e tipos de dados
- Relacionamentos (1:N, N:1)
- Chaves primárias e estrangeiras
- Constraints (CHECK, UNIQUE)
- Índices para otimização
- Diagrama ER
- Integridade referencial
- Transações atômicas
- Segurança (Argon2)

**Localização:** `/docs/esquema_banco_dados.md`

**Tabelas:**
1. clientes
2. admins
3. enderecos
4. categorias
5. produtos
6. imagens_produto
7. pedidos
8. itens_pedido

---

## 4. Código Fonte

### 🔧 Models (Entidades ORM)
**Localização:** `/models/`

**Arquivos:**
- `base.py` - Classe base declarativa
- `cliente.py` - Entidade Cliente
- `admin.py` - Entidade Admin
- `endereco.py` - Entidade Endereco
- `categoria.py` - Entidade Categoria
- `produto.py` - Entidade Produto
- `imagem_produto.py` - Entidade ImagemProduto
- `pedido.py` - Entidade Pedido
- `item_pedido.py` - Entidade ItemPedido

---

### 💾 Repositories (Persistência)
**Localização:** `/repositories/`

**Arquivos:**
- `base_repository.py` - Repositório genérico base
- `cliente_repository.py` - Operações de Cliente
- `admin_repository.py` - Operações de Admin
- `produto_repository.py` - Operações de Produto
- `categoria_repository.py` - Operações de Categoria
- `endereco_repository.py` - Operações de Endereco
- `pedido_repository.py` - Operações de Pedido

---

### 🎮 Controllers (Lógica de Negócios)
**Localização:** `/controllers/`

**Arquivos:**
- `auth_controller.py` - Autenticação e validações
- `cliente_controller.py` - Gerenciamento de perfil
- `produto_controller.py` - Gerenciamento de produtos
- `carrinho_controller.py` - Lógica do carrinho
- `pedido_controller.py` - Criação e gestão de pedidos

---

### 🌐 Views (Templates)
**Localização:** `/templates/`

**Templates Públicos:**
- `base.html` - Template base
- `index.html` - Página inicial
- `registro.html` - Registro de cliente
- `login.html` - Login
- `produtos.html` - Listagem de produtos
- `produto_detalhe.html` - Detalhes do produto
- `carrinho.html` - Carrinho de compras
- `checkout.html` - Finalização de compra
- `minha_conta.html` - Conta do cliente

**Templates Admin:**
- `admin/dashboard.html` - Dashboard administrativo
- `admin/produtos.html` - Gerenciamento de produtos
- `admin/produto_form.html` - Formulário de produto
- `admin/pedidos.html` - Gerenciamento de pedidos

---

### 🎨 Estilos
**Localização:** `/static/css/`

**Arquivo:**
- `style.css` - Estilos responsivos (~600 linhas)

**Características:**
- Design moderno
- Mobile-first
- Media queries
- Variáveis CSS
- Grid e Flexbox

---

## 5. Configuração e Scripts

### ⚙️ Arquivos de Configuração

**database.py**
- Configuração do SQLAlchemy
- Gerenciamento de sessões
- Criação de tabelas

**app.py**
- Aplicação Flask principal
- Rotas (View/Controller)
- Integração MVC

**init_db.py**
- Script de inicialização
- Criação de categorias padrão
- Criação de admin padrão

**requirements.txt**
- Dependências Python
- Versões específicas

**.gitignore**
- Arquivos a ignorar no Git

---

## 6. Como Usar Esta Documentação

### Para Desenvolvedores

1. **Começar:** Leia `README.md`
2. **Instalar:** Siga `GUIA_INSTALACAO.md`
3. **Entender Arquitetura:** Consulte `diagrama_classes.md`
4. **Entender Funcionalidades:** Consulte `diagrama_casos_uso.md`
5. **Banco de Dados:** Consulte `esquema_banco_dados.md`

### Para Avaliadores

1. **Visão Geral:** Leia `RESUMO_PROJETO.md`
2. **Verificar Requisitos:** Consulte `CHECKLIST_REQUISITOS.md`
3. **Diagramas UML:** Veja `diagrama_classes.md` e `diagrama_casos_uso.md`
4. **Testar:** Siga `GUIA_INSTALACAO.md`

### Para Usuários Finais

1. **Instalação:** Siga `GUIA_INSTALACAO.md`
2. **Uso:** Seção "Funcionalidades Disponíveis" no guia
3. **Problemas:** Seção "Solução de Problemas" no guia

---

## 7. Estrutura de Navegação

```
scee/
│
├── 📄 README.md                    ← Documentação principal
├── 📄 GUIA_INSTALACAO.md          ← Como instalar e executar
├── 📄 RESUMO_PROJETO.md           ← Resumo executivo
├── 📄 CHECKLIST_REQUISITOS.md     ← Verificação de requisitos
│
├── 📁 docs/
│   ├── 📄 INDEX.md                ← Este arquivo
│   ├── 📄 diagrama_classes.md     ← UML de Classes
│   ├── 📄 diagrama_casos_uso.md   ← UML de Casos de Uso
│   └── 📄 esquema_banco_dados.md  ← Esquema do BD
│
├── 📁 models/                      ← Entidades ORM
├── 📁 repositories/                ← Camada de Persistência
├── 📁 controllers/                 ← Lógica de Negócios
├── 📁 templates/                   ← Views HTML
├── 📁 static/                      ← CSS e Uploads
│
├── 🐍 app.py                       ← Aplicação Flask
├── 🐍 database.py                  ← Configuração BD
├── 🐍 init_db.py                   ← Inicialização
└── 📄 requirements.txt             ← Dependências
```

---

## 8. Referências Rápidas

### Comandos Úteis

**Instalar:**
```powershell
pip install -r requirements.txt
```

**Inicializar BD:**
```powershell
python init_db.py
```

**Executar:**
```powershell
python app.py
```

**Acessar:**
```
http://localhost:5000
```

### Credenciais Padrão

**Admin:**
- E-mail: `admin@scee.com`
- Senha: `Admin@123`

### Estrutura MVC

- **Model:** `models/`
- **View:** `templates/` + `static/`
- **Controller:** `controllers/` + `app.py`
- **Repository:** `repositories/`

---

## 9. Glossário

**MVC:** Model-View-Controller (padrão arquitetural)  
**ORM:** Object-Relational Mapping (mapeamento objeto-relacional)  
**POO:** Programação Orientada a Objetos  
**CRUD:** Create, Read, Update, Delete  
**UML:** Unified Modeling Language  
**SQLite:** Sistema de banco de dados relacional  
**Flask:** Framework web Python  
**SQLAlchemy:** ORM Python  
**Argon2:** Algoritmo de hash de senha  
**Repository Pattern:** Padrão de projeto para abstração de persistência  

---

## 10. Contato e Suporte

Para dúvidas sobre a documentação:
1. Consulte o arquivo específico listado acima
2. Verifique os comentários no código (docstrings)
3. Revise os diagramas UML

---

**Última Atualização:** 30/11/2024  
**Versão da Documentação:** 1.0  
**Status:** Completa
