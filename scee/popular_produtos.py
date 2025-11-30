"""Script para popular o banco de dados com produtos de exemplo."""

from database import Database
from models.produto import Produto
from models.categoria import Categoria
from repositories.categoria_repository import CategoriaRepository
from repositories.produto_repository import ProdutoRepository


def criar_produtos_exemplo():
    """Cria produtos de exemplo para testes."""
    
    # Inicializar banco
    db = Database()
    session = db.get_session()
    
    categoria_repo = CategoriaRepository(session)
    produto_repo = ProdutoRepository(session)
    
    print("🔄 Criando produtos de exemplo...\n")
    
    # Buscar categorias existentes
    categorias = {
        'Smartphones': categoria_repo.get_by_nome('Smartphones'),
        'Notebooks': categoria_repo.get_by_nome('Notebooks'),
        'Periféricos': categoria_repo.get_by_nome('Periféricos'),
        'Componentes': categoria_repo.get_by_nome('Componentes'),
        'Áudio': categoria_repo.get_by_nome('Áudio')
    }
    
    # Produtos de exemplo
    produtos_exemplo = [
        # Smartphones
        {
            'nome': 'iPhone 15 Pro Max',
            'sku': 'IPH15PROMAX256',
            'descricao': 'iPhone 15 Pro Max 256GB - Titânio Natural. Chip A17 Pro, câmera de 48MP, tela Super Retina XDR de 6.7", Dynamic Island, USB-C.',
            'preco': 8999.00,
            'estoque': 15,
            'categoria': 'Smartphones'
        },
        {
            'nome': 'Samsung Galaxy S24 Ultra',
            'sku': 'SAMS24ULTRA512',
            'descricao': 'Samsung Galaxy S24 Ultra 512GB - Preto. Snapdragon 8 Gen 3, câmera de 200MP, tela AMOLED de 6.8", S Pen integrada, bateria de 5000mAh.',
            'preco': 7499.00,
            'estoque': 20,
            'categoria': 'Smartphones'
        },
        {
            'nome': 'Xiaomi 14 Pro',
            'sku': 'XIAOMI14PRO256',
            'descricao': 'Xiaomi 14 Pro 256GB - Branco. Snapdragon 8 Gen 3, câmera Leica de 50MP, tela AMOLED de 6.73", carregamento rápido de 120W.',
            'preco': 4999.00,
            'estoque': 25,
            'categoria': 'Smartphones'
        },
        {
            'nome': 'Motorola Edge 40 Pro',
            'sku': 'MOTOEDGE40PRO',
            'descricao': 'Motorola Edge 40 Pro 256GB - Azul. Snapdragon 8 Gen 2, câmera de 50MP, tela OLED de 6.67" 165Hz, carregamento turbo de 125W.',
            'preco': 3299.00,
            'estoque': 30,
            'categoria': 'Smartphones'
        },
        
        # Notebooks
        {
            'nome': 'MacBook Pro 14" M3 Pro',
            'sku': 'MBPRO14M3PRO',
            'descricao': 'MacBook Pro 14" com chip M3 Pro, 18GB RAM, SSD 512GB. Tela Liquid Retina XDR, até 18h de bateria, 3 portas Thunderbolt 4.',
            'preco': 16999.00,
            'estoque': 8,
            'categoria': 'Notebooks'
        },
        {
            'nome': 'Dell XPS 15',
            'sku': 'DELLXPS15I9',
            'descricao': 'Dell XPS 15 - Intel Core i9-13900H, 32GB RAM, SSD 1TB, RTX 4060 8GB, tela OLED 3.5K touch, Windows 11 Pro.',
            'preco': 12999.00,
            'estoque': 10,
            'categoria': 'Notebooks'
        },
        {
            'nome': 'Lenovo Legion 5 Pro',
            'sku': 'LEGION5PRORTX',
            'descricao': 'Lenovo Legion 5 Pro - AMD Ryzen 7 7745HX, 16GB RAM, SSD 512GB, RTX 4070 8GB, tela 16" WQXGA 240Hz, RGB.',
            'preco': 8999.00,
            'estoque': 12,
            'categoria': 'Notebooks'
        },
        {
            'nome': 'ASUS VivoBook 15',
            'sku': 'VIVOBOOK15I5',
            'descricao': 'ASUS VivoBook 15 - Intel Core i5-1235U, 8GB RAM, SSD 256GB, Intel Iris Xe, tela 15.6" Full HD, Windows 11.',
            'preco': 3299.00,
            'estoque': 25,
            'categoria': 'Notebooks'
        },
        
        # Periféricos
        {
            'nome': 'Mouse Logitech MX Master 3S',
            'sku': 'LOGIMXMASTER3S',
            'descricao': 'Mouse sem fio Logitech MX Master 3S - 8000 DPI, sensor Darkfield, 7 botões programáveis, bateria de 70 dias, USB-C.',
            'preco': 599.00,
            'estoque': 40,
            'categoria': 'Periféricos'
        },
        {
            'nome': 'Teclado Mecânico Keychron K8 Pro',
            'sku': 'KEYCHK8PROBROWN',
            'descricao': 'Teclado mecânico Keychron K8 Pro - Switch Brown, hot-swappable, RGB, conexão sem fio/USB-C, layout TKL, bateria 4000mAh.',
            'preco': 899.00,
            'estoque': 30,
            'categoria': 'Periféricos'
        },
        {
            'nome': 'Webcam Logitech Brio 4K',
            'sku': 'LOGIBRIO4K',
            'descricao': 'Webcam Logitech Brio 4K - Resolução 4K Ultra HD, HDR, campo de visão ajustável, microfone com redução de ruído, USB 3.0.',
            'preco': 1299.00,
            'estoque': 20,
            'categoria': 'Periféricos'
        },
        {
            'nome': 'Monitor LG UltraGear 27" 144Hz',
            'sku': 'LG27GL850144HZ',
            'descricao': 'Monitor Gamer LG UltraGear 27" - Nano IPS QHD 2560x1440, 144Hz, 1ms, HDR10, FreeSync Premium, altura ajustável.',
            'preco': 2199.00,
            'estoque': 15,
            'categoria': 'Periféricos'
        },
        
        # Componentes
        {
            'nome': 'SSD Kingston NV2 1TB',
            'sku': 'KINGSTONNV21TB',
            'descricao': 'SSD Kingston NV2 1TB - NVMe PCIe 4.0, leitura 3500MB/s, gravação 2100MB/s, formato M.2 2280.',
            'preco': 449.00,
            'estoque': 50,
            'categoria': 'Componentes'
        },
        {
            'nome': 'Memória RAM Corsair Vengeance 32GB',
            'sku': 'CORSAIRV32GB',
            'descricao': 'Memória RAM Corsair Vengeance DDR5 32GB (2x16GB) - 5600MHz, CL36, RGB, compatível Intel 12ª/13ª/14ª gen e AMD Ryzen 7000.',
            'preco': 899.00,
            'estoque': 35,
            'categoria': 'Componentes'
        },
        {
            'nome': 'Placa de Vídeo RTX 4070 Ti',
            'sku': 'RTX4070TISUPER',
            'descricao': 'NVIDIA GeForce RTX 4070 Ti Super 16GB - GDDR6X, DLSS 3, Ray Tracing, 3 ventoinhas, RGB, 8K ready.',
            'preco': 5999.00,
            'estoque': 8,
            'categoria': 'Componentes'
        },
        {
            'nome': 'Processador AMD Ryzen 7 7800X3D',
            'sku': 'RYZEN77800X3D',
            'descricao': 'Processador AMD Ryzen 7 7800X3D - 8 núcleos, 16 threads, 4.2GHz base / 5.0GHz boost, cache 3D V-Cache 96MB, AM5.',
            'preco': 2799.00,
            'estoque': 12,
            'categoria': 'Componentes'
        },
        
        # Áudio
        {
            'nome': 'Headset HyperX Cloud III',
            'sku': 'HYPERXCLOUD3',
            'descricao': 'Headset Gamer HyperX Cloud III - Som surround 7.1, drivers 53mm, microfone removível com cancelamento de ruído, almofadas memory foam.',
            'preco': 699.00,
            'estoque': 25,
            'categoria': 'Áudio'
        },
        {
            'nome': 'Fone Sony WH-1000XM5',
            'sku': 'SONYWH1000XM5',
            'descricao': 'Fone Sony WH-1000XM5 - Cancelamento de ruído líder de mercado, 30h de bateria, LDAC, multipoint, controle por toque.',
            'preco': 2299.00,
            'estoque': 18,
            'categoria': 'Áudio'
        },
        {
            'nome': 'Microfone Blue Yeti X',
            'sku': 'BLUEYETIX',
            'descricao': 'Microfone Condensador Blue Yeti X - 4 padrões polares, medidor LED, controles de ganho/mute, suporte para choque, USB.',
            'preco': 1499.00,
            'estoque': 15,
            'categoria': 'Áudio'
        },
        {
            'nome': 'Caixa de Som JBL Flip 6',
            'sku': 'JBLFLIP6',
            'descricao': 'Caixa de Som Portátil JBL Flip 6 - Bluetooth 5.1, à prova d\'água IP67, 12h de bateria, PartyBoost, graves potentes.',
            'preco': 799.00,
            'estoque': 30,
            'categoria': 'Áudio'
        }
    ]
    
    # Criar produtos
    criados = 0
    atualizados = 0
    erros = 0
    
    for prod_data in produtos_exemplo:
        try:
            # Verificar se já existe
            produto_existente = produto_repo.get_by_sku(prod_data['sku'])
            
            categoria = categorias.get(prod_data['categoria'])
            if not categoria:
                print(f"❌ Categoria '{prod_data['categoria']}' não encontrada para {prod_data['nome']}")
                erros += 1
                continue
            
            if produto_existente:
                # Atualizar
                produto_existente.nome = prod_data['nome']
                produto_existente.descricao = prod_data['descricao']
                produto_existente.preco = prod_data['preco']
                produto_existente.estoque = prod_data['estoque']
                produto_existente.categoria_id = categoria.id
                produto_repo.update(produto_existente)
                print(f"🔄 Atualizado: {prod_data['nome']}")
                atualizados += 1
            else:
                # Criar novo
                novo_produto = Produto(
                    nome=prod_data['nome'],
                    sku=prod_data['sku'],
                    descricao=prod_data['descricao'],
                    preco=prod_data['preco'],
                    estoque=prod_data['estoque'],
                    categoria_id=categoria.id
                )
                produto_repo.create(novo_produto)
                print(f"✅ Criado: {prod_data['nome']}")
                criados += 1
        
        except Exception as e:
            print(f"❌ Erro ao processar {prod_data['nome']}: {str(e)}")
            erros += 1
    
    # Fechar sessão
    db.close_session()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DA IMPORTAÇÃO")
    print("="*60)
    print(f"✅ Produtos criados: {criados}")
    print(f"🔄 Produtos atualizados: {atualizados}")
    print(f"❌ Erros: {erros}")
    print(f"📦 Total processado: {criados + atualizados + erros}")
    print("="*60)
    
    if criados + atualizados > 0:
        print("\n🎉 Produtos de exemplo criados com sucesso!")
        print("🌐 Acesse http://localhost:5000/produtos para visualizar")
    else:
        print("\n⚠️ Nenhum produto foi criado. Verifique se as categorias existem.")


if __name__ == '__main__':
    criar_produtos_exemplo()
