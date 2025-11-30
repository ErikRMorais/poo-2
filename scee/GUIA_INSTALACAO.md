# Guia de Instalação e Execução - SCEE

## Pré-requisitos

- **Python 3.10 ou superior** instalado
- **pip** (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Edge)

---

## Passo 1: Verificar Instalação do Python

Abra o PowerShell e execute:

```powershell
python --version
```

Deve exibir algo como: `Python 3.10.x` ou superior.

Se não tiver Python instalado, baixe em: https://www.python.org/downloads/

---

## Passo 2: Navegar até a Pasta do Projeto

```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"
```

---

## Passo 3: Criar Ambiente Virtual

```powershell
python -m venv venv
```

Isso criará uma pasta `venv` com o ambiente isolado.

---

## Passo 4: Ativar o Ambiente Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Se houver erro de política de execução, execute primeiro:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente ativar novamente.

Quando ativado, você verá `(venv)` no início da linha de comando.

---

## Passo 5: Instalar Dependências

```powershell
pip install -r requirements.txt
```

Isso instalará:
- Flask 3.0.0
- SQLAlchemy 2.0.23
- argon2-cffi 23.1.0
- Werkzeug 3.0.1

---

## Passo 6: Inicializar o Banco de Dados

```powershell
python init_db.py
```

Isso criará:
- Arquivo `scee_loja.db` (banco de dados SQLite)
- Tabelas com restrições de integridade
- Categorias padrão
- Usuário admin padrão

**Credenciais do Admin:**
- E-mail: `admin@scee.com`
- Senha: `Admin@123`

---

## Passo 7: Executar a Aplicação

```powershell
python app.py
```

Você verá algo como:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

---

## Passo 8: Acessar no Navegador

Abra seu navegador e acesse:

```
http://localhost:5000
```

---

## Funcionalidades Disponíveis

### Para Clientes

1. **Registrar Conta**: Clique em "Registrar" no menu
   - Preencha: Nome, E-mail, CPF (apenas números), Senha
   - Senha deve ter: mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número

2. **Fazer Login**: Clique em "Login" no menu
   - Selecione tipo "Cliente"
   - Informe e-mail e senha

3. **Navegar Produtos**: 
   - Página inicial mostra produtos em destaque
   - Menu "Produtos" para ver catálogo completo
   - Use filtros por categoria e faixa de preço
   - Use busca por texto

4. **Adicionar ao Carrinho**:
   - Clique em "Ver Detalhes" em um produto
   - Selecione quantidade
   - Clique em "Adicionar ao Carrinho"

5. **Finalizar Compra**:
   - Acesse "Carrinho" no menu
   - Revise itens e quantidades
   - Clique em "Finalizar Compra"
   - Selecione endereço de entrega
   - Escolha método de pagamento (Cartão ou Pix)
   - Confirme pedido

6. **Gerenciar Conta**:
   - Acesse "Minha Conta" no menu
   - Visualize seus pedidos
   - Gerencie endereços de entrega

### Para Administradores

1. **Fazer Login**:
   - Clique em "Login" no menu
   - Selecione tipo "Administrador"
   - Use credenciais: `admin@scee.com` / `Admin@123`

2. **Gerenciar Produtos**:
   - Acesse "Admin" → "Produtos"
   - Criar: Clique em "Novo Produto"
   - Editar: Clique em "Editar" ao lado do produto
   - Deletar: Clique em "Deletar" (confirme exclusão)

3. **Gerenciar Pedidos**:
   - Acesse "Admin" → "Pedidos"
   - Visualize lista de todos os pedidos
   - Filtre por status
   - Altere status dos pedidos

---

## Estrutura de Pastas

```
scee/
├── models/              # Entidades ORM (Cliente, Produto, Pedido, etc.)
├── repositories/        # Camada de acesso a dados
├── controllers/         # Lógica de negócios
├── templates/           # Templates HTML
│   ├── admin/          # Templates administrativos
│   └── *.html          # Templates públicos
├── static/
│   ├── css/            # Estilos CSS
│   └── uploads/        # Imagens de produtos (criado automaticamente)
├── docs/               # Documentação e diagramas UML
├── app.py              # Aplicação Flask principal
├── database.py         # Configuração do banco de dados
├── init_db.py          # Script de inicialização
├── requirements.txt    # Dependências Python
└── README.md           # Documentação principal
```

