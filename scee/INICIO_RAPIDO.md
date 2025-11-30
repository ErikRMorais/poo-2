# Início Rápido - SCEE

## 🚀 Execute o Sistema em 5 Minutos

---

## Passo 1: Abrir PowerShell

Pressione `Win + X` e selecione "Windows PowerShell"

---

## Passo 2: Navegar até a Pasta

```powershell
cd "C:\Users\MORAIS\Documents\poo 2\scee"
```

---

## Passo 3: Criar Ambiente Virtual

```powershell
python -m venv venv
```

---

## Passo 4: Ativar Ambiente Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

**Se houver erro**, execute primeiro:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Passo 5: Instalar Dependências

```powershell
pip install -r requirements.txt
```

Aguarde a instalação (1-2 minutos)

---

## Passo 6: Inicializar Banco de Dados

```powershell
python init_db.py
```

Você verá:
```
Banco de dados inicializado com sucesso!

Credenciais do Admin:
E-mail: admin@scee.com
Senha: Admin@123
```

---

## Passo 7: Executar Aplicação

```powershell
python app.py
```

Você verá:
```
* Running on http://0.0.0.0:5000
```

---

## Passo 8: Acessar no Navegador

Abra seu navegador e acesse:

```
http://localhost:5000
```

---

## ✅ Pronto!

O sistema está rodando. Agora você pode:

### Como Cliente
1. Clique em **"Registrar"**
2. Crie uma conta
3. Navegue pelos produtos
4. Adicione ao carrinho
5. Finalize a compra

### Como Admin
1. Clique em **"Login"**
2. Selecione tipo **"Administrador"**
3. Use: `admin@scee.com` / `Admin@123`
4. Gerencie produtos e pedidos

---

## 🛑 Para Parar

No terminal, pressione: `Ctrl + C`

---

## 📚 Próximos Passos

- Leia o **README.md** para entender o sistema
- Consulte o **GUIA_INSTALACAO.md** para detalhes
- Veja os **diagramas UML** em `docs/`

---

## ⚡ Comandos Úteis

**Ativar ambiente:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Desativar ambiente:**
```powershell
deactivate
```

**Reiniciar banco de dados:**
```powershell
# Deletar arquivo
Remove-Item scee_loja.db

# Recriar
python init_db.py
```

**Executar aplicação:**
```powershell
python app.py
```

---

## 🎯 Teste Rápido

### Criar um Cliente
1. Acesse http://localhost:5000/registro
2. Preencha:
   - Nome: `Teste Silva`
   - E-mail: `teste@exemplo.com`
   - CPF: `12345678909`
   - Senha: `Teste@123`
3. Clique em "Registrar"

### Criar um Produto (Admin)
1. Faça login como admin
2. Vá em "Admin" → "Produtos" → "Novo Produto"
3. Preencha os dados
4. Salve

### Fazer uma Compra
1. Faça logout do admin
2. Faça login como cliente
3. Adicione um endereço em "Minha Conta"
4. Navegue até "Produtos"
5. Adicione ao carrinho
6. Finalize a compra

---

## 🆘 Problemas?

Consulte a seção **"Solução de Problemas"** no `GUIA_INSTALACAO.md`

---

**Boa sorte! 🎉**
