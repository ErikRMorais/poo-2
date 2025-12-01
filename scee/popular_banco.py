"""Script para popular o banco de dados com categorias e produtos."""

from database import Database
from models.categoria import Categoria
from models.produto import Produto
from models.imagem_produto import ImagemProduto

def criar_categorias():
    """Cria categorias de produtos."""
    
    print("\n" + "=" * 60)
    print("📁 CRIANDO CATEGORIAS")
    print("=" * 60)
    
    db = Database()
    session = db.get_session()
    
    categorias_data = [
        "Eletrônicos",
        "Roupas",
        "Livros",
        "Casa e Decoração",
        "Esportes",
        "Beleza",
        "Alimentos",
        "Brinquedos",
    ]
    
    categorias_criadas = []
    
    for nome_categoria in categorias_data:
        # Verificar se já existe
        categoria_existente = session.query(Categoria).filter_by(nome=nome_categoria).first()
        
        if categoria_existente:
            print(f"⚠️  Categoria '{nome_categoria}' já existe (ID: {categoria_existente.id})")
            categorias_criadas.append(categoria_existente)
        else:
            categoria = Categoria(nome=nome_categoria)
            session.add(categoria)
            session.flush()
            categorias_criadas.append(categoria)
            print(f"✅ Categoria criada: {nome_categoria} (ID: {categoria.id})")
    
    session.commit()
    print(f"\n✅ Total de categorias: {len(categorias_criadas)}")
    session.close()
    
    return categorias_criadas

