# 🎤 SCRIPT DE APRESENTAÇÃO - 10 MINUTOS

**Sistema:** SCEE - Sistema de Comércio Eletrônico  
**Tempo:** 10 minutos  
**Objetivo:** Demonstrar conceitos de POO aplicados

---

## ⏱️ CRONOGRAMA

| Tempo | Tópico | Duração |
|-------|--------|---------|
| 0:00-1:00 | Introdução e Visão Geral | 1 min |
| 1:00-2:30 | Arquitetura MVC | 1.5 min |
| 2:30-5:30 | Conceitos de POO | 3 min |
| 5:30-7:30 | Demonstração Prática | 2 min |
| 7:30-9:30 | Funcionalidades Principais | 2 min |
| 9:30-10:00 | Conclusão | 0.5 min |

---

## 📝 SCRIPT COMPLETO

### [0:00-1:00] INTRODUÇÃO E VISÃO GERAL (1 min)

**[SLIDE 1: Título]**

> "Bom dia/Boa tarde! Hoje vou apresentar o **SCEE - Sistema de Comércio Eletrônico**, um projeto desenvolvido em Python que demonstra na prática os **4 pilares da Programação Orientada a Objetos**."

**[SLIDE 2: O que é o SCEE?]**

> "O SCEE é uma aplicação web completa de e-commerce que permite:"
> - Cadastro e autenticação de clientes
> - Catálogo de produtos com controle de estoque
> - Carrinho de compras
> - Sistema de pedidos com **3 opções de frete**
> - **3 métodos de pagamento**
> - Área administrativa completa

**[Mostrar tela inicial do sistema]**

> "Desenvolvido com **Flask**, **SQLAlchemy** e **SQLite**, o sistema possui mais de **3.500 linhas de código** organizadas em uma arquitetura sólida."

---

### [1:00-2:30] ARQUITETURA MVC (1.5 min)

**[SLIDE 3: Diagrama MVC]**

> "O sistema segue o padrão **MVC - Model-View-Controller**, que separa responsabilidades em 3 camadas:"

**[Apontar para o diagrama]**

> "**1. MODELS (Modelos)** - Representam as entidades do domínio:"
> - Cliente, Produto, Pedido, Categoria
> - Usam SQLAlchemy ORM
> - 8 modelos principais

> "**2. VIEWS (Visões)** - Interface com o usuário:"
> - Templates HTML com Jinja2
> - CSS responsivo
> - 15 templates

> "**3. CONTROLLERS (Controladores)** - Lógica de negócio:"
> - AuthController, ProdutoController, PedidoController
> - CarrinhoController, IntegracaoController
> - 6 controllers principais

**[SLIDE 4: Camada Repository]**

> "Além do MVC, implementamos o **Padrão Repository** para abstrair o acesso a dados:"
> - BaseRepository genérico com CRUD
> - Repositórios específicos para cada entidade
> - Facilita testes e manutenção

---

### [2:30-5:30] CONCEITOS DE POO (3 min)

**[SLIDE 5: 4 Pilares da POO]**

> "Agora vamos ver como os **4 pilares da POO** foram aplicados no projeto:"

---

#### **1. HERANÇA** (45 segundos)

**[SLIDE 6: Herança - BaseRepository]**

> "**HERANÇA** está presente principalmente nos repositórios:"

**[Mostrar código]**

```python
class BaseRepository(Generic[T]):
    def create(self, entity: T) -> T
    def get_by_id(self, entity_id: int)
    def get_all(self) -> List[T]
    def update(self, entity: T) -> T
    def delete(self, entity: T) -> None
```

> "Todos os repositórios **herdam** desta classe base, evitando duplicação de código CRUD."

```python
class ClienteRepository(BaseRepository):
    # Herda CRUD + métodos específicos
    def get_by_email(self, email: str)
    def cpf_exists(self, cpf: str)
```

> "Isso garante **reutilização de código** e **manutenção centralizada**."

---

#### **2. POLIMORFISMO** (1 min 15 seg)

**[SLIDE 7: Polimorfismo - Frete]**

> "**POLIMORFISMO** é o conceito mais destacado no projeto. Vou mostrar com o sistema de frete:"

**[Mostrar código]**

```python
# Classe abstrata define o CONTRATO
class CalculadoraFreteBase(ABC):
    @abstractmethod
    def calcular_frete(self, cep, peso, valor) -> tuple[float, int]:
        pass
```

> "Temos **3 implementações diferentes** desta interface:"

**[SLIDE 8: Três Implementações]**

