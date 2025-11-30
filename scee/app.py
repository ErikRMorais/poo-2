"""Aplicação principal Flask (View/Controller)."""

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from database import Database
from controllers.auth_controller import AuthController
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController
from controllers.carrinho_controller import CarrinhoController
from controllers.pedido_controller import PedidoController
from repositories.categoria_repository import CategoriaRepository
from argon2 import PasswordHasher

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = Database()
db.create_tables()

carrinhos = {}


def get_carrinho():
    """Obtém o carrinho da sessão atual."""
    session_id = session.get('session_id')
    if not session_id:
        session_id = os.urandom(16).hex()
        session['session_id'] = session_id
    
    if session_id not in carrinhos:
        carrinhos[session_id] = CarrinhoController()
    
    return carrinhos[session_id]


@app.route('/')
def index():
    """Página inicial."""
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    produtos, total, total_pages = produto_controller.listar_produtos(page=1, per_page=12)
    
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    
    return render_template('index.html', produtos=produtos, categorias=categorias, 
                         total_pages=total_pages, current_page=1)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de novo cliente."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf', '').replace('.', '').replace('-', '')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        db_session = db.get_session()
        auth_controller = AuthController(db_session)
        
        sucesso, mensagem, cliente = auth_controller.registrar_cliente(
            nome, email, cpf, senha, confirmar_senha
        )
        
        if sucesso:
            session['cliente_id'] = cliente.id
            session['cliente_nome'] = cliente.nome
            flash(mensagem, 'success')
            return redirect(url_for('minha_conta'))
        else:
            flash(mensagem, 'error')
    
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de cliente ou admin."""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo', 'cliente')
        
        db_session = db.get_session()
        auth_controller = AuthController(db_session)
        
        if tipo == 'admin':
            sucesso, mensagem, admin = auth_controller.login_admin(email, senha)
            if sucesso:
                session['admin_id'] = admin.id
                session['admin_nome'] = admin.nome
                flash(mensagem, 'success')
                return redirect(url_for('admin_dashboard'))
        else:
            sucesso, mensagem, cliente = auth_controller.login_cliente(email, senha)
            if sucesso:
                session['cliente_id'] = cliente.id
                session['cliente_nome'] = cliente.nome
                flash(mensagem, 'success')
                return redirect(url_for('minha_conta'))
        
        flash(mensagem, 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout."""
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('index'))


@app.route('/minha-conta')
def minha_conta():
    """Página da conta do cliente."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar sua conta', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    cliente_controller = ClienteController(db_session)
    enderecos = cliente_controller.listar_enderecos(session['cliente_id'])
    
    pedido_controller = PedidoController(db_session)
    pedidos = pedido_controller.listar_pedidos_cliente(session['cliente_id'])
    
    return render_template('minha_conta.html', enderecos=enderecos, pedidos=pedidos)


@app.route('/produtos')
def produtos():
    """Listagem de produtos."""
    page = request.args.get('page', 1, type=int)
    categoria_id = request.args.get('categoria', type=int)
    busca = request.args.get('q', '')
    min_preco = request.args.get('min_preco', type=float)
    max_preco = request.args.get('max_preco', type=float)
    
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    
    if busca:
        produtos_list = produto_controller.buscar_produtos(busca, page=page)
        total_pages = 1
    elif min_preco and max_preco:
        produtos_list = produto_controller.filtrar_por_preco(min_preco, max_preco, page=page)
        total_pages = 1
    elif categoria_id:
        produtos_list, total, total_pages = produto_controller.listar_por_categoria(categoria_id, page=page)
    else:
        produtos_list, total, total_pages = produto_controller.listar_produtos(page=page)
    
    return render_template('produtos.html', produtos=produtos_list, categorias=categorias,
                         total_pages=total_pages, current_page=page)


@app.route('/produto/<int:produto_id>')
def produto_detalhe(produto_id):
    """Detalhes de um produto."""
    db_session = db.get_session()
    from repositories.produto_repository import ProdutoRepository
    produto_repo = ProdutoRepository(db_session)
    produto = produto_repo.get_by_id(produto_id)
    
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produtos'))
    
    return render_template('produto_detalhe.html', produto=produto)


@app.route('/carrinho')
def carrinho():
    """Visualizar carrinho."""
    carrinho_obj = get_carrinho()
    itens = carrinho_obj.obter_itens()
    total = carrinho_obj.calcular_total()
    
    return render_template('carrinho.html', itens=itens, total=total)


@app.route('/carrinho/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    """Adicionar produto ao carrinho."""
    quantidade = request.form.get('quantidade', 1, type=int)
    
    db_session = db.get_session()
    from repositories.produto_repository import ProdutoRepository
    produto_repo = ProdutoRepository(db_session)
    produto = produto_repo.get_by_id(produto_id)
    
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('produtos'))
    
    if produto.estoque < quantidade:
        flash('Estoque insuficiente', 'error')
        return redirect(url_for('produto_detalhe', produto_id=produto_id))
    
    carrinho_obj = get_carrinho()
    sucesso, mensagem = carrinho_obj.adicionar_item(produto.id, produto.nome, produto.preco, quantidade)
    flash(mensagem, 'success' if sucesso else 'error')
    
    return redirect(url_for('carrinho'))


@app.route('/carrinho/remover/<int:produto_id>', methods=['POST'])
def remover_carrinho(produto_id):
    """Remover produto do carrinho."""
    carrinho_obj = get_carrinho()
    sucesso, mensagem = carrinho_obj.remover_item(produto_id)
    flash(mensagem, 'success' if sucesso else 'error')
    
    return redirect(url_for('carrinho'))


@app.route('/carrinho/atualizar/<int:produto_id>', methods=['POST'])
def atualizar_carrinho(produto_id):
    """Atualizar quantidade no carrinho."""
    quantidade = request.form.get('quantidade', 1, type=int)
    
    carrinho_obj = get_carrinho()
    sucesso, mensagem = carrinho_obj.atualizar_quantidade(produto_id, quantidade)
    flash(mensagem, 'success' if sucesso else 'error')
    
    return redirect(url_for('carrinho'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Processo de checkout."""
    if 'cliente_id' not in session:
        flash('Faça login para finalizar a compra', 'error')
        return redirect(url_for('login'))
    
    carrinho_obj = get_carrinho()
    if carrinho_obj.quantidade_itens() == 0:
        flash('Carrinho vazio', 'error')
        return redirect(url_for('produtos'))
    
    db_session = db.get_session()
    cliente_controller = ClienteController(db_session)
    enderecos = cliente_controller.listar_enderecos(session['cliente_id'])
    
    if request.method == 'POST':
        endereco_id = request.form.get('endereco_id', type=int)
        metodo_pagamento = request.form.get('metodo_pagamento')
        
        pedido_controller = PedidoController(db_session)
        itens = carrinho_obj.obter_itens()
        
        sucesso, mensagem, pedido = pedido_controller.criar_pedido(
            session['cliente_id'], itens, endereco_id, metodo_pagamento
        )
        
        if sucesso:
            carrinho_obj.limpar()
            flash(f'Pedido #{pedido.id} criado com sucesso!', 'success')
            return redirect(url_for('minha_conta'))
        else:
            flash(mensagem, 'error')
    
    itens = carrinho_obj.obter_itens()
    total = carrinho_obj.calcular_total()
    
    return render_template('checkout.html', enderecos=enderecos, itens=itens, total=total)


