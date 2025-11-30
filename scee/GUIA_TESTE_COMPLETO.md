# Guia de Teste Completo - Sistema SCEE

## 🚀 Iniciando o Sistema

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar aplicação
python app.py
```

**Acesse:** http://localhost:5000

---

## 👤 PARTE 1: TESTES COMO CLIENTE

### Teste 1.1: Registro de Novo Cliente

1. Acesse http://localhost:5000/registro
2. Preencha:
   - Nome: `João Silva`
   - E-mail: `joao@teste.com`
   - CPF: `12345678909`
   - Senha: `Senha@123`
   - Confirmar Senha: `Senha@123`
3. Clique em "Registrar"
4. ✅ **Resultado Esperado:** Redirecionamento para "Minha Conta"

---

### Teste 1.2: Editar Perfil

1. Em "Minha Conta", clique em "Editar Perfil"
2. Altere:
   - Nome: `João Silva Santos`
   - E-mail: `joao.santos@teste.com`
3. Clique em "Salvar Alterações"
4. ✅ **Resultado Esperado:** Mensagem de sucesso e dados atualizados

---

### Teste 1.3: Alterar Senha

1. Em "Minha Conta", clique em "Alterar Senha"
2. Preencha:
   - Senha Atual: `Senha@123`
   - Nova Senha: `NovaSenha@456`
   - Confirmar: `NovaSenha@456`
3. Clique em "Alterar Senha"
4. Faça logout e login com a nova senha
5. ✅ **Resultado Esperado:** Login bem-sucedido com nova senha

---

### Teste 1.4: Adicionar Endereço

1. Em "Minha Conta", clique em "+ Adicionar Endereço"
2. Preencha:
   - CEP: `01310-100`
   - Rua: `Avenida Paulista`
   - Número: `1000`
   - Complemento: `Apto 101`
   - Bairro: `Bela Vista`
   - Cidade: `São Paulo`
   - Estado: `SP`
3. Clique em "Salvar Endereço"
4. ✅ **Resultado Esperado:** Endereço aparece em "Meus Endereços"

---

### Teste 1.5: Editar Endereço

1. Clique em "Editar" no endereço criado
2. Altere o número para `1500`
3. Clique em "Salvar Endereço"
4. ✅ **Resultado Esperado:** Endereço atualizado

---

### Teste 1.6: Adicionar Segundo Endereço

1. Adicione outro endereço:
   - CEP: `20040-020`
   - Rua: `Avenida Rio Branco`
   - Número: `156`
   - Bairro: `Centro`
   - Cidade: `Rio de Janeiro`
   - Estado: `RJ`
2. ✅ **Resultado Esperado:** Dois endereços listados

---

### Teste 1.7: Buscar Produtos

1. Acesse "Produtos"
2. Busque por "iPhone"
3. ✅ **Resultado Esperado:** Produtos filtrados, imagens visíveis

---

### Teste 1.8: Filtrar por Categoria

1. Selecione categoria "Smartphones"
2. Clique em "Filtrar"
3. ✅ **Resultado Esperado:** Apenas smartphones exibidos

---

### Teste 1.9: Filtrar por Preço

1. Preencha:
   - Preço mín: `3000`
   - Preço máx: `6000`
2. Clique em "Filtrar"
3. ✅ **Resultado Esperado:** Produtos na faixa de preço

---

### Teste 1.10: Ver Detalhes do Produto

1. Clique em "Ver Detalhes" de um produto
2. ✅ **Resultado Esperado:** 
   - Imagens visíveis (não quebradas)
   - Descrição completa
   - Preço e estoque
   - Botão "Adicionar ao Carrinho"

---

### Teste 1.11: Adicionar ao Carrinho

1. Selecione quantidade: `2`
2. Clique em "Adicionar ao Carrinho"
3. ✅ **Resultado Esperado:** Redirecionamento para carrinho

---

### Teste 1.12: Gerenciar Carrinho

1. No carrinho, altere quantidade para `3`
2. Adicione outro produto
3. Remova um produto
4. ✅ **Resultado Esperado:** 
   - Quantidade atualizada
   - Total recalculado
   - Produto removido

---

### Teste 1.13: Finalizar Compra (Checkout)

1. Clique em "Finalizar Compra"
2. Selecione um endereço de entrega
3. Selecione método de pagamento: "Cartão"
4. Clique em "Confirmar Pedido"
5. ✅ **Resultado Esperado:** 
   - Pedido criado com sucesso
   - Carrinho limpo
   - Pedido aparece em "Meus Pedidos"

---

### Teste 1.14: Verificar Pedido

1. Em "Minha Conta", veja "Meus Pedidos"
2. ✅ **Resultado Esperado:** 
   - Pedido listado
   - Status: "Pendente"
   - Total correto

---

### Teste 1.15: Deletar Endereço

1. Clique em "Excluir" em um endereço
2. Confirme a exclusão
3. ✅ **Resultado Esperado:** Endereço removido

---

## 🔐 PARTE 2: TESTES COMO ADMINISTRADOR

### Teste 2.1: Login Admin

1. Faça logout
2. Acesse http://localhost:5000/login
3. Selecione "Administrador"
4. Login:
   - E-mail: `admin@scee.com`
   - Senha: `Admin@123`
5. ✅ **Resultado Esperado:** Redirecionamento para Dashboard Admin

---

### Teste 2.2: Dashboard Admin

1. Verifique os 4 cards:
   - Produtos
   - Categorias
   - Pedidos
   - Clientes
2. ✅ **Resultado Esperado:** Todos os cards visíveis e clicáveis

---

### Teste 2.3: Criar Categoria

1. Clique em "Categorias"
2. Clique em "+ Nova Categoria"
3. Nome: `Wearables`
4. Clique em "Salvar"
5. ✅ **Resultado Esperado:** Categoria criada e listada

---

### Teste 2.4: Editar Categoria

1. Clique em "Editar" na categoria criada
2. Altere nome para `Dispositivos Vestíveis`
3. Clique em "Salvar"
4. ✅ **Resultado Esperado:** Categoria atualizada

---

### Teste 2.5: Tentar Criar Categoria Duplicada

1. Tente criar categoria "Smartphones" (já existe)
2. ✅ **Resultado Esperado:** Mensagem de erro "Categoria já existe"

---

### Teste 2.6: Deletar Categoria

1. Clique em "Deletar" na categoria "Dispositivos Vestíveis"
2. Confirme a exclusão
3. ✅ **Resultado Esperado:** Categoria removida

---

### Teste 2.7: Criar Produto com Imagens

1. Acesse "Produtos" → "+ Novo Produto"
2. Preencha:
   - Nome: `Apple Watch Series 9`
   - SKU: `APPLEWATCH9`
   - Descrição: `Smartwatch com GPS, tela Retina Always-On`
   - Preço: `3999.00`
   - Estoque: `20`
   - Categoria: `Smartwatches`
3. Faça upload de 2 imagens (JPG ou PNG)
4. Clique em "Salvar"
5. ✅ **Resultado Esperado:** Produto criado com imagens

---

### Teste 2.8: Verificar Imagens do Produto

1. Acesse a loja (não-admin)
2. Busque pelo produto criado
3. Clique em "Ver Detalhes"
4. ✅ **Resultado Esperado:** 
   - Imagens visíveis (NÃO quebradas)
   - Ambas as imagens aparecem

---

### Teste 2.9: Editar Produto

1. Como admin, edite o produto criado
2. Altere:
   - Preço: `3799.00`
   - Estoque: `25`
3. Clique em "Salvar"
4. ✅ **Resultado Esperado:** Produto atualizado

---

### Teste 2.10: Visualizar Pedidos

1. Acesse "Pedidos"
2. ✅ **Resultado Esperado:** 
   - Pedido do cliente listado
   - Dados do cliente visíveis
   - Status "Pendente"

---

### Teste 2.11: Atualizar Status do Pedido

1. Altere status para "Processando"
2. Clique em "Atualizar"
3. ✅ **Resultado Esperado:** Status atualizado

---

### Teste 2.12: Filtrar Pedidos por Status

1. Selecione status "Processando"
2. ✅ **Resultado Esperado:** Apenas pedidos processando

---

### Teste 2.13: Visualizar Clientes

1. Acesse "Clientes"
2. ✅ **Resultado Esperado:** 
   - Lista de clientes cadastrados
   - Dados: Nome, E-mail, CPF, Data Cadastro

---

### Teste 2.14: Ver Detalhes do Cliente

1. Clique em "Ver Detalhes" de um cliente
2. ✅ **Resultado Esperado:** 
   - **Dados Pessoais:** Nome, E-mail, CPF, Data Cadastro
   - **Endereços:** Lista de endereços do cliente
   - **Histórico de Pedidos:** Pedidos realizados
   - **Total Gasto:** Soma de todos os pedidos

---

### Teste 2.15: Deletar Produto

1. Acesse "Produtos"
2. Clique em "Deletar" em um produto
3. Confirme a exclusão
4. ✅ **Resultado Esperado:** Produto removido

---

## 🔍 PARTE 3: TESTES DE VALIDAÇÃO

### Teste 3.1: Validação de E-mail Duplicado

1. Tente registrar com e-mail já existente
2. ✅ **Resultado Esperado:** Erro "E-mail já cadastrado"

---

### Teste 3.2: Validação de CPF Duplicado

1. Tente registrar com CPF já existente
2. ✅ **Resultado Esperado:** Erro "CPF já cadastrado"

---

### Teste 3.3: Validação de Senha Fraca

1. Tente registrar com senha `123`
2. ✅ **Resultado Esperado:** Erro de validação

---

### Teste 3.4: Validação de Senhas Diferentes

1. Senha: `Senha@123`
2. Confirmar: `Senha@456`
3. ✅ **Resultado Esperado:** Erro "Senhas não coincidem"

---

### Teste 3.5: Validação de SKU Duplicado

1. Como admin, tente criar produto com SKU existente
2. ✅ **Resultado Esperado:** Erro "SKU já cadastrado"

---

### Teste 3.6: Validação de Preço Negativo

1. Tente criar produto com preço `-100`
2. ✅ **Resultado Esperado:** Erro "Preço deve ser maior que zero"

---

### Teste 3.7: Validação de Estoque Negativo

1. Tente criar produto com estoque `-5`
2. ✅ **Resultado Esperado:** Erro "Estoque não pode ser negativo"

---

### Teste 3.8: Validação de Estoque Insuficiente

1. Adicione produto ao carrinho
2. Tente adicionar quantidade maior que o estoque
3. ✅ **Resultado Esperado:** Erro "Estoque insuficiente"

---

### Teste 3.9: Validação de Checkout sem Login

1. Faça logout
2. Adicione produto ao carrinho
3. Tente finalizar compra
4. ✅ **Resultado Esperado:** Redirecionamento para login

---

### Teste 3.10: Validação de Checkout sem Endereço

1. Faça login com cliente sem endereços
2. Tente finalizar compra
3. ✅ **Resultado Esperado:** Mensagem para adicionar endereço

---

## 🎯 PARTE 4: TESTES DE SEGURANÇA

### Teste 4.1: Acesso Admin sem Login

1. Faça logout
2. Tente acessar http://localhost:5000/admin
3. ✅ **Resultado Esperado:** Redirecionamento para login

---

### Teste 4.2: Cliente Tentando Acessar Admin

1. Faça login como cliente
2. Tente acessar http://localhost:5000/admin
3. ✅ **Resultado Esperado:** Acesso negado

---

### Teste 4.3: Editar Endereço de Outro Usuário

1. Como cliente, tente acessar `/endereco/editar/999` (ID inexistente)
2. ✅ **Resultado Esperado:** Erro "Endereço não encontrado"

---

### Teste 4.4: Senha com Hash Argon2

1. Verifique no banco de dados
2. ✅ **Resultado Esperado:** Senha armazenada como hash, não texto plano

---

## 📊 CHECKLIST FINAL

### Funcionalidades do Cliente
- [ ] Registro de conta
- [ ] Login
- [ ] Editar perfil (nome e e-mail)
- [ ] Alterar senha
- [ ] Adicionar endereço
- [ ] Editar endereço
- [ ] Deletar endereço
- [ ] Buscar produtos
- [ ] Filtrar por categoria
- [ ] Filtrar por preço
- [ ] Ver detalhes do produto
- [ ] Adicionar ao carrinho
- [ ] Atualizar quantidade no carrinho
- [ ] Remover do carrinho
- [ ] Finalizar compra (checkout)
- [ ] Visualizar pedidos

### Funcionalidades do Admin
- [ ] Login admin
- [ ] Dashboard com 4 cards
- [ ] Criar categoria
- [ ] Editar categoria
- [ ] Deletar categoria
- [ ] Criar produto
- [ ] Upload de imagens
- [ ] Editar produto
- [ ] Deletar produto
- [ ] Visualizar pedidos
- [ ] Atualizar status do pedido
- [ ] Filtrar pedidos por status
- [ ] Visualizar clientes
- [ ] Ver detalhes do cliente

### Correções Específicas
- [ ] Imagens NÃO quebradas
- [ ] Checkout funcionando
- [ ] Endereços gerenciáveis
- [ ] Perfil editável
- [ ] Senha alterável
- [ ] Categorias gerenciáveis
- [ ] Clientes visualizáveis

---

## 🐛 Problemas Conhecidos e Soluções

### Problema: Imagens ainda quebradas
**Solução:** Limpe o banco de dados e recrie os produtos com as novas imagens.

```powershell
# Deletar banco antigo
Remove-Item scee_loja.db

# Recriar banco
python app.py
# (Ctrl+C para parar)

# Popular com dados de exemplo
python criar_categorias.py
python popular_produtos.py
```

---

## ✅ RESULTADO ESPERADO FINAL

Após completar todos os testes:

- ✅ **15 testes de cliente** passando
- ✅ **15 testes de admin** passando
- ✅ **10 testes de validação** passando
- ✅ **4 testes de segurança** passando

**Total: 44 testes** ✅

---

**Sistema 100% funcional e pronto para uso!** 🎉
