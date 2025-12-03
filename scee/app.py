"""Aplicação principal Flask (View/Controller)."""

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import Database
from controllers.auth_controller import AuthController
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController
from controllers.carrinho_controller import CarrinhoController
from controllers.pedido_controller import PedidoController
from repositories.categoria_repository import CategoriaRepository

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
    
    # Carregar relacionamentos antes de fechar sessão
    for produto in produtos:
        _ = produto.categoria
        _ = produto.imagens
    
    db_session.close()
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
    from repositories.cliente_repository import ClienteRepository
    cliente_repo = ClienteRepository(db_session)
    cliente = cliente_repo.get_by_id(session['cliente_id'])
    
    cliente_controller = ClienteController(db_session)
    enderecos = cliente_controller.listar_enderecos(session['cliente_id'])
    
    pedido_controller = PedidoController(db_session)
    pedidos = pedido_controller.listar_pedidos_cliente(session['cliente_id'])
    
    return render_template('minha_conta.html', cliente=cliente, enderecos=enderecos, pedidos=pedidos)


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
    
    # Aplicar filtros combinados
    if busca:
        produtos_list = produto_controller.buscar_produtos(busca, page=page)
        total_pages = 1
    elif categoria_id and (min_preco is not None and max_preco is not None):
        # Filtro combinado: categoria + preço
        produtos_list = produto_controller.filtrar_por_categoria_e_preco(
            categoria_id, min_preco, max_preco, page=page
        )
        total_pages = 1
    elif min_preco is not None and max_preco is not None:
        # Apenas filtro de preço
        produtos_list = produto_controller.filtrar_por_preco(min_preco, max_preco, page=page)
        total_pages = 1
    elif categoria_id:
        # Apenas filtro de categoria
        produtos_list, total, total_pages = produto_controller.listar_por_categoria(categoria_id, page=page)
    else:
        # Sem filtros
        produtos_list, total, total_pages = produto_controller.listar_produtos(page=page)
    
    # Carregar categorias de todos os produtos antes de fechar sessão
    for produto in produtos_list:
        _ = produto.categoria
        _ = produto.imagens
    
    db_session.close()
    return render_template('produtos.html', produtos=produtos_list, categorias=categorias,
                         total_pages=total_pages, current_page=page, 
                         categoria_selecionada=categoria_id, min_preco=min_preco, max_preco=max_preco)