@app.route('/admin')
def admin_dashboard():
    """Dashboard do administrador."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/dashboard.html')


@app.route('/admin/produtos')
def admin_produtos():
    """Gerenciamento de produtos (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    produtos_list, total, total_pages = produto_controller.listar_produtos(page=page)
    
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    
    return render_template('admin/produtos.html', produtos=produtos_list, categorias=categorias,
                         total_pages=total_pages, current_page=page)


@app.route('/admin/produto/criar', methods=['GET', 'POST'])
def admin_criar_produto():
    """Criar novo produto (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        sku = request.form.get('sku')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco', type=float)
        estoque = request.form.get('estoque', type=int)
        categoria_id = request.form.get('categoria_id', type=int)
        
        imagens = request.files.getlist('imagens')
        
        produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
        sucesso, mensagem, produto = produto_controller.criar_produto(
            nome, sku, descricao, preco, estoque, categoria_id, imagens
        )
        
        flash(mensagem, 'success' if sucesso else 'error')
        if sucesso:
            return redirect(url_for('admin_produtos'))
    
    return render_template('admin/produto_form.html', categorias=categorias, produto=None)


@app.route('/admin/produto/editar/<int:produto_id>', methods=['GET', 'POST'])
def admin_editar_produto(produto_id):
    """Editar produto (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.produto_repository import ProdutoRepository
    produto_repo = ProdutoRepository(db_session)
    produto = produto_repo.get_by_id(produto_id)
    
    if not produto:
        flash('Produto não encontrado', 'error')
        return redirect(url_for('admin_produtos'))
    
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco', type=float)
        estoque = request.form.get('estoque', type=int)
        categoria_id = request.form.get('categoria_id', type=int)
        
        produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
        sucesso, mensagem = produto_controller.atualizar_produto(
            produto_id, nome, descricao, preco, estoque, categoria_id
        )
        
        flash(mensagem, 'success' if sucesso else 'error')
        if sucesso:
            return redirect(url_for('admin_produtos'))
    
    return render_template('admin/produto_form.html', categorias=categorias, produto=produto)


@app.route('/admin/produto/deletar/<int:produto_id>', methods=['POST'])
def admin_deletar_produto(produto_id):
    """Deletar produto (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    sucesso, mensagem = produto_controller.remover_produto(produto_id)
    
    flash(mensagem, 'success' if sucesso else 'error')
    return redirect(url_for('admin_produtos'))


@app.route('/admin/pedidos')
def admin_pedidos():
    """Gerenciamento de pedidos (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    db_session = db.get_session()
    pedido_controller = PedidoController(db_session)
    
    if status:
        pedidos_list, total, total_pages = pedido_controller.filtrar_por_status(status, page=page)
    else:
        pedidos_list, total, total_pages = pedido_controller.listar_todos_pedidos(page=page)
    
    return render_template('admin/pedidos.html', pedidos=pedidos_list,
                         total_pages=total_pages, current_page=page, status_filtro=status)


@app.route('/admin/pedido/<int:pedido_id>/status', methods=['POST'])
def admin_atualizar_status_pedido(pedido_id):
    """Atualizar status do pedido (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    novo_status = request.form.get('status')
    
    db_session = db.get_session()
    pedido_controller = PedidoController(db_session)
    sucesso, mensagem = pedido_controller.atualizar_status(pedido_id, novo_status)
    
    flash(mensagem, 'success' if sucesso else 'error')
    return redirect(url_for('admin_pedidos'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
