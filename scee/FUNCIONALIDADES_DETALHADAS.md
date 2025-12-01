# 📋 FUNCIONALIDADES DETALHADAS - SCEE

**Sistema de Comércio Eletrônico**  
**Análise Técnica Completa**

---

## 📑 ÍNDICE

1. [Módulo de Autenticação](#1-módulo-de-autenticação)
2. [Módulo de Produtos](#2-módulo-de-produtos)
3. [Módulo de Carrinho](#3-módulo-de-carrinho)
4. [Módulo de Pedidos](#4-módulo-de-pedidos)
5. [Módulo de Frete](#5-módulo-de-frete)
6. [Módulo de Pagamento](#6-módulo-de-pagamento)
7. [Módulo Administrativo](#7-módulo-administrativo)
8. [Módulo de Endereços](#8-módulo-de-endereços)
9. [Controle de Estoque](#9-controle-de-estoque)
10. [Segurança e Validações](#10-segurança-e-validações)

---

## 1. MÓDULO DE AUTENTICAÇÃO

### 1.1 Registro de Cliente

**Arquivo:** `controllers/auth_controller.py`  
**Método:** `registrar_cliente()`

#### Fluxo de Execução:

```
1. Usuário preenche formulário
   ├── Nome completo
   ├── Email
   ├── CPF (apenas números)
   ├── Senha
   └── Confirmação de senha
   ↓
2. Sistema valida dados
   ├── Campos obrigatórios preenchidos?
   ├── Senhas coincidem?
   ├── Email válido (regex)?
   ├── CPF válido (dígitos verificadores)?
   ├── Senha forte?
   ├── Email já cadastrado?
   └── CPF já cadastrado?
   ↓
3. Sistema cria hash da senha (Argon2)
   ↓
4. Sistema salva cliente no banco
   ↓
5. Retorna sucesso
```

#### Validações Implementadas:

**1. Validação de Email:**
```python
def validar_email(self, email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```
- Formato padrão de email
- Domínio obrigatório
- Extensão mínima de 2 caracteres

**2. Validação de CPF:**
```python
def validar_cpf(self, cpf: str) -> bool:
    # Verifica formato (11 dígitos)
    if not cpf or len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Rejeita CPFs com todos dígitos iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    
    return int(cpf[10]) == digito2
```
- Algoritmo oficial de validação de CPF
- Verifica dígitos verificadores
- Rejeita CPFs inválidos (111.111.111-11, etc.)

**3. Validação de Senha Forte:**
```python
def validar_senha_forte(self, senha: str) -> tuple[bool, str]:
    if len(senha) < 8:
        return False, "Mínimo 8 caracteres"
    if not re.search(r'[A-Z]', senha):
        return False, "Ao menos uma maiúscula"
    if not re.search(r'[a-z]', senha):
        return False, "Ao menos uma minúscula"
    if not re.search(r'[0-9]', senha):
        return False, "Ao menos um número"
    return True, ""
```
- Mínimo 8 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 letra minúscula
- Pelo menos 1 número

#### Hash de Senha (Argon2):

```python
from argon2 import PasswordHasher

ph = PasswordHasher()
senha_hash = ph.hash(senha)  # Gera hash seguro
```

**Por que Argon2?**
- Vencedor do Password Hashing Competition (2015)
- Resistente a ataques de GPU
- Resistente a ataques de força bruta
- Configuração de memória e tempo ajustável

### 1.2 Login de Cliente

**Método:** `login_cliente()`

#### Fluxo:

```
1. Usuário informa email e senha
   ↓
2. Sistema busca cliente por email
   ↓
3. Cliente existe?
   ├── NÃO → "Email ou senha incorretos"
   └── SIM → Continua
   ↓
4. Sistema verifica hash da senha
   ↓
5. Senha correta?
   ├── NÃO → "Email ou senha incorretos"
   └── SIM → Cria sessão
   ↓
6. Armazena ID e nome na sessão
   ↓
7. Redireciona para conta
```

#### Verificação de Senha:

```python
try:
    self.ph.verify(cliente.senha_hash, senha)
    return True, "Login realizado", cliente
except VerifyMismatchError:
    return False, "Email ou senha incorretos", None
```

**Segurança:**
- Mensagem genérica (não revela se email existe)
- Hash verificado de forma segura
- Sessão criada apenas após verificação

### 1.3 Login de Admin

**Método:** `login_admin()`

- Fluxo similar ao login de cliente
- Sessão separada (`admin_id` vs `cliente_id`)
- Acesso à área administrativa

---

## 2. MÓDULO DE PRODUTOS

### 2.1 Listagem de Produtos

**Arquivo:** `app.py`  
**Rota:** `/produtos`

#### Funcionalidades:

1. **Listagem completa**
   - Todos os produtos ativos
   - Ordenados por ID

2. **Filtro por categoria**
   - URL: `/produtos?categoria=1`
   - Filtra produtos da categoria selecionada

3. **Informações exibidas:**
   - Nome do produto
   - Preço formatado
   - Categoria
   - Imagem principal
   - **Indicador de estoque**

#### Indicadores de Estoque:

```html
{% if produto.estoque > 0 %}
    <p class="estoque-disponivel">
        ✓ Em estoque ({{ produto.estoque }} unidades)
    </p>
{% else %}
    <p class="sem-estoque">✗ SEM ESTOQUE</p>
{% endif %}
```

### 2.2 Detalhes do Produto

**Rota:** `/produto/<int:produto_id>`

#### Informações Exibidas:

1. **Dados básicos:**
   - Nome
   - SKU
   - Descrição completa
   - Preço
   - Categoria

2. **Imagens:**
   - Galeria com todas as imagens
   - Até 5 imagens por produto

3. **Estoque:**
   - Quantidade disponível
   - Mensagem se sem estoque
   - Botão desabilitado se sem estoque

#### Validação de Estoque:

```html
{% if produto.estoque > 0 %}
    <form method="POST" action="{{ url_for('adicionar_carrinho') }}">
        <button type="submit" class="btn btn-primary">
            🛒 Adicionar ao Carrinho
        </button>
    </form>
{% else %}
    <button class="btn btn-disabled" disabled>
        🛒 Indisponível para Compra
    </button>
    <p class="texto-indisponivel">
        Entre em contato para saber quando estará disponível.
    </p>
{% endif %}
```

### 2.3 Criação de Produto (Admin)

**Arquivo:** `controllers/produto_controller.py`  
**Método:** `criar_produto()`

#### Fluxo:

```
1. Admin preenche formulário
   ├── Nome
   ├── SKU (único)
   ├── Descrição
   ├── Preço
   ├── Estoque
   ├── Categoria
   └── Imagens (até 5)
   ↓
2. Sistema valida dados
   ├── Campos obrigatórios?
   ├── Preço > 0?
   ├── Estoque >= 0?
   ├── SKU único?
   ├── Categoria existe?
   └── Imagens válidas?
   ↓
3. Sistema cria produto
   ↓
4. Sistema salva imagens
   ├── Valida extensão (jpg, jpeg, png)
   ├── Gera nome seguro
   ├── Salva em uploads/
   └── Cria registro ImagemProduto
   ↓
5. Retorna sucesso
```

#### Validações:

```python
def criar_produto(self, nome, sku, descricao, preco, estoque, 
                  categoria_id, imagens):
    # Validar campos obrigatórios
    if not all([nome, sku, descricao]):
        return False, "Campos obrigatórios ausentes", None
    
    # Validar preço
    if preco <= 0:
        return False, "Preço deve ser maior que zero", None
    
    # Validar estoque
    if estoque < 0:
        return False, "Estoque não pode ser negativo", None
    
    # Validar SKU único
    if self.produto_repo.sku_exists(sku):
        return False, "SKU já cadastrado", None
    
    # Validar categoria
    categoria = self.categoria_repo.get_by_id(categoria_id)
    if not categoria:
        return False, "Categoria não encontrada", None
    
    # Criar produto
    # ...
```

#### Upload de Imagens:

```python
def _salvar_imagens(self, produto, imagens):
    for i, imagem in enumerate(imagens[:5]):  # Máximo 5
        if imagem and self.validar_extensao(imagem.filename):
            # Nome seguro
            filename = secure_filename(f"{produto.sku}_{i}_{imagem.filename}")
            
            # Salvar arquivo
            filepath = os.path.join(self.upload_folder, filename)
            imagem.save(filepath)
            
            # Criar registro
            img_produto = ImagemProduto(
                produto_id=produto.id,
                caminho=f"uploads/{filename}",
                ordem=i
            )
            self.session.add(img_produto)
    
    self.session.commit()
```

**Segurança:**
- `secure_filename()` previne path traversal
- Validação de extensão
- Limite de 5 imagens
- Tamanho máximo configurável

---

## 3. MÓDULO DE CARRINHO

### 3.1 Estrutura do Carrinho

**Arquivo:** `controllers/carrinho_controller.py`

#### Classes:

**1. ItemCarrinho:**
```python
class ItemCarrinho:
    def __init__(self, produto_id, nome, preco, quantidade):
        self.produto_id = produto_id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.subtotal = preco * quantidade  # Calculado automaticamente
    
    def atualizar_quantidade(self, quantidade):
        self.quantidade = quantidade
        self.subtotal = self.preco * quantidade  # Recalcula
```

**Encapsulamento:**
- Subtotal sempre consistente
- Atualização controlada

**2. CarrinhoController:**
```python
class CarrinhoController:
    def __init__(self):
        self.itens: Dict[int, ItemCarrinho] = {}  # Encapsulado
    
    def adicionar_item(self, produto_id, nome, preco, quantidade):
        # Validação + lógica
    
    def remover_item(self, produto_id):
        # Validação + lógica
    
    def atualizar_quantidade(self, produto_id, quantidade):
        # Validação + lógica
    
    def calcular_total(self):
        return sum(item.subtotal for item in self.itens.values())
```

### 3.2 Adicionar ao Carrinho

**Rota:** `/carrinho/adicionar/<int:produto_id>`

#### Fluxo Completo:

```
1. Usuário clica "Adicionar ao Carrinho"
   ↓
2. Sistema busca produto no banco
   ↓
3. Produto existe?
   ├── NÃO → Erro "Produto não encontrado"
   └── SIM → Continua
   ↓
4. Produto tem estoque?
   ├── estoque == 0 → Erro "SEM ESTOQUE"
   ├── estoque < quantidade → Erro "Estoque insuficiente"
   └── estoque >= quantidade → Continua
   ↓
5. Adiciona ao carrinho
   ├── Produto já no carrinho? → Incrementa quantidade
   └── Produto novo? → Cria ItemCarrinho
   ↓
6. Exibe mensagem de sucesso
   ↓
7. Redireciona para carrinho
```

#### Código:

```python
@app.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    if 'cliente_id' not in session:
        flash('Faça login para adicionar ao carrinho', 'error')
        return redirect(url_for('login'))
    
    quantidade = 1
    
    db_session = db.get_session()
    produto_repo = ProdutoRepository(db_session)
    produto = produto_repo.get_by_id(produto_id)
    
    # Validações
    if not produto:
        flash('Produto não encontrado', 'error')
        db_session.close()
        return redirect(url_for('produtos'))
    
    if produto.estoque == 0:
        flash('❌ Produto SEM ESTOQUE', 'error')
        db_session.close()
        return redirect(url_for('produto_detalhe', produto_id=produto_id))
    
    if produto.estoque < quantidade:
        flash(f'❌ Estoque insuficiente! Disponível: {produto.estoque}', 'error')
        db_session.close()
        return redirect(url_for('produto_detalhe', produto_id=produto_id))
    
    # Adiciona ao carrinho
    carrinho_obj = get_carrinho()
    sucesso, mensagem = carrinho_obj.adicionar_item(
        produto.id, produto.nome, produto.preco, quantidade
    )
    
    flash(mensagem, 'success' if sucesso else 'error')
    db_session.close()
    
    return redirect(url_for('carrinho'))
```

### 3.3 Visualizar Carrinho

**Rota:** `/carrinho`

#### Informações Exibidas:

```html
Para cada item:
├── Imagem do produto
├── Nome
├── Preço unitário
├── Quantidade (editável)
├── Subtotal
└── Botão remover

Total do carrinho: R$ XX,XX

Botões:
├── Continuar comprando
└── Finalizar compra
```

### 3.4 Atualizar Quantidade

**Rota:** `/carrinho/atualizar/<int:produto_id>`

```python
def atualizar_quantidade(self, produto_id, quantidade):
    if produto_id not in self.itens:
        return False, "Item não encontrado"
    
    if quantidade <= 0:
        return False, "Quantidade inválida"
    
    self.itens[produto_id].atualizar_quantidade(quantidade)
    return True, "Quantidade atualizada"
```

### 3.5 Remover Item

**Rota:** `/carrinho/remover/<int:produto_id>`

```python
def remover_item(self, produto_id):
    if produto_id not in self.itens:
        return False, "Item não encontrado"
    
    del self.itens[produto_id]
    return True, "Item removido"
```

---

## 4. MÓDULO DE PEDIDOS

### 4.1 Criar Pedido

**Arquivo:** `controllers/pedido_controller.py`  
**Método:** `criar_pedido()`

#### Fluxo Completo:

```
1. Cliente finaliza compra
   ├── Seleciona endereço
   ├── Escolhe tipo de frete
   └── Escolhe método de pagamento
   ↓
2. Sistema valida dados
   ├── Carrinho vazio?
   ├── Método de pagamento válido?
   ├── Tipo de frete válido?
   ├── Endereço pertence ao cliente?
   └── Todos válidos? → Continua
   ↓
3. Sistema inicia transação
   ↓
4. Para cada item do carrinho:
   ├── Busca produto no banco
   ├── Produto existe?
   ├── Tem estoque suficiente?
   ├── Atualiza estoque (produto.estoque -= quantidade)
   └── Cria ItemPedido
   ↓
5. Calcula frete
   ├── Instancia calculadora (Fixo/Correios/Expresso)
   ├── Calcula peso total (0.5kg por item)
   ├── Chama calcular_frete(cep, peso, valor)
   └── Obtém (valor_frete, prazo_entrega)
   ↓
6. Calcula total
   total_final = total_produtos + valor_frete
   ↓
7. Cria pedido
   ├── Cliente ID
   ├── Total com frete
   ├── Endereço completo
   ├── Método de pagamento
   ├── Status: "Pendente"
   ├── Tipo de frete
   ├── Valor do frete
   └── Prazo de entrega
   ↓
8. Salva itens do pedido
   ↓
9. Commit da transação
   ↓
10. Limpa carrinho
   ↓
11. Retorna sucesso
```

#### Código Simplificado:

```python
def criar_pedido(self, cliente_id, itens_carrinho, endereco_id,
                 metodo_pagamento, tipo_frete='Fixo'):
    # Validações
    if not itens_carrinho:
        return False, "Carrinho vazio", None
    
    if metodo_pagamento not in ['Cartão', 'Pix', 'Boleto']:
        return False, "Método de pagamento inválido", None
    
    if tipo_frete not in ['Fixo', 'Correios', 'Expresso']:
        return False, "Tipo de frete inválido", None
    
    endereco = self.endereco_repo.get_by_id(endereco_id)
    if not endereco or endereco.cliente_id != cliente_id:
        return False, "Endereço inválido", None
    
    try:
        self.session.begin_nested()  # Transação
        
        total = 0
        itens_pedido = []
        
        # Processar cada item
        for item in itens_carrinho:
            produto = self.produto_repo.get_by_id(item.produto_id)
            
            if not produto:
                self.session.rollback()
                return False, f"Produto {item.nome} não encontrado", None
            
            if produto.estoque < item.quantidade:
                self.session.rollback()
                return False, f"Estoque insuficiente para {produto.nome}", None
            
            # Atualiza estoque
            produto.estoque -= item.quantidade
            
            # Calcula subtotal
            subtotal = produto.preco * item.quantidade
            total += subtotal
            
            # Cria item do pedido
            item_pedido = ItemPedido(
                produto_id=produto.id,
                produto_nome=produto.nome,
                quantidade=item.quantidade,
                preco_unitario=produto.preco,
                subtotal=subtotal
            )
            itens_pedido.append(item_pedido)
        
        # Calcular frete (POLIMORFISMO)
        from controllers.integracao_controller import (
            FreteFixo, FreteCorreios, FreteExpresso
        )
        
        if tipo_frete == 'Fixo':
            calculadora = FreteFixo()
        elif tipo_frete == 'Correios':
            calculadora = FreteCorreios()
        else:
            calculadora = FreteExpresso()
        
        peso_total = sum(item.quantidade * 0.5 for item in itens_carrinho)
        valor_frete, prazo_entrega = calculadora.calcular_frete(
            endereco.cep, peso_total, total
        )
        
        # Total com frete
        total_com_frete = total + valor_frete
        
        # Criar pedido
        pedido = Pedido(
            cliente_id=cliente_id,
            total=total_com_frete,
            endereco_entrega=endereco_completo,
            metodo_pagamento=metodo_pagamento,
            status='Pendente',
            tipo_frete=tipo_frete,
            valor_frete=valor_frete,
            prazo_entrega=prazo_entrega
        )
        
        pedido = self.pedido_repo.create(pedido)
        
        # Salvar itens
        for item in itens_pedido:
            item.pedido_id = pedido.id
            self.session.add(item)
        
        self.session.commit()
        
        return True, "Pedido criado com sucesso", pedido
        
    except SQLAlchemyError as e:
        self.session.rollback()
        return False, f"Erro ao criar pedido: {str(e)}", None
```

**Transação Atômica:**
- Tudo ou nada
- Se falhar em qualquer ponto, rollback
- Garante consistência dos dados

### 4.2 Cancelar Pedido

**Método:** `cancelar_pedido()`

#### Regras:

1. Apenas pedidos "Pendente" ou "Processando" podem ser cancelados
2. Estoque é devolvido automaticamente
3. Status atualizado para "Cancelado"

#### Código:

```python
def cancelar_pedido(self, pedido_id, cliente_id):
    pedido = self.pedido_repo.get_by_id(pedido_id)
    
    # Validações
    if not pedido:
        return False, "Pedido não encontrado"
    
    if pedido.cliente_id != cliente_id:
        return False, "Pedido não pertence ao cliente"
    
    if pedido.status not in ['Pendente', 'Processando']:
        return False, "Pedido não pode ser cancelado"
    
    try:
        # Devolver estoque
        for item in pedido.itens:
            produto = self.produto_repo.get_by_id(item.produto_id)
            if produto:
                produto.estoque += item.quantidade
        
        # Atualizar status
        pedido.status = 'Cancelado'
        self.pedido_repo.update(pedido)
        
        return True, "Pedido cancelado com sucesso"
        
    except SQLAlchemyError as e:
        self.session.rollback()
        return False, f"Erro ao cancelar pedido: {str(e)}"
```

### 4.3 Atualizar Status (Admin)

**Método:** `atualizar_status()`

#### Status Possíveis:

1. **Pendente** - Aguardando processamento
2. **Processando** - Em preparação
3. **Enviado** - A caminho do cliente
4. **Entregue** - Finalizado com sucesso
5. **Cancelado** - Cancelado

#### Fluxo:

```
Admin → Seleciona pedido → Escolhe novo status → Sistema atualiza
```

---

## 5. MÓDULO DE FRETE

### 5.1 Arquitetura (POLIMORFISMO)

**Arquivo:** `controllers/integracao_controller.py`

#### Hierarquia de Classes:

```
CalculadoraFreteBase (ABC)
    ├── FreteFixo
    ├── FreteCorreios
    └── FreteExpresso
```

### 5.2 Classe Abstrata Base

```python
from abc import ABC, abstractmethod

class CalculadoraFreteBase(ABC):
    """
    Classe abstrata base para cálculo de frete.
    Define o CONTRATO que todas as calculadoras devem seguir.
    """
    
    @abstractmethod
    def calcular_frete(
        self, 
        cep_destino: str, 
        peso_kg: float, 
        valor_produtos: float
    ) -> tuple[float, int]:
        """
        Calcula valor e prazo do frete.
        
        Args:
            cep_destino: CEP de destino (8 dígitos)
            peso_kg: Peso total em kg
            valor_produtos: Valor total dos produtos
            
        Returns:
            (valor_frete, prazo_dias)
        """
        pass
```

### 5.3 FreteFixo

**Características:**
- Valor fixo de R$ 15,00
- Prazo fixo de 7 dias
- Frete grátis para compras acima de R$ 500

```python
class FreteFixo(CalculadoraFreteBase):
    def __init__(self, valor_fixo=15.00, prazo_fixo=7):
        self.valor_fixo = valor_fixo
        self.prazo_fixo = prazo_fixo
    
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        # Frete grátis acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, self.prazo_fixo
        
        return self.valor_fixo, self.prazo_fixo
```

**Exemplo:**
```
Compra de R$ 300,00
→ Frete: R$ 15,00 / 7 dias

Compra de R$ 600,00
→ Frete: R$ 0,00 / 7 dias (GRÁTIS)
```

### 5.4 FreteCorreios

**Características:**
- Valor varia por CEP (distância)
- Valor varia por peso
- Prazo varia por distância
- Frete grátis acima de R$ 500

```python
class FreteCorreios(CalculadoraFreteBase):
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        cep_limpo = cep_destino.replace('-', '').replace('.', '')
        
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return 20.0, 10  # CEP inválido
        
        primeiro_digito = int(cep_limpo[0])
        
        # Simula distância pelo primeiro dígito do CEP
        if primeiro_digito <= 3:  # Sudeste
            valor_base = 15.0
            prazo_base = 5
        elif primeiro_digito <= 6:  # Sul/Centro-Oeste
            valor_base = 25.0
            prazo_base = 8
        else:  # Norte/Nordeste
            valor_base = 35.0
            prazo_base = 12
        
        # Adiciona custo por peso (R$ 2 por kg adicional após 1kg)
        if peso_kg > 1:
            valor_base += (peso_kg - 1) * 2.0
        
        # Frete grátis acima de R$ 500
        if valor_produtos >= 500:
            return 0.0, prazo_base
        
        return round(valor_base, 2), prazo_base
```

**Exemplos:**

```
CEP 01000-000 (São Paulo), 2kg, R$ 300
→ Primeiro dígito: 0 (Sudeste)
→ Valor base: R$ 15,00
→ Peso adicional: (2 - 1) * 2 = R$ 2,00
→ Total: R$ 17,00 / 5 dias

CEP 60000-000 (Fortaleza), 1kg, R$ 300
→ Primeiro dígito: 6 (Centro-Oeste)
→ Valor base: R$ 25,00
→ Peso adicional: 0
→ Total: R$ 25,00 / 8 dias

CEP 80000-000 (Curitiba), 3kg, R$ 600
→ Primeiro dígito: 8 (Norte/Nordeste)
→ Valor base: R$ 35,00
→ Peso adicional: (3 - 1) * 2 = R$ 4,00
→ Subtotal: R$ 39,00
→ Frete grátis (valor >= 500): R$ 0,00 / 12 dias
```

### 5.5 FreteExpresso

**Características:**
- Valor mais alto (premium)
- Prazo mais curto (rápido)
- 50% de desconto acima de R$ 500 (não grátis)

```python
class FreteExpresso(CalculadoraFreteBase):
    def calcular_frete(self, cep_destino, peso_kg, valor_produtos):
        cep_limpo = cep_destino.replace('-', '').replace('.', '')
        
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return 40.0, 3
        
        primeiro_digito = int(cep_limpo[0])
        
        # Valores mais altos, prazos menores
        if primeiro_digito <= 3:
            valor_base = 30.0
            prazo = 2
        elif primeiro_digito <= 6:
            valor_base = 45.0
            prazo = 3
        else:
            valor_base = 60.0
            prazo = 5
        
        # Custo por peso (R$ 3 por kg adicional)
        if peso_kg > 1:
            valor_base += (peso_kg - 1) * 3.0
        
        # 50% de desconto acima de R$ 500
        if valor_produtos >= 500:
            valor_base *= 0.5
        
        return round(valor_base, 2), prazo
```

**Exemplos:**

```
CEP 01000-000, 1kg, R$ 300
→ Valor: R$ 30,00 / 2 dias

CEP 01000-000, 1kg, R$ 600
→ Valor base: R$ 30,00
→ Desconto 50%: R$ 15,00 / 2 dias

CEP 80000-000, 3kg, R$ 300
→ Valor base: R$ 60,00
→ Peso adicional: (3 - 1) * 3 = R$ 6,00
→ Total: R$ 66,00 / 5 dias
```

### 5.6 Tabela Comparativa

| Tipo | Valor Base | Prazo | Grátis R$500+ | Desconto R$500+ |
|------|------------|-------|---------------|-----------------|
| **Fixo** | R$ 15 | 7 dias | ✅ 100% | - |
| **Correios** | R$ 15-35 | 5-12 dias | ✅ 100% | - |
| **Expresso** | R$ 30-60 | 2-5 dias | ❌ | ⚠️ 50% |

### 5.7 Uso Polimórfico

```python
# No PedidoController
if tipo_frete == 'Fixo':
    calculadora = FreteFixo()
elif tipo_frete == 'Correios':
    calculadora = FreteCorreios()
else:
    calculadora = FreteExpresso()

# POLIMORFISMO: Mesma chamada, comportamentos diferentes!
valor_frete, prazo_entrega = calculadora.calcular_frete(
    endereco.cep, 
    peso_total, 
    total
)
```

**Benefícios:**
- ✅ Fácil adicionar novos tipos de frete
- ✅ Código desacoplado
- ✅ Testável independentemente
- ✅ Mesma interface, comportamentos diferentes

---

## 6. MÓDULO DE PAGAMENTO

### 6.1 Arquitetura (POLIMORFISMO)

**Hierarquia:**

```
GatewayPagamentoBase (ABC)
    ├── PagamentoCartao
    └── PagamentoPix
```

### 6.2 Classe Abstrata Base

```python
class GatewayPagamentoBase(ABC):
    @abstractmethod
    def processar_pagamento(
        self, 
        valor: float, 
        dados_pagamento: Dict[str, Any]
    ) -> tuple[bool, str]:
        pass
    
    @abstractmethod
    def validar_dados_pagamento(
        self, 
        dados_pagamento: Dict[str, Any]
    ) -> tuple[bool, str]:
        pass
```

### 6.3 PagamentoCartao

```python
class PagamentoCartao(GatewayPagamentoBase):
    def processar_pagamento(self, valor, dados_pagamento):
        # Valida dados
        valido, msg = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, msg
        
        # Simula processamento
        if valor > 10000:
            return False, "Valor acima do limite"
        
        return True, "Pagamento aprovado"
    
    def validar_dados_pagamento(self, dados):
        campos = ['numero_cartao', 'cvv', 'validade', 'titular']
        
        for campo in campos:
            if campo not in dados or not dados[campo]:
                return False, f"Campo {campo} obrigatório"
        
        # Valida número (16 dígitos)
        numero = str(dados['numero_cartao']).replace(' ', '')
        if not numero.isdigit() or len(numero) != 16:
            return False, "Número do cartão inválido"
        
        # Valida CVV (3 ou 4 dígitos)
        cvv = str(dados['cvv'])
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            return False, "CVV inválido"
        
        return True, "Dados válidos"
```

### 6.4 PagamentoPix

```python
class PagamentoPix(GatewayPagamentoBase):
    def processar_pagamento(self, valor, dados_pagamento):
        valido, msg = self.validar_dados_pagamento(dados_pagamento)
        if not valido:
            return False, msg
        
        # Pix sempre aprovado (simulação)
        return True, "Pagamento via Pix aprovado"
    
    def validar_dados_pagamento(self, dados):
        if 'cpf_pagador' not in dados:
            return False, "CPF obrigatório"
        
        cpf = str(dados['cpf_pagador']).replace('.', '').replace('-', '')
        if not cpf.isdigit() or len(cpf) != 11:
            return False, "CPF inválido"
        
        return True, "Dados válidos"
```

---

## 7. MÓDULO ADMINISTRATIVO

### 7.1 Dashboard

**Rota:** `/admin`

**Informações exibidas:**
- Total de clientes
- Total de produtos
- Total de pedidos
- Total de categorias

### 7.2 Gestão de Produtos

**Funcionalidades:**
- Listar todos os produtos
- Criar novo produto
- Editar produto existente
- Remover produto
- Upload de imagens

### 7.3 Gestão de Categorias

**Funcionalidades:**
- Listar categorias
- Criar categoria
- Editar categoria
- Remover categoria

### 7.4 Gestão de Pedidos

**Funcionalidades:**
- Listar todos os pedidos
- Visualizar detalhes
- Atualizar status
- Filtrar por status

---

## 8. MÓDULO DE ENDEREÇOS

### 8.1 Adicionar Endereço

**Arquivo:** `controllers/cliente_controller.py`  
**Método:** `adicionar_endereco()`

#### Validações:

```python
def adicionar_endereco(self, cliente_id, rua, numero, complemento,
                       bairro, cidade, estado, cep):
    # Campos obrigatórios
    if not all([rua, numero, bairro, cidade, estado, cep]):
        return False, "Campos obrigatórios ausentes", None
    
    # UF (2 caracteres)
    if len(estado) != 2:
        return False, "Estado deve ter 2 caracteres (UF)", None
    
    # CEP (8 dígitos)
    if len(cep) != 8 or not cep.isdigit():
        return False, "CEP inválido", None
    
    # Criar endereço
    endereco = Endereco(
        cliente_id=cliente_id,
        rua=rua,
        numero=numero,
        complemento=complemento,
        bairro=bairro,
        cidade=cidade,
        estado=estado.upper(),
        cep=cep
    )
    
    endereco = self.endereco_repo.create(endereco)
    return True, "Endereço adicionado", endereco
```

### 8.2 Listar Endereços

```python
def listar_enderecos(self, cliente_id):
    return self.endereco_repo.get_by_cliente(cliente_id)
```

### 8.3 Atualizar Endereço

```python
def atualizar_endereco(self, endereco_id, rua, numero, ...):
    endereco = self.endereco_repo.get_by_id(endereco_id)
    if not endereco:
        return False, "Endereço não encontrado"
    
    # Validações...
    
    # Atualiza campos
    endereco.rua = rua
    endereco.numero = numero
    # ...
    
    self.endereco_repo.update(endereco)
    return True, "Endereço atualizado"
```

### 8.4 Deletar Endereço

```python
def deletar_endereco(self, endereco_id):
    endereco = self.endereco_repo.get_by_id(endereco_id)
    if not endereco:
        return False, "Endereço não encontrado"
    
    self.endereco_repo.delete(endereco)
    return True, "Endereço removido"
```

---

## 9. CONTROLE DE ESTOQUE

### 9.1 Validação ao Adicionar ao Carrinho

```python
# Verifica se produto existe
if not produto:
    return "Produto não encontrado"

# Verifica se tem estoque
if produto.estoque == 0:
    return "Produto SEM ESTOQUE"

# Verifica se tem estoque suficiente
if produto.estoque < quantidade:
    return f"Estoque insuficiente! Disponível: {produto.estoque}"
```

### 9.2 Atualização ao Criar Pedido

```python
# Para cada item do pedido
for item in itens_carrinho:
    produto = produto_repo.get_by_id(item.produto_id)
    
    # Valida estoque novamente
    if produto.estoque < item.quantidade:
        rollback()
        return "Estoque insuficiente"
    
    # Atualiza estoque
    produto.estoque -= item.quantidade
```

### 9.3 Devolução ao Cancelar Pedido

```python
# Ao cancelar pedido
for item in pedido.itens:
    produto = produto_repo.get_by_id(item.produto_id)
    if produto:
        # Devolve estoque
        produto.estoque += item.quantidade
```

### 9.4 Indicadores Visuais

**Listagem de produtos:**
```html
{% if produto.estoque > 0 %}
    <p class="estoque-disponivel">
        ✓ Em estoque ({{ produto.estoque }} unidades)
    </p>
{% else %}
    <p class="sem-estoque">✗ SEM ESTOQUE</p>
{% endif %}
```

**Detalhes do produto:**
```html
{% if produto.estoque > 0 %}
    <p class="estoque-disponivel">
        ✓ Em estoque: {{ produto.estoque }} unidades disponíveis
    </p>
    <button type="submit">🛒 Adicionar ao Carrinho</button>
{% else %}
    <div class="alerta-sem-estoque">
        <p class="sem-estoque">✗ PRODUTO SEM ESTOQUE</p>
        <p class="aviso-estoque">
            Este produto está temporariamente indisponível.
        </p>
    </div>
    <button class="btn-disabled" disabled>
        🛒 Indisponível para Compra
    </button>
{% endif %}
```

---

## 10. SEGURANÇA E VALIDAÇÕES

### 10.1 Hash de Senhas

**Algoritmo:** Argon2

```python
from argon2 import PasswordHasher

ph = PasswordHasher()

# Criar hash
senha_hash = ph.hash(senha)

# Verificar senha
try:
    ph.verify(senha_hash, senha)
    # Senha correta
except VerifyMismatchError:
    # Senha incorreta
```

**Por que Argon2?**
- Vencedor do Password Hashing Competition
- Resistente a ataques de GPU
- Resistente a ataques de força bruta
- Configurável (memória, tempo, paralelismo)

### 10.2 Validação de CPF

```python
def validar_cpf(self, cpf: str) -> bool:
    # Formato
    if not cpf or len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # CPFs inválidos (111.111.111-11, etc.)
    if cpf == cpf[0] * 11:
        return False
    
    # Primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    
    if int(cpf[9]) != digito1:
        return False
    
    # Segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    
    return int(cpf[10]) == digito2
```

### 10.3 Validação de Email

```python
def validar_email(self, email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### 10.4 Validação de Senha Forte

```python
def validar_senha_forte(self, senha: str) -> tuple[bool, str]:
    if len(senha) < 8:
        return False, "Mínimo 8 caracteres"
    if not re.search(r'[A-Z]', senha):
        return False, "Ao menos uma maiúscula"
    if not re.search(r'[a-z]', senha):
        return False, "Ao menos uma minúscula"
    if not re.search(r'[0-9]', senha):
        return False, "Ao menos um número"
    return True, ""
```

### 10.5 Prevenção de SQL Injection

- SQLAlchemy ORM (queries parametrizadas)
- Não usa SQL direto
- Validação de tipos

### 10.6 Upload Seguro de Arquivos

```python
from werkzeug.utils import secure_filename

# Nome seguro (previne path traversal)
filename = secure_filename(imagem.filename)

# Validação de extensão
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def validar_extensao(self, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### 10.7 Sessões Seguras

```python
# Flask sessions
app.secret_key = 'chave-secreta-aleatoria'

# Armazenar ID do usuário
session['cliente_id'] = cliente.id
session['cliente_nome'] = cliente.nome

# Verificar autenticação
if 'cliente_id' not in session:
    return redirect(url_for('login'))

# Logout
session.clear()
```

---

## 📊 RESUMO TÉCNICO

### Estatísticas:

- **Linhas de código:** 3.500+
- **Arquivos Python:** 28
- **Templates HTML:** 15
- **Modelos:** 8
- **Repositórios:** 7
- **Controllers:** 6
- **Rotas Flask:** 40+
- **Classes abstratas:** 2
- **Implementações polimórficas:** 5

### Conceitos de POO:

1. ✅ **Herança** - BaseRepository, modelos SQLAlchemy
2. ✅ **Polimorfismo** - Fretes (3) e Pagamentos (2)
3. ✅ **Encapsulamento** - Controllers, ItemCarrinho
4. ✅ **Abstração** - Classes ABC, interfaces

### Padrões de Projeto:

1. ✅ **MVC** - Model-View-Controller
2. ✅ **Repository** - Acesso a dados
3. ✅ **Strategy** - Calculadoras de frete
4. ✅ **Dependency Injection** - Session nos controllers

---

**Sistema completo, funcional e demonstrando POO na prática!** 🚀