```python
class FreteFixo(CalculadoraFreteBase):
    # R$ 15,00 - 7 dias
    
class FreteCorreios(CalculadoraFreteBase):
    # R$ 15-35 - 5-12 dias (varia por CEP)
    
class FreteExpresso(CalculadoraFreteBase):
    # R$ 30-60 - 2-5 dias (mais rápido)
```

> "O **polimorfismo** permite que usemos a **mesma interface** com **comportamentos diferentes**:"

```python
# Escolhe implementação em tempo de execução
if tipo_frete == 'Fixo':
    calculadora = FreteFixo()
elif tipo_frete == 'Correios':
    calculadora = FreteCorreios()
else:
    calculadora = FreteExpresso()

# MESMA CHAMADA, COMPORTAMENTO DIFERENTE!
valor, prazo = calculadora.calcular_frete(cep, peso, total)
```

> "Isso torna o código **extensível** - podemos adicionar novos tipos de frete sem modificar o código existente."

---

#### **3. ENCAPSULAMENTO** (45 segundos)

**[SLIDE 9: Encapsulamento]**

> "**ENCAPSULAMENTO** protege os dados e garante consistência:"

**[Mostrar código]**

```python
class CarrinhoController:
    def __init__(self):
        # Atributo PRIVADO
        self.itens: Dict[int, ItemCarrinho] = {}
    
    # Acesso CONTROLADO via métodos
    def adicionar_item(self, produto_id, nome, preco, quantidade):
        # VALIDAÇÃO antes de modificar
        if quantidade <= 0:
            return False, "Quantidade inválida"
        
        self.itens[produto_id] = ItemCarrinho(...)
        return True, "Item adicionado"
```

> "Os dados são acessados apenas através de métodos públicos que **validam** e **garantem consistência**."

---

#### **4. ABSTRAÇÃO** (45 segundos)

**[SLIDE 10: Abstração]**

> "**ABSTRAÇÃO** esconde complexidade e expõe apenas o necessário:"

**[Mostrar código]**

```python
from abc import ABC, abstractmethod

class GatewayPagamentoBase(ABC):
    @abstractmethod
    def processar_pagamento(self, valor, dados):
        pass
```

> "Classes abstratas **definem contratos** que as subclasses devem seguir:"

```python
class PagamentoCartao(GatewayPagamentoBase):
    def processar_pagamento(self, valor, dados):
        # Implementação específica para cartão
        
class PagamentoPix(GatewayPagamentoBase):
    def processar_pagamento(self, valor, dados):
        # Implementação específica para Pix
```

> "Isso garante que todas as implementações sigam a **mesma interface**."

---

### [5:30-7:30] DEMONSTRAÇÃO PRÁTICA (2 min)

**[SLIDE 11: Demo ao Vivo]**

> "Agora vou demonstrar o sistema funcionando:"

