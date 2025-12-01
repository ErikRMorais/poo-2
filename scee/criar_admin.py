"""Script para criar novos usuários administradores."""

from database import Database
from models.admin import Admin
from argon2 import PasswordHasher

def criar_admin():
    """Cria um novo administrador no sistema."""
    
    print("=" * 50)
    print("🔧 CRIAR NOVO ADMINISTRADOR")
    print("=" * 50)
    
    # Coletar dados
    nome = input("\n👤 Nome do administrador: ").strip()
    email = input("📧 E-mail: ").strip()
    senha = input("🔒 Senha: ").strip()
    
    # Validações básicas
    if not nome or not email or not senha:
        print("\n❌ Erro: Todos os campos são obrigatórios!")
        return
    
    if len(senha) < 6:
        print("\n❌ Erro: Senha deve ter no mínimo 6 caracteres!")
        return
    
    if '@' not in email or '.' not in email:
        print("\n❌ Erro: E-mail inválido!")
        return
    
    # Confirmar
    print("\n" + "=" * 50)
    print("📋 CONFIRME OS DADOS:")
    print(f"   Nome: {nome}")
    print(f"   E-mail: {email}")
    print(f"   Senha: {'*' * len(senha)}")
    print("=" * 50)
    
    confirma = input("\n✅ Confirmar criação? (s/n): ").strip().lower()
    
    if confirma != 's':
        print("\n❌ Operação cancelada.")
        return
    
    # Criar admin
    try:
        db = Database()
        session = db.get_session()
        
        # Verificar se e-mail já existe
        from repositories.admin_repository import AdminRepository
        admin_repo = AdminRepository(session)
        
        if admin_repo.get_by_email(email):
            print(f"\n❌ Erro: E-mail '{email}' já está cadastrado!")
            session.close()
            return
        
        # Hash da senha
        ph = PasswordHasher()
        senha_hash = ph.hash(senha)
        
        # Criar admin
        admin = Admin(
            nome=nome,
            email=email,
            senha_hash=senha_hash
        )
        
        session.add(admin)
        session.commit()
        
        print("\n" + "=" * 50)
        print("✅ ADMINISTRADOR CRIADO COM SUCESSO!")
        print("=" * 50)
        print(f"👤 Nome: {nome}")
        print(f"📧 E-mail: {email}")
        print(f"🔑 ID: {admin.id}")
        print("=" * 50)
        print("\n🌐 Acesse: http://localhost:5000/login")
        print(f"📧 Login: {email}")
        print(f"🔒 Senha: {senha}")
        print("=" * 50)
        
        session.close()
        
    except Exception as e:
        print(f"\n❌ Erro ao criar administrador: {e}")

def listar_admins():
    """Lista todos os administradores cadastrados."""
    
    print("\n" + "=" * 50)
    print("👥 ADMINISTRADORES CADASTRADOS")
    print("=" * 50)
    
    try:
        db = Database()
        session = db.get_session()
        
        from repositories.admin_repository import AdminRepository
        admin_repo = AdminRepository(session)
        admins = admin_repo.get_all()
        
        if not admins:
            print("\n⚠️  Nenhum administrador cadastrado.")
        else:
            for i, admin in enumerate(admins, 1):
                print(f"\n{i}. {admin.nome}")
                print(f"   📧 E-mail: {admin.email}")
                print(f"   🔑 ID: {admin.id}")
                if hasattr(admin, 'data_cadastro') and admin.data_cadastro:
                    print(f"   📅 Cadastro: {admin.data_cadastro.strftime('%d/%m/%Y %H:%M')}")
        
        print("\n" + "=" * 50)
        session.close()
        
    except Exception as e:
        print(f"\n❌ Erro ao listar administradores: {e}")

def menu():
    """Menu principal."""
    
    while True:
        print("\n" + "=" * 50)
        print("🔧 GERENCIADOR DE ADMINISTRADORES")
        print("=" * 50)
        print("\n1. Criar novo administrador")
        print("2. Listar administradores")
        print("3. Sair")
        print("=" * 50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            criar_admin()
        elif opcao == '2':
            listar_admins()
        elif opcao == '3':
            print("\n👋 Até logo!")
            break
        else:
            print("\n❌ Opção inválida!")

if __name__ == '__main__':
    menu()
