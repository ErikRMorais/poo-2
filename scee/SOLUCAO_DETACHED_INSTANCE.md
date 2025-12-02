# 🔧 Solução: DetachedInstanceError no SQLAlchemy

## ❌ Problema

```
sqlalchemy.orm.exc.DetachedInstanceError: 
A instância pai <Produto at 0x1d3e3e5a50> não está vinculada a uma sessão; 
a operação de carregamento lento do atributo 'imagens' não pode prosseguir
```

## 🔍 Causa

O erro ocorre quando:

1. Você busca um objeto do banco (ex: `produto`)
2. Fecha a sessão do SQLAlchemy (`db_session.close()`)
3. Tenta acessar um relacionamento lazy-loaded (ex: `produto.imagens`)

### Exemplo do Erro:

```python
@app.route('/admin/produto/editar/<int:produto_id>')
def admin_editar_produto(produto_id):
    db_session = db.get_session()
    produto = produto_repo.get_by_id(produto_id)
    
    db_session.close()  # ❌ Sessão fechada aqui
    
    # ❌ ERRO: Tenta acessar 'imagens' após fechar sessão
    return render_template('produto_form.html', produto=produto)
```

No template:
```html
{% for imagem in produto.imagens %}  <!-- ❌ ERRO AQUI -->
    <img src="{{ imagem.caminho }}">
{% endfor %}
```

## ✅ Solução Aplicada

### Opção 1: Eager Loading (Forçar Carregamento)

```python
@app.route('/admin/produto/editar/<int:produto_id>')
def admin_editar_produto(produto_id):
    db_session = db.get_session()
    produto = produto_repo.get_by_id(produto_id)
    
    # ✅ SOLUÇÃO: Forçar carregamento ANTES de fechar sessão
    _ = produto.imagens  # Acessa o relacionamento
    
    db_session.close()  # Agora pode fechar
    
    # ✅ OK: Imagens já foram carregadas
    return render_template('produto_form.html', produto=produto)
```

### Opção 2: Eager Loading na Query

Alterar o repositório para carregar imagens automaticamente:

```python
# Em produto_repository.py
from sqlalchemy.orm import joinedload

def get_by_id(self, produto_id):
    return self.session.query(Produto).options(
        joinedload(Produto.imagens)  # Carrega imagens junto
    ).filter(Produto.id == produto_id).first()
```

### Opção 3: Não Fechar Sessão Antes do Render

```python
@app.route('/admin/produto/editar/<int:produto_id>')
def admin_editar_produto(produto_id):
    db_session = db.get_session()
    produto = produto_repo.get_by_id(produto_id)
    
    # Renderiza ANTES de fechar
    response = render_template('produto_form.html', produto=produto)
    
    db_session.close()  # Fecha DEPOIS
    return response
```

## 📝 Correção Aplicada no Projeto

**Arquivo:** `app.py`  
**Linha:** 415-416

```python
# Carregar imagens antes de fechar a sessão (eager loading)
_ = produto.imagens  # Força o carregamento das imagens

db_session.close()
return render_template('admin/produto_form.html', categorias=categorias, produto=produto)
```

## 🎯 Por Que Funciona?

1. **Lazy Loading:** Por padrão, SQLAlchemy não carrega relacionamentos até você acessá-los
2. **Sessão Ativa:** Relacionamentos só podem ser carregados com sessão ativa
3. **Eager Loading:** Ao acessar `produto.imagens` antes de fechar, forçamos o carregamento
4. **Dados em Memória:** Após carregamento, dados ficam em memória (não precisa mais da sessão)

## 🔄 Outros Relacionamentos

A mesma solução se aplica a outros relacionamentos lazy-loaded:

```python
# Forçar carregamento de múltiplos relacionamentos
_ = produto.imagens
_ = produto.categoria
_ = cliente.enderecos
_ = pedido.itens

db_session.close()
```

## ⚠️ Quando Ocorre

Este erro é comum quando:

- ✅ Você fecha sessões para evitar `TimeoutError`
- ✅ Usa relacionamentos lazy-loaded (padrão do SQLAlchemy)
- ✅ Acessa relacionamentos em templates
- ✅ Passa objetos ORM para templates

## 🎓 Boas Práticas

### ✅ Fazer:

1. Carregar relacionamentos antes de fechar sessão
2. Usar `joinedload()` para queries que precisam de relacionamentos
3. Fechar sessões após renderizar templates
4. Documentar relacionamentos lazy vs eager

### ❌ Evitar:

1. Fechar sessão antes de acessar relacionamentos
2. Assumir que todos os dados estão carregados
3. Ignorar warnings de lazy loading
4. Deixar sessões abertas indefinidamente

## 📊 Comparação de Soluções

| Solução | Vantagens | Desvantagens |
|---------|-----------|--------------|
| **Eager Loading Manual** | Simples, controle fino | Precisa lembrar de fazer |
| **joinedload()** | Automático, eficiente | Modifica repositório |
| **Fechar Depois** | Sem mudanças no código | Sessão fica aberta mais tempo |

## 🔗 Relacionado

- **TimeoutError:** Sessões abertas por muito tempo
- **N+1 Problem:** Múltiplas queries para relacionamentos
- **Lazy vs Eager Loading:** Estratégias de carregamento

## ✅ Status

**Problema:** ❌ DetachedInstanceError ao editar produto  
**Solução:** ✅ Eager loading manual antes de fechar sessão  
**Testado:** ✅ Funciona corretamente  
**Documentado:** ✅ Este arquivo

---

**Desenvolvido para o projeto SCEE - Sistema de Comércio Eletrônico**