@app.route('/produto/<int:produto_id>')
def produto_detalhe(produto_id):
    """Detalhes de um produto."""
    db_session = db.get_session()
    from repositories.produto_repository import ProdutoRepository
    produto_repo = ProdutoRepository(db_session)
    produto = produto_repo.get_by_id(produto_id)
    
    if not produto:
        flash('Produto não encontrado', 'error')
        db_session.close()
        return redirect(url_for('produtos'))
    
    # Carregar relacionamentos antes de fechar a sessão (eager loading)
    _ = produto.imagens  # Força carregamento das imagens
    _ = produto.categoria  # Força carregamento da categoria
    
    db_session.close()
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
        db_session.close()
        return redirect(url_for('produtos'))
    
    if produto.estoque == 0:
        flash('❌ Este produto está SEM ESTOQUE e não pode ser adicionado ao carrinho', 'error')
        db_session.close()
        return redirect(url_for('produto_detalhe', produto_id=produto_id))
    
    if produto.estoque < quantidade:
        flash(f'❌ Estoque insuficiente! Disponível: {produto.estoque} unidades', 'error')
        db_session.close()
        return redirect(url_for('produto_detalhe', produto_id=produto_id))
    
    carrinho_obj = get_carrinho()
    sucesso, mensagem = carrinho_obj.adicionar_item(produto.id, produto.nome, produto.preco, quantidade)
    flash(mensagem, 'success' if sucesso else 'error')
    db_session.close()
    
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
        tipo_frete = request.form.get('tipo_frete', 'Fixo')
        
        pedido_controller = PedidoController(db_session)
        itens = carrinho_obj.obter_itens()
        
        sucesso, mensagem, pedido = pedido_controller.criar_pedido(
            cliente_id=session['cliente_id'],
            itens_carrinho=itens,
            endereco_id=endereco_id,
            metodo_pagamento=metodo_pagamento,
            tipo_frete=tipo_frete
        )
        
        if sucesso:
            carrinho_obj.limpar()
            flash(f'✅ Pedido #{pedido.id} criado com sucesso! Frete: {tipo_frete}', 'success')
            db_session.close()
            return redirect(url_for('minha_conta'))
        else:
            flash(mensagem, 'error')
            db_session.close()
    
    itens = carrinho_obj.obter_itens()
    total = carrinho_obj.calcular_total()
    db_session.close()
    
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
    
    # Carregar categorias antes de fechar sessão
    for produto in produtos_list:
        _ = produto.categoria
    
    db_session.close()
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
        
        # Capturar novas imagens
        novas_imagens = request.files.getlist('novas_imagens')
        novas_imagens = [img for img in novas_imagens if img.filename]
        
        produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
        sucesso, mensagem = produto_controller.atualizar_produto(
            produto_id, nome, descricao, preco, estoque, categoria_id, novas_imagens
        )
        
        flash(mensagem, 'success' if sucesso else 'error')
        db_session.close()
        if sucesso:
            return redirect(url_for('admin_produtos'))
        return redirect(url_for('admin_editar_produto', produto_id=produto_id))
    
    # Carregar imagens antes de fechar a sessão (eager loading)
    _ = produto.imagens  # Força o carregamento das imagens
    
    db_session.close()
    return render_template('admin/produto_form.html', categorias=categorias, produto=produto)


@app.route('/admin/produto/imagem/remover/<int:imagem_id>', methods=['POST'])
def admin_remover_imagem(imagem_id):
    """Remover imagem de produto (admin)."""
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Acesso negado'}), 403
    
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    sucesso, mensagem = produto_controller.remover_imagem(imagem_id)
    db_session.close()
    
    return jsonify({'success': sucesso, 'message': mensagem})


@app.route('/admin/produto/deletar/<int:produto_id>', methods=['POST'])
def admin_deletar_produto(produto_id):
    """Deletar produto (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    produto_controller = ProdutoController(db_session, app.config['UPLOAD_FOLDER'])
    sucesso, mensagem = produto_controller.remover_produto(produto_id)
    db_session.close()
    
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


# ==================== ROTAS DE EDIÇÃO DE PERFIL ====================

@app.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    """Editar dados do cliente."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar esta página', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.cliente_repository import ClienteRepository
    cliente_repo = ClienteRepository(db_session)
    cliente = cliente_repo.get_by_id(session['cliente_id'])
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        
        # Validar e-mail único (exceto o próprio)
        cliente_existente = cliente_repo.get_by_email(email)
        if cliente_existente and cliente_existente.id != cliente.id:
            flash('E-mail já cadastrado por outro usuário', 'error')
            return render_template('editar_perfil.html', cliente=cliente)
        
        cliente.nome = nome
        cliente.email = email
        
        try:
            cliente_repo.update(cliente)
            session['cliente_nome'] = nome
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('minha_conta'))
        except Exception as e:
            flash(f'Erro ao atualizar perfil: {str(e)}', 'error')
    
    return render_template('editar_perfil.html', cliente=cliente)