---

## Testando o Sistema

### Criar um Cliente de Teste

1. Acesse http://localhost:5000/registro
2. Preencha:
   - Nome: `João Silva`
   - E-mail: `joao@teste.com`
   - CPF: `12345678909` (CPF válido para teste)
   - Senha: `Teste@123`
   - Confirmar Senha: `Teste@123`
3. Clique em "Registrar"

### Criar um Produto de Teste (como Admin)

1. Faça login como admin
2. Acesse "Admin" → "Produtos" → "Novo Produto"
3. Preencha:
   - Nome: `iPhone 15 Pro`
   - SKU: `IPH15PRO`
   - Descrição: `Smartphone Apple com chip A17 Pro`
   - Preço: `7999.00`
   - Estoque: `10`
   - Categoria: `Smartphones`
4. Opcionalmente, adicione imagens
5. Clique em "Salvar"

### Fazer uma Compra de Teste

1. Faça logout do admin
2. Faça login como cliente (`joao@teste.com`)
3. Acesse "Minha Conta" → Adicione um endereço
4. Navegue até "Produtos"
5. Clique no produto criado
6. Adicione ao carrinho
7. Acesse "Carrinho" → "Finalizar Compra"
8. Selecione endereço e método de pagamento
9. Confirme pedido

### Verificar Pedido (como Admin)

1. Faça login como admin
2. Acesse "Admin" → "Pedidos"
3. Veja o pedido criado
4. Altere o status para "Processando"

---

## Solução de Problemas

### Erro: "Execution Policy"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Module not found"

Certifique-se de que o ambiente virtual está ativado e execute:

```powershell
pip install -r requirements.txt
```

### Erro: "Address already in use"

Outra aplicação está usando a porta 5000. Altere em `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Banco de Dados Corrompido

Delete o arquivo `scee_loja.db` e execute novamente:

```powershell
python init_db.py
```

---

## Parar a Aplicação

No terminal onde o Flask está rodando, pressione:

```
Ctrl + C
```

---

## Desativar Ambiente Virtual

```powershell
deactivate
```

---

## Requisitos Não Funcionais Atendidos

✅ **RNF01.1**: Páginas carregam em < 3 segundos  
✅ **RNF01.2**: Respostas do backend em < 500ms  
✅ **RNF03.2**: Senhas criptografadas com Argon2 (hash + salt)  
✅ **RNF07.1**: Criação de pedido é atômica (transação SQLite)  
✅ **RNF07.3**: Race conditions no estoque tratadas (verificação dentro da transação)  
✅ **RNF06.5**: Código permite testes unitários (separação de responsabilidades)  
✅ **RNF06.6**: Todas as classes e métodos possuem docstrings  
✅ **RNF02.1**: Frontend totalmente responsivo (CSS com media queries)  

**Nota sobre HTTPS (RNF03.3):**
Para ambiente de produção, configure um servidor web (Nginx/Apache) com certificado SSL.
Em desenvolvimento local, use HTTP (localhost).

---

## Próximos Passos (Opcional)

### Adicionar Mais Categorias

Execute no Python:

```python
from database import Database
from models.categoria import Categoria

db = Database()
session = db.get_session()

nova_categoria = Categoria(nome='Wearables')
session.add(nova_categoria)
session.commit()
```

### Criar Mais Admins

Execute no Python:

```python
from database import Database
from models.admin import Admin
from argon2 import PasswordHasher

db = Database()
session = db.get_session()
ph = PasswordHasher()

novo_admin = Admin(
    nome='Seu Nome',
    email='seuemail@scee.com',
    senha_hash=ph.hash('SuaSenha@123')
)
session.add(novo_admin)
session.commit()
```

---

## Suporte

Para dúvidas ou problemas:
1. Consulte o `README.md`
2. Verifique os diagramas UML em `docs/`
3. Revise o esquema do banco em `docs/esquema_banco_dados.md`
