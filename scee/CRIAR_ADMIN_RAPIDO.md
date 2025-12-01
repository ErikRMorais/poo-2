# 🚀 CRIAR ADMIN - GUIA RÁPIDO

## ⚠️ IMPORTANTE: Use o Diretório Correto!

**SEMPRE execute dentro da pasta `scee`:**

```powershell
# 1. Ir para pasta scee
cd "C:\Users\MORAIS\Documents\poo 2\scee"

# 2. Executar script
python criar_admin.py
```

---

## 📝 Passo a Passo

### 1. Abrir PowerShell na pasta correta:

```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"
```

### 2. Executar o script:

```powershell
python criar_admin.py
```

### 3. Escolher opção:

```
1. Criar novo administrador  ← Escolha esta
2. Listar administradores
3. Sair
```

### 4. Preencher dados:

```
👤 Nome do administrador: João Silva
📧 E-mail: joao@scee.com
🔒 Senha: Senha@123
```

### 5. Confirmar:

```
✅ Confirmar criação? (s/n): s
```

### 6. Pronto! ✅

```
✅ ADMINISTRADOR CRIADO COM SUCESSO!
👤 Nome: João Silva
📧 E-mail: joao@scee.com
```

---

## 🔐 Fazer Login

Depois de criar, acesse:

```
http://localhost:5000/login
```

Selecione "Administrador" e use:
- **E-mail:** joao@scee.com
- **Senha:** Senha@123

---

## 👥 Ver Admins Existentes

```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"
python criar_admin.py
# Escolha opção 2
```

---

## ❌ ERRO COMUM

**Se aparecer "ModuleNotFoundError":**

❌ **ERRADO:**
```powershell
cd "C:\Users\MORAIS\Documents\poo 2"  # Pasta errada!
python scee/criar_admin.py
```

✅ **CORRETO:**
```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"  # Pasta certa!
python criar_admin.py
```

---

## 🎯 Comandos Prontos (Copie e Cole)

### Criar Admin:
```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"; python criar_admin.py
```

### Listar Admins:
```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"; python criar_admin.py
```

---

## 📋 Exemplo Completo

```powershell
# Ir para pasta
PS C:\> cd "C:\Users\MORAIS\Documents\poo 2\scee"

# Executar
PS C:\Users\MORAIS\Documents\poo 2\scee> python criar_admin.py

# Menu aparece
🔧 GERENCIADOR DE ADMINISTRADORES
1. Criar novo administrador
2. Listar administradores
3. Sair

Escolha uma opção: 1

# Preencher
👤 Nome do administrador: Maria Santos
📧 E-mail: maria@scee.com
🔒 Senha: Admin@456

# Confirmar
✅ Confirmar criação? (s/n): s

# Sucesso!
✅ ADMINISTRADOR CRIADO COM SUCESSO!
```

---

## ✅ Checklist

- [ ] Estou na pasta `scee`
- [ ] Executei `python criar_admin.py`
- [ ] Escolhi opção 1
- [ ] Preenchi nome, e-mail e senha
- [ ] Confirmei com 's'
- [ ] Admin criado com sucesso

---

**Dica:** Sempre execute dentro da pasta `scee`! 🎯