@app.route('/perfil/alterar-senha', methods=['GET', 'POST'])
def alterar_senha():
    """Alterar senha do cliente."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar esta página', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        db_session = db.get_session()
        from repositories.cliente_repository import ClienteRepository
        cliente_repo = ClienteRepository(db_session)
        cliente = cliente_repo.get_by_id(session['cliente_id'])
        
        # Verificar senha atual
        ph = PasswordHasher()
        try:
            ph.verify(cliente.senha_hash, senha_atual)
        except:
            flash('Senha atual incorreta', 'error')
            return render_template('alterar_senha.html')
        
        # Validar nova senha
        if nova_senha != confirmar_senha:
            flash('As senhas não coincidem', 'error')
            return render_template('alterar_senha.html')
        
        if len(nova_senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres', 'error')
            return render_template('alterar_senha.html')
        
        # Atualizar senha
        cliente.senha_hash = ph.hash(nova_senha)
        cliente_repo.update(cliente)
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('minha_conta'))
    
    return render_template('alterar_senha.html')


# ==================== ROTAS DE ENDEREÇOS ====================

@app.route('/endereco/adicionar', methods=['GET', 'POST'])
def adicionar_endereco():
    """Adicionar novo endereço."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar esta página', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        cep = request.form.get('cep', '').replace('-', '').replace('.', '')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        complemento = request.form.get('complemento', '')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        
        db_session = db.get_session()
        cliente_controller = ClienteController(db_session)
        
        sucesso, mensagem, endereco = cliente_controller.adicionar_endereco(
            session['cliente_id'], rua, numero, complemento, bairro, cidade, estado, cep
        )
        
        flash(mensagem, 'success' if sucesso else 'error')
        if sucesso:
            return redirect(url_for('minha_conta'))
    
    return render_template('endereco_form.html', endereco=None)


