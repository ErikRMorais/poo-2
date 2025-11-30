"""Script para criar todas as categorias necessárias."""

from database import Database
from models.categoria import Categoria
from repositories.categoria_repository import CategoriaRepository


def criar_categorias():
    """Cria todas as categorias necessárias."""
    
    db = Database()
    session = db.get_session()
    categoria_repo = CategoriaRepository(session)
    
    categorias = [
        'Smartphones',
        'Notebooks',
        'Periféricos',
        'Componentes',
        'Áudio',
        'Tablets',
        'Smartwatches',
        'Câmeras',
        'Games',
        'Acessórios'
    ]
    
    print("🔄 Criando categorias...\n")
    
    criadas = 0
    existentes = 0
    
    for nome_categoria in categorias:
        categoria_existente = categoria_repo.get_by_nome(nome_categoria)
        
        if categoria_existente:
            print(f"⚠️  Já existe: {nome_categoria}")
            existentes += 1
        else:
            nova_categoria = Categoria(nome=nome_categoria)
            categoria_repo.create(nova_categoria)
            print(f"✅ Criada: {nome_categoria}")
            criadas += 1
    
    db.close_session()
    
    print("\n" + "="*50)
    print(f"✅ Categorias criadas: {criadas}")
    print(f"⚠️  Categorias já existentes: {existentes}")
    print("="*50)


if __name__ == '__main__':
    criar_categorias()