def criar_produtos():
    """Cria produtos de exemplo."""
    
    print("\n" + "=" * 60)
    print("📦 CRIANDO PRODUTOS")
    print("=" * 60)
    
    db = Database()
    session = db.get_session()
    
    # Buscar categorias
    categorias = session.query(Categoria).all()
    
    if not categorias:
        print("❌ Nenhuma categoria encontrada! Execute criar_categorias() primeiro.")
        session.close()
        return
    
    # Criar dicionário de categorias por nome
    cat_dict = {cat.nome: cat for cat in categorias}
    
    produtos_data = [
        # Eletrônicos
        {
            "nome": "Notebook Dell Inspiron 15",
            "descricao": "Notebook com processador Intel Core i5, 8GB RAM, 256GB SSD, tela 15.6 polegadas Full HD",
            "preco": 3299.90,
            "estoque": 15,
            "categoria": "Eletrônicos"
        },
        {
            "nome": "Smartphone Samsung Galaxy A54",
            "descricao": "Smartphone 5G, 128GB, câmera tripla 50MP, tela Super AMOLED 6.4 polegadas",
            "preco": 1899.00,
            "estoque": 25,
            "categoria": "Eletrônicos"
        },
        {
            "nome": "Fone de Ouvido Bluetooth JBL",
            "descricao": "Fone over-ear com cancelamento de ruído, bateria 30h, som premium",
            "preco": 299.90,
            "estoque": 40,
            "categoria": "Eletrônicos"
        },
        {
            "nome": "Smart TV LG 50 polegadas 4K",
            "descricao": "TV LED 4K UHD, WebOS, HDR, ThinQ AI, 3 HDMI, 2 USB",
            "preco": 2199.00,
            "estoque": 10,
            "categoria": "Eletrônicos"
        },
        {
            "nome": "Mouse Gamer Logitech G502",
            "descricao": "Mouse óptico RGB, 11 botões programáveis, sensor HERO 25K, peso ajustável",
            "preco": 249.90,
            "estoque": 30,
            "categoria": "Eletrônicos"
        },
        
        # Roupas
        {
            "nome": "Camiseta Básica Algodão",
            "descricao": "Camiseta 100% algodão, gola redonda, disponível em várias cores",
            "preco": 49.90,
            "estoque": 100,
            "categoria": "Roupas"
        },
        {
            "nome": "Calça Jeans Masculina",
            "descricao": "Calça jeans tradicional, corte reto, 98% algodão 2% elastano",
            "preco": 129.90,
            "estoque": 50,
            "categoria": "Roupas"
        },
        {
            "nome": "Jaqueta Corta-Vento",
            "descricao": "Jaqueta impermeável, capuz ajustável, bolsos laterais",
            "preco": 189.90,
            "estoque": 35,
            "categoria": "Roupas"
        },
        {
            "nome": "Tênis Esportivo Nike",
            "descricao": "Tênis para corrida, tecnologia Air, solado antiderrapante",
            "preco": 399.90,
            "estoque": 45,
            "categoria": "Roupas"
        },
        
        # Livros
        {
            "nome": "Clean Code - Robert Martin",
            "descricao": "Guia completo sobre boas práticas de programação e código limpo",
            "preco": 89.90,
            "estoque": 20,
            "categoria": "Livros"
        },
        {
            "nome": "O Senhor dos Anéis - Coleção",
            "descricao": "Box com os 3 livros da trilogia de J.R.R. Tolkien",
            "preco": 149.90,
            "estoque": 15,
            "categoria": "Livros"
        },
        {
            "nome": "1984 - George Orwell",
            "descricao": "Clássico da literatura distópica, edição especial",
            "preco": 39.90,
            "estoque": 30,
            "categoria": "Livros"
        },
        
        # Casa e Decoração
        {
            "nome": "Jogo de Panelas Antiaderente 5 Peças",
            "descricao": "Panelas com revestimento antiaderente, cabos ergonômicos",
            "preco": 259.90,
            "estoque": 25,
            "categoria": "Casa e Decoração"
        },
        {
            "nome": "Luminária LED de Mesa",
            "descricao": "Luminária articulada, 3 níveis de intensidade, USB",
            "preco": 79.90,
            "estoque": 40,
            "categoria": "Casa e Decoração"
        },
        {
            "nome": "Tapete Decorativo 2x1.5m",
            "descricao": "Tapete felpudo, antialérgico, fácil limpeza",
            "preco": 199.90,
            "estoque": 20,
            "categoria": "Casa e Decoração"
        },
        
        # Esportes
        {
            "nome": "Bola de Futebol Profissional",
            "descricao": "Bola oficial, costurada à mão, tamanho padrão FIFA",
            "preco": 129.90,
            "estoque": 35,
            "categoria": "Esportes"
        },
        {
            "nome": "Halteres 5kg (Par)",
            "descricao": "Par de halteres emborrachados, pegada antiderrapante",
            "preco": 89.90,
            "estoque": 50,
            "categoria": "Esportes"
        },
        {
            "nome": "Tapete de Yoga Premium",
            "descricao": "Tapete antiderrapante, 6mm espessura, com bolsa",
            "preco": 119.90,
            "estoque": 30,
            "categoria": "Esportes"
        },
        
        # Beleza
        {
            "nome": "Kit Shampoo e Condicionador",
            "descricao": "Kit para todos os tipos de cabelo, sem parabenos",
            "preco": 69.90,
            "estoque": 60,
            "categoria": "Beleza"
        },
        {
            "nome": "Perfume Importado 100ml",
            "descricao": "Fragrância amadeirada, longa duração",
            "preco": 249.90,
            "estoque": 25,
            "categoria": "Beleza"
        },
        
        # Alimentos
        {
            "nome": "Café Gourmet Torrado 500g",
            "descricao": "Café especial, torra média, notas de chocolate",
            "preco": 34.90,
            "estoque": 80,
            "categoria": "Alimentos"
        },
        {
            "nome": "Chocolate Belga Premium 200g",
            "descricao": "Chocolate 70% cacau, importado da Bélgica",
            "preco": 29.90,
            "estoque": 100,
            "categoria": "Alimentos"
        },
        
        # Brinquedos
        {
            "nome": "LEGO Classic - Caixa Média",
            "descricao": "484 peças coloridas, manual de instruções incluído",
            "preco": 199.90,
            "estoque": 30,
            "categoria": "Brinquedos"
        },
        {
            "nome": "Boneca Barbie Profissões",
            "descricao": "Boneca com acessórios, roupas intercambiáveis",
            "preco": 89.90,
            "estoque": 45,
            "categoria": "Brinquedos"
        },
    ]
    
    produtos_criados = 0
    
    for prod_data in produtos_data:
        # Verificar se já existe
        produto_existente = session.query(Produto).filter_by(nome=prod_data["nome"]).first()
        
        if produto_existente:
            print(f"⚠️  Produto '{prod_data['nome']}' já existe")
            continue
        
        # Buscar categoria
        categoria = cat_dict.get(prod_data["categoria"])
        
        if not categoria:
            print(f"❌ Categoria '{prod_data['categoria']}' não encontrada para '{prod_data['nome']}'")
            continue
        
        # Gerar SKU único baseado no nome
        import re
        sku_base = re.sub(r'[^a-zA-Z0-9]', '', prod_data["nome"][:20].upper())
        sku = f"{sku_base}-{produtos_criados + 1:04d}"
        
        # Criar produto
        produto = Produto(
            nome=prod_data["nome"],
            sku=sku,
            descricao=prod_data["descricao"],
            preco=prod_data["preco"],
            estoque=prod_data["estoque"],
            categoria_id=categoria.id
        )
        
        session.add(produto)
        produtos_criados += 1
        print(f"✅ Produto criado: {prod_data['nome']} - R$ {prod_data['preco']:.2f}")
    
    session.commit()
    print(f"\n✅ Total de produtos criados: {produtos_criados}")
    session.close()

def popular_banco_completo():
    """Popula o banco com categorias e produtos."""
    
    print("\n" + "=" * 60)
    print("🚀 POPULANDO BANCO DE DADOS")
    print("=" * 60)
    
    # Criar categorias
    criar_categorias()
    
    # Criar produtos
    criar_produtos()
    
    print("\n" + "=" * 60)
    print("🎉 BANCO DE DADOS POPULADO COM SUCESSO!")
    print("=" * 60)
    print("\n📊 Resumo:")
    
    db = Database()
    session = db.get_session()
    
    total_categorias = session.query(Categoria).count()
    total_produtos = session.query(Produto).count()
    
    print(f"   📁 Categorias: {total_categorias}")
    print(f"   📦 Produtos: {total_produtos}")
    print("\n🌐 Acesse: http://localhost:5000")
    print("=" * 60)
    
    session.close()

if __name__ == '__main__':
    popular_banco_completo()