@app.route('/endereco/editar/<int:endereco_id>', methods=['GET', 'POST'])
def editar_endereco(endereco_id):
    """Editar endereço existente."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar esta página', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.endereco_repository import EnderecoRepository
    endereco_repo = EnderecoRepository(db_session)
    endereco = endereco_repo.get_by_id(endereco_id)
    
    if not endereco or endereco.cliente_id != session['cliente_id']:
        flash('Endereço não encontrado', 'error')
        return redirect(url_for('minha_conta'))
    
    if request.method == 'POST':
        endereco.cep = request.form.get('cep', '').replace('-', '').replace('.', '')
        endereco.rua = request.form.get('rua')
        endereco.numero = request.form.get('numero')
        endereco.complemento = request.form.get('complemento', '')
        endereco.bairro = request.form.get('bairro')
        endereco.cidade = request.form.get('cidade')
        endereco.estado = request.form.get('estado')
        
        try:
            endereco_repo.update(endereco)
            flash('Endereço atualizado com sucesso!', 'success')
            return redirect(url_for('minha_conta'))
        except Exception as e:
            flash(f'Erro ao atualizar endereço: {str(e)}', 'error')
    
    return render_template('endereco_form.html', endereco=endereco)


@app.route('/endereco/deletar/<int:endereco_id>', methods=['POST'])
def deletar_endereco(endereco_id):
    """Deletar endereço."""
    if 'cliente_id' not in session:
        flash('Faça login para acessar esta página', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.endereco_repository import EnderecoRepository
    endereco_repo = EnderecoRepository(db_session)
    endereco = endereco_repo.get_by_id(endereco_id)
    
    if not endereco or endereco.cliente_id != session['cliente_id']:
        flash('Endereço não encontrado', 'error')
        db_session.close()
        return redirect(url_for('minha_conta'))
    
    try:
        endereco_repo.delete(endereco)
        flash('Endereço removido com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao remover endereço: {str(e)}', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for('minha_conta'))


# ==================== ROTAS ADMIN - CATEGORIAS ====================

@app.route('/admin/categorias')
def admin_categorias():
    """Gerenciamento de categorias (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    categoria_repo = CategoriaRepository(db_session)
    categorias = categoria_repo.get_all()
    db_session.close()
    
    return render_template('admin/categorias.html', categorias=categorias)


@app.route('/admin/categoria/criar', methods=['GET', 'POST'])
def admin_criar_categoria():
    """Criar nova categoria (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        
        db_session = db.get_session()
        categoria_repo = CategoriaRepository(db_session)
        
        # Verificar se já existe
        if categoria_repo.get_by_nome(nome):
            flash('Categoria já existe', 'error')
            return render_template('admin/categoria_form.html', categoria=None)
        
        from models.categoria import Categoria
        nova_categoria = Categoria(nome=nome)
        
        try:
            categoria_repo.create(nova_categoria)
            flash('Categoria criada com sucesso!', 'success')
            db_session.close()
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            flash(f'Erro ao criar categoria: {str(e)}', 'error')
        finally:
            db_session.close()
    
    return render_template('admin/categoria_form.html', categoria=None)


@app.route('/admin/categoria/editar/<int:categoria_id>', methods=['GET', 'POST'])
def admin_editar_categoria(categoria_id):
    """Editar categoria (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    categoria_repo = CategoriaRepository(db_session)
    categoria = categoria_repo.get_by_id(categoria_id)
    
    if not categoria:
        flash('Categoria não encontrada', 'error')
        db_session.close()
        return redirect(url_for('admin_categorias'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        
        # Verificar se já existe (exceto a própria)
        categoria_existente = categoria_repo.get_by_nome(nome)
        if categoria_existente and categoria_existente.id != categoria_id:
            flash('Já existe uma categoria com este nome', 'error')
            db_session.close()
            return render_template('admin/categoria_form.html', categoria=categoria)
        
        categoria.nome = nome
        
        try:
            categoria_repo.update(categoria)
            flash('Categoria atualizada com sucesso!', 'success')
            db_session.close()
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
        finally:
            db_session.close()
            return render_template('admin/categoria_form.html', categoria=categoria)
    
    # GET request
    result = render_template('admin/categoria_form.html', categoria=categoria)
    db_session.close()
    return result


@app.route('/admin/categoria/deletar/<int:categoria_id>', methods=['POST'])
def admin_deletar_categoria(categoria_id):
    """Deletar categoria (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    categoria_repo = CategoriaRepository(db_session)
    
    try:
        categoria = categoria_repo.get_by_id(categoria_id)
        if not categoria:
            flash('Categoria não encontrada', 'error')
        else:
            categoria_repo.delete(categoria)
            flash('Categoria removida com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao remover categoria: {str(e)}', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for('admin_categorias'))


# ==================== ROTAS ADMIN - CLIENTES ====================

@app.route('/admin/clientes')
def admin_clientes():
    """Gerenciamento de clientes (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.cliente_repository import ClienteRepository
    cliente_repo = ClienteRepository(db_session)
    clientes = cliente_repo.get_all()
    
    return render_template('admin/clientes.html', clientes=clientes)


@app.route('/admin/cliente/<int:cliente_id>')
def admin_cliente_detalhes(cliente_id):
    """Ver detalhes de um cliente (admin)."""
    if 'admin_id' not in session:
        flash('Acesso negado', 'error')
        return redirect(url_for('login'))
    
    db_session = db.get_session()
    from repositories.cliente_repository import ClienteRepository
    from repositories.endereco_repository import EnderecoRepository
    from repositories.pedido_repository import PedidoRepository
    
    cliente_repo = ClienteRepository(db_session)
    endereco_repo = EnderecoRepository(db_session)
    pedido_repo = PedidoRepository(db_session)
    
    cliente = cliente_repo.get_by_id(cliente_id)
    if not cliente:
        flash('Cliente não encontrado', 'error')
        return redirect(url_for('admin_clientes'))
    
    enderecos = endereco_repo.get_by_cliente(cliente_id)
    pedidos = pedido_repo.get_by_cliente(cliente_id)
    
    total_gasto = sum(p.total for p in pedidos)
    
    return render_template('admin/cliente_detalhes.html', 
                         cliente=cliente, 
                         enderecos=enderecos, 
                         pedidos=pedidos,
                         total_gasto=total_gasto)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