**[Abrir navegador - http://localhost:5000]**

#### **1. Página Inicial (15 seg)**

> "Esta é a página inicial com produtos em destaque. Note os **indicadores de estoque**."

**[Clicar em um produto]**

#### **2. Detalhes do Produto (15 seg)**

> "Aqui vemos detalhes, preço, estoque disponível e opção de adicionar ao carrinho."

**[Adicionar ao carrinho]**

#### **3. Carrinho (15 seg)**

> "O carrinho mostra os itens, quantidades e total calculado automaticamente."

**[Clicar em Finalizar Compra]**

#### **4. Checkout (45 seg)**

> "No checkout, temos:"

**[Mostrar cada seção]**

> "**1. Endereço de entrega** - selecionado de endereços cadastrados"

> "**2. Tipo de frete** - aqui está o **POLIMORFISMO em ação**!"

**[Apontar para as 3 opções]**

> - "Frete Fixo: R$ 15, 7 dias"
> - "Correios: varia por CEP, 5-12 dias"
> - "Expresso: mais caro, 2-5 dias"

> "Cada opção usa uma **classe diferente**, mas a **interface é a mesma**."

> "**3. Método de pagamento** - Cartão, Pix ou Boleto"

**[Selecionar opções e finalizar]**

#### **5. Confirmação (15 seg)**

> "Pedido criado! O sistema:"
> - Calculou o frete automaticamente
> - Atualizou o estoque
> - Criou o pedido no banco
> - Limpou o carrinho

**[Ir para Minha Conta]**

> "Aqui vemos o pedido com todas as informações de frete."

---

### [7:30-9:30] FUNCIONALIDADES PRINCIPAIS (2 min)

**[SLIDE 12: Funcionalidades]**

> "O sistema possui funcionalidades completas:"

#### **1. Autenticação (20 seg)**

> "**Autenticação segura:**"
> - Registro com validação de CPF (dígitos verificadores)
> - Senha forte obrigatória
> - Hash com Argon2 (algoritmo vencedor de competição)
> - Sessões separadas para cliente e admin

#### **2. Controle de Estoque (20 seg)**

> "**Controle de estoque automático:**"
> - Produtos sem estoque não podem ser comprados
> - Validação ao adicionar ao carrinho
> - Atualização automática ao criar pedido
> - Devolução ao cancelar pedido
> - Indicadores visuais em todo o site

#### **3. Sistema de Pedidos (30 seg)**

> "**Gestão completa de pedidos:**"
> - 5 status: Pendente, Processando, Enviado, Entregue, Cancelado
> - Cliente pode cancelar pedidos Pendentes ou Processando
> - Estoque é devolvido automaticamente
> - Admin pode atualizar status
> - Histórico completo

#### **4. Área Administrativa (30 seg)**

**[Mostrar área admin rapidamente]**

> "**Área administrativa completa:**"
> - Dashboard com estatísticas
> - CRUD de produtos com upload de imagens
> - CRUD de categorias
> - Visualização de clientes
> - Gestão de pedidos
> - Atualização de status

#### **5. Arquitetura (20 seg)**

**[SLIDE 13: Estatísticas]**

> "**Números do projeto:**"
> - 3.500+ linhas de código
> - 28 arquivos Python
> - 15 templates HTML
> - 8 modelos de dados
> - 7 repositórios
> - 6 controllers
> - 2 classes abstratas
> - 5 implementações polimórficas

---

### [9:30-10:00] CONCLUSÃO (30 seg)

**[SLIDE 14: Conclusão]**

> "Em resumo, o SCEE demonstra:"

**[Apontar para cada item]**

> "✅ **HERANÇA** - BaseRepository, reutilização de código"

> "✅ **POLIMORFISMO** - Fretes e pagamentos com mesma interface, comportamentos diferentes"

> "✅ **ENCAPSULAMENTO** - Dados protegidos, acesso controlado"

> "✅ **ABSTRAÇÃO** - Classes abstratas, interfaces bem definidas"

**[SLIDE 15: Obrigado]**

> "O sistema está **completo**, **funcional** e demonstra de forma prática os conceitos de POO."

> "Todo o código está documentado e disponível. Obrigado!"

**[Abrir para perguntas]**

---

## 📊 SLIDES SUGERIDOS

### Slide 1: Título
```
SCEE - Sistema de Comércio Eletrônico
Demonstração Prática de POO

[Logo ou imagem do sistema]

Desenvolvido em Python com Flask
```

### Slide 2: O que é o SCEE?
```
O que é o SCEE?

✅ E-commerce completo
✅ Cadastro e autenticação
✅ Catálogo de produtos
✅ Carrinho de compras
✅ 3 opções de frete
✅ 3 métodos de pagamento
✅ Área administrativa

Tecnologias: Python, Flask, SQLAlchemy, SQLite
```

### Slide 3: Arquitetura MVC
```
Arquitetura MVC

[Diagrama com 3 camadas]

VIEW (Templates)
    ↓
CONTROLLER (Lógica)
    ↓
REPOSITORY (Dados)
    ↓
MODEL (Entidades)
    ↓
DATABASE (SQLite)
```

### Slide 4: Padrão Repository
```
Padrão Repository

BaseRepository (Genérico)
├── ClienteRepository
├── ProdutoRepository
├── PedidoRepository
├── CategoriaRepository
└── EnderecoRepository

✅ Abstrai acesso a dados
✅ CRUD reutilizável
✅ Facilita testes
```

### Slide 5: 4 Pilares da POO
```
4 Pilares da POO

1️⃣ HERANÇA
   Reutilização de código

2️⃣ POLIMORFISMO
   Mesma interface, comportamentos diferentes

3️⃣ ENCAPSULAMENTO
   Proteção de dados

4️⃣ ABSTRAÇÃO
   Esconder complexidade
```

### Slide 6: Herança
```
1️⃣ HERANÇA

BaseRepository (Genérico)
    ↓
ClienteRepository
    ↓
Herda: create, get_by_id, get_all, update, delete

✅ Evita duplicação
✅ Manutenção centralizada
```

### Slide 7: Polimorfismo - Interface
```
2️⃣ POLIMORFISMO

CalculadoraFreteBase (Abstrata)
    ↓
    ├── FreteFixo
    ├── FreteCorreios
    └── FreteExpresso

Mesma interface: calcular_frete()
Comportamentos diferentes!
```

### Slide 8: Polimorfismo - Implementações
```
Três Implementações de Frete

📦 FreteFixo
   R$ 15,00 - 7 dias

📮 FreteCorreios
   R$ 15-35 - 5-12 dias (varia por CEP)

⚡ FreteExpresso
   R$ 30-60 - 2-5 dias (mais rápido)

✅ Fácil adicionar novos tipos!
```

### Slide 9: Encapsulamento
```
3️⃣ ENCAPSULAMENTO

CarrinhoController
    ├── itens (PRIVADO)
    └── Métodos públicos:
        ├── adicionar_item()
        ├── remover_item()
        └── calcular_total()

✅ Dados protegidos
✅ Acesso controlado
✅ Validações garantidas
```

### Slide 10: Abstração
```
4️⃣ ABSTRAÇÃO

GatewayPagamentoBase (ABC)
    ↓
    ├── PagamentoCartao
    └── PagamentoPix

Classes abstratas definem CONTRATOS
Subclasses implementam detalhes

✅ Interface simples
✅ Complexidade escondida
```

### Slide 11: Demo ao Vivo
```
DEMONSTRAÇÃO PRÁTICA

[Screenshot do sistema]

Vamos ver o sistema funcionando!
```

### Slide 12: Funcionalidades
```
Funcionalidades Principais

🔒 Autenticação segura (Argon2)
📦 Controle de estoque automático
🚚 3 opções de frete (Polimorfismo)
💳 3 métodos de pagamento
📊 Gestão de pedidos
👤 Área administrativa
```

### Slide 13: Estatísticas
```
Números do Projeto

📝 3.500+ linhas de código
📄 28 arquivos Python
🎨 15 templates HTML
📦 8 modelos
🗄️ 7 repositórios
🎮 6 controllers
🔷 2 classes abstratas
⚡ 5 implementações polimórficas
```

### Slide 14: Conclusão
```
Conclusão

✅ HERANÇA - BaseRepository
✅ POLIMORFISMO - Fretes e Pagamentos
✅ ENCAPSULAMENTO - Controllers
✅ ABSTRAÇÃO - Classes ABC

Sistema completo e funcional!
Código limpo e documentado!
```

### Slide 15: Obrigado
```
Obrigado!

SCEE - Sistema de Comércio Eletrônico

Perguntas?

[Contato/Email]
```

---

## 🎯 DICAS PARA APRESENTAÇÃO

### Antes da Apresentação

1. ✅ **Testar o sistema** - Garantir que está funcionando
2. ✅ **Preparar dados** - Produtos cadastrados, categorias
3. ✅ **Limpar carrinho** - Começar com carrinho vazio
4. ✅ **Abrir abas** - Sistema, slides, código
5. ✅ **Ensaiar** - Praticar o tempo

### Durante a Apresentação

1. ✅ **Falar claramente** - Voz firme e pausada
2. ✅ **Apontar para tela** - Mostrar o que está falando
3. ✅ **Manter contato visual** - Olhar para audiência
4. ✅ **Controlar tempo** - Relógio visível
5. ✅ **Demonstrar confiança** - Você conhece o código!

### Possíveis Perguntas

**P: Por que usar Argon2 para hash?**
> R: Argon2 venceu a Password Hashing Competition e é resistente a ataques de GPU e força bruta.

**P: Por que SQLite e não MySQL/PostgreSQL?**
> R: SQLite é ideal para desenvolvimento e demonstração. Em produção, poderia usar PostgreSQL facilmente (SQLAlchemy abstrai o banco).

**P: Como adicionar um novo tipo de frete?**
> R: Basta criar uma nova classe que herda de `CalculadoraFreteBase` e implementa `calcular_frete()`. Não precisa modificar código existente!

**P: O sistema está pronto para produção?**
> R: É um projeto acadêmico demonstrando POO. Para produção, precisaria de: testes automatizados, deploy em servidor, HTTPS, integração real com gateways de pagamento, etc.

---

## ⏱️ CHECKLIST FINAL

- [ ] Sistema rodando (localhost:5000)
- [ ] Produtos cadastrados
- [ ] Admin funcionando
- [ ] Slides preparados
- [ ] Código aberto no editor
- [ ] Navegador com abas prontas
- [ ] Relógio/timer visível
- [ ] Água por perto
- [ ] Ensaiado pelo menos 2x

---

**Boa sorte na apresentação! 🚀**

**Você domina o código e os conceitos. Mostre isso com confiança!**
