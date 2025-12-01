# 👤 Como Criar Usuário Administrador

## 🚀 Método 1: Script Interativo (RECOMENDADO)

### Passo a Passo:

```powershell
# 1. Ativar ambiente virtual (se não estiver ativo)
.\venv\Scripts\Activate.ps1

# 2. Executar script
python criar_admin.py
```

### Menu do Script:

```
🔧 GERENCIADOR DE ADMINISTRADORES
==================================================

1. Criar novo administrador
2. Listar administradores
3. Sair
==================================================
```

### Exemplo de Uso:

```
Escolha uma opção: 1

👤 Nome do administrador: João Silva
📧 E-mail: joao@scee.com
🔒 Senha: Senha@123

📋 CONFIRME OS DADOS:
   Nome: João Silva
   E-mail: joao@scee.com
   Senha: *********

✅ Confirmar criação? (s/n): s

✅ ADMINISTRADOR CRIADO COM SUCESSO!
👤 Nome: João Silva
📧 E-mail: joao@scee.com
🔑 ID: 2

🌐 Acesse: http://localhost:5000/login
📧 Login: joao@scee.com
🔒 Senha: Senha@123
```

---

## 🔧 Método 2: Python Direto

### Criar Admin via Terminal Python:

```powershell
# Abrir Python
python

# Executar comandos
>>> from database import Database
>>> from models.admin import Admin
>>> from argon2 import PasswordHasher
>>> 
>>> db = Database()
>>> session = db.get_session()
>>> ph = PasswordHasher()
>>> 
>>> # Criar admin
>>> admin = Admin(
...     nome='Maria Santos',
...     email='maria@scee.com',
...     senha_hash=ph.hash('Senha@456')
... )
>>> 
>>> session.add(admin)
>>> session.commit()
>>> print(f"Admin criado! ID: {admin.id}")
>>> session.close()
>>> exit()
```

---

## 📝 Método 3: Script Personalizado

Crie um arquivo `meu_admin.py`:

```python
from database import Database
from models.admin import Admin
from argon2 import PasswordHasher

# Configurar dados
NOME = "Carlos Admin"
EMAIL = "carlos@scee.com"
SENHA = "Admin@789"

# Criar
db = Database()
session = db.get_session()
ph = PasswordHasher()

admin = Admin(
    nome=NOME,
    email=EMAIL,
    senha_hash=ph.hash(SENHA)
)

session.add(admin)
session.commit()

print(f"✅ Admin criado: {EMAIL}")
session.close()
```

Execute:
```powershell
python meu_admin.py
```

---

## 👥 Listar Administradores

### Usando o Script:

```powershell
python criar_admin.py
# Escolha opção 2
```

### Via Python:

```python
from database import Database
from repositories.admin_repository import AdminRepository

db = Database()
session = db.get_session()
admin_repo = AdminRepository(session)

admins = admin_repo.get_all()
for admin in admins:
    print(f"{admin.nome} - {admin.email}")

session.close()
```

---

## 🔐 Admin Padrão do Sistema

O sistema já vem com um admin padrão:

```
📧 E-mail: admin@scee.com
🔒 Senha: Admin@123
```

**Acesse:** http://localhost:5000/login

---

## ✅ Validações

O sistema valida automaticamente:

- ✅ **Nome:** Obrigatório
- ✅ **E-mail:** Formato válido e único
- ✅ **Senha:** Mínimo 6 caracteres
- ✅ **Hash:** Senha criptografada com Argon2

---

## 🔒 Segurança

### Boas Práticas:

1. ✅ Use senhas fortes (mínimo 8 caracteres)
2. ✅ Combine letras, números e símbolos
3. ✅ Não compartilhe credenciais
4. ✅ Troque senhas periodicamente

### Exemplos de Senhas Fortes:

```
✅ Admin@2024
✅ Segura#123
✅ Forte$456
❌ 123456 (fraca)
❌ admin (fraca)
```

---

## 🐛 Solução de Problemas

### Erro: "E-mail já cadastrado"

**Causa:** E-mail já existe no banco

**Solução:** Use outro e-mail ou delete o admin existente

### Erro: "Senha muito curta"

**Causa:** Senha tem menos de 6 caracteres

**Solução:** Use senha com 6+ caracteres

### Erro: "E-mail inválido"

**Causa:** Formato de e-mail incorreto

**Solução:** Use formato válido (exemplo@dominio.com)

---

## 🔄 Alterar Senha de Admin Existente

### Via Script Python:

```python
from database import Database
from repositories.admin_repository import AdminRepository
from argon2 import PasswordHasher

db = Database()
session = db.get_session()
admin_repo = AdminRepository(session)
ph = PasswordHasher()

# Buscar admin por e-mail
admin = admin_repo.get_by_email('admin@scee.com')

if admin:
    # Alterar senha
    nova_senha = 'NovaSenha@123'
    admin.senha_hash = ph.hash(nova_senha)
    session.commit()
    print(f"✅ Senha alterada para: {nova_senha}")
else:
    print("❌ Admin não encontrado")

session.close()
```

---

## 🗑️ Deletar Admin

### Via Python:

```python
from database import Database
from repositories.admin_repository import AdminRepository

db = Database()
session = db.get_session()
admin_repo = AdminRepository(session)

# Buscar admin
admin = admin_repo.get_by_email('admin@deletar.com')

if admin:
    admin_repo.delete(admin.id)
    print(f"✅ Admin deletado: {admin.email}")
else:
    print("❌ Admin não encontrado")

session.close()
```

---

## 📊 Verificar Admins no Banco

### Via SQLite:

```powershell
# Abrir banco
sqlite3 scee_loja.db

# Listar admins
SELECT id, nome, email, data_cadastro FROM admins;

# Sair
.quit
```

---

## 🎯 Resumo Rápido

### Criar Admin (Mais Fácil):

```powershell
python criar_admin.py
```

### Listar Admins:

```powershell
python criar_admin.py
# Opção 2
```

### Login Admin:

```
URL: http://localhost:5000/login
Tipo: Administrador
E-mail: admin@scee.com
Senha: Admin@123
```

---

## 📚 Arquivos Relacionados

- **`criar_admin.py`** - Script para criar admins
- **`models/admin.py`** - Modelo Admin
- **`repositories/admin_repository.py`** - Repositório
- **`controllers/auth_controller.py`** - Autenticação

---

## ✅ Checklist

Após criar admin:

- [ ] Admin criado com sucesso
- [ ] E-mail único e válido
- [ ] Senha forte (6+ caracteres)
- [ ] Testado login no sistema
- [ ] Acesso ao dashboard admin

---

**Dica:** Use o script `criar_admin.py` - é o método mais fácil e seguro! 🚀

```powershell
python criar_admin.py
```
