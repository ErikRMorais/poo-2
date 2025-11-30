"""Script para inicializar o banco de dados com dados de exemplo."""

from database import Database
from models.categoria import Categoria
from models.admin import Admin
from argon2 import PasswordHasher

def init_database():
    """
    Inicializa o banco de dados com categorias e admin padrão.
    """
    db = Database()
    db.create_tables()
    
    session = db.get_session()
    ph = PasswordHasher()
    
    # Criar categorias padrão
    categorias = [
        'Smartphones',
        'Notebooks',
        'Tablets',
        'Acessórios',
        'Áudio',
        'Câmeras',
        'Games',
        'Smart Home'
    ]
    
    for nome_categoria in categorias:
        if not session.query(Categoria).filter(Categoria.nome == nome_categoria).first():
            categoria = Categoria(nome=nome_categoria)
            session.add(categoria)
    
    # Criar admin padrão
    if not session.query(Admin).filter(Admin.email == 'admin@scee.com').first():
        admin = Admin(
            nome='Administrador',
            email='admin@scee.com',
            senha_hash=ph.hash('Admin@123')
        )
        session.add(admin)
    
    session.commit()
    print("Banco de dados inicializado com sucesso!")
    print("\nCredenciais do Admin:")
    print("E-mail: admin@scee.com")
    print("Senha: Admin@123")
    
    db.close_session()

if __name__ == '__main__':
    init_database()
