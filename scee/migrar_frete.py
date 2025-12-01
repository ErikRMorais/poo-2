"""Script para adicionar campos de frete à tabela pedidos."""

import sqlite3
from datetime import datetime

def migrar_frete():
    """Adiciona campos de frete à tabela pedidos."""
    
    print("=" * 60)
    print("🔧 MIGRAÇÃO: Adicionar Campos de Frete")
    print("=" * 60)
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect('scee_loja.db')
        cursor = conn.cursor()
        
        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(pedidos)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        colunas_adicionadas = []
        
        # Adicionar tipo_frete se não existir
        if 'tipo_frete' not in colunas:
            print("\n📦 Adicionando coluna 'tipo_frete'...")
            cursor.execute("""
                ALTER TABLE pedidos 
                ADD COLUMN tipo_frete VARCHAR(50) DEFAULT 'Fixo'
            """)
            colunas_adicionadas.append('tipo_frete')
            print("✅ Coluna 'tipo_frete' adicionada")
        else:
            print("\n⚠️  Coluna 'tipo_frete' já existe")
        
        # Adicionar valor_frete se não existir
        if 'valor_frete' not in colunas:
            print("\n💰 Adicionando coluna 'valor_frete'...")
            cursor.execute("""
                ALTER TABLE pedidos 
                ADD COLUMN valor_frete FLOAT DEFAULT 0.0
            """)
            colunas_adicionadas.append('valor_frete')
            print("✅ Coluna 'valor_frete' adicionada")
        else:
            print("\n⚠️  Coluna 'valor_frete' já existe")
        
        # Adicionar prazo_entrega se não existir
        if 'prazo_entrega' not in colunas:
            print("\n📅 Adicionando coluna 'prazo_entrega'...")
            cursor.execute("""
                ALTER TABLE pedidos 
                ADD COLUMN prazo_entrega INTEGER DEFAULT 7
            """)
            colunas_adicionadas.append('prazo_entrega')
            print("✅ Coluna 'prazo_entrega' adicionada")
        else:
            print("\n⚠️  Coluna 'prazo_entrega' já existe")
        
        # Commit das mudanças
        if colunas_adicionadas:
            conn.commit()
            print("\n" + "=" * 60)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print(f"\n📊 Colunas adicionadas: {', '.join(colunas_adicionadas)}")
        else:
            print("\n" + "=" * 60)
            print("ℹ️  NENHUMA MIGRAÇÃO NECESSÁRIA")
            print("=" * 60)
            print("\nTodas as colunas já existem no banco de dados.")
        
        # Verificar estrutura final
        cursor.execute("PRAGMA table_info(pedidos)")
        colunas_finais = cursor.fetchall()
        
        print("\n📋 Estrutura da tabela 'pedidos':")
        print("-" * 60)
        for col in colunas_finais:
            print(f"  {col[1]:<20} {col[2]:<15} {'NOT NULL' if col[3] else 'NULL':<10}")
        print("-" * 60)
        
        # Fechar conexão
        conn.close()
        
        print("\n✅ Banco de dados atualizado!")
        print("\n🚀 Agora você pode reiniciar a aplicação:")
        print("   python app.py")
        print("=" * 60)
        
    except sqlite3.Error as e:
        print(f"\n❌ Erro ao migrar banco de dados: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
    
    return True

if __name__ == '__main__':
    migrar_frete()
