"""Módulo para importação e exportação de dados em lote."""

import csv
import io
from typing import List, Dict, Any
from datetime import datetime
from repositories.produto_repository import ProdutoRepository
from repositories.categoria_repository import CategoriaRepository
from repositories.pedido_repository import PedidoRepository
from models.produto import Produto


class ImportacaoController:
    """
    Controller para importação e exportação de dados em lote.
    
    Atende ao requisito RNF01.3: Sincronização de dados sem travar o sistema.
    """
    
    def __init__(self, session):
        """
        Inicializa o controller de importação.
        
        Args:
            session: Sessão do SQLAlchemy.
        """
        self.session = session
        self.produto_repo = ProdutoRepository(session)
        self.categoria_repo = CategoriaRepository(session)
        self.pedido_repo = PedidoRepository(session)
    
    def importar_produtos_csv(self, arquivo_csv: str) -> tuple[bool, str, Dict[str, int]]:
        """
        Importa produtos de um arquivo CSV.
        
        Formato esperado do CSV:
        sku,nome,descricao,preco,estoque,categoria_nome
        
        Args:
            arquivo_csv: Caminho do arquivo CSV ou conteúdo do arquivo.
            
        Returns:
            Tupla (sucesso, mensagem, estatisticas).
            estatisticas: {'criados': int, 'atualizados': int, 'erros': int}
        """
        estatisticas = {'criados': 0, 'atualizados': 0, 'erros': 0}
        erros_detalhados = []
        
        try:
            # Ler CSV
            if isinstance(arquivo_csv, str) and '\n' in arquivo_csv:
                # Conteúdo do arquivo
                reader = csv.DictReader(io.StringIO(arquivo_csv))
            else:
                # Caminho do arquivo
                with open(arquivo_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    linhas = list(reader)
            
            # Processar em lote
            for idx, linha in enumerate(linhas, start=2):  # linha 2 (1 é cabeçalho)
                try:
                    # Validar campos obrigatórios
                    campos_obrigatorios = ['sku', 'nome', 'preco', 'estoque', 'categoria_nome']
                    for campo in campos_obrigatorios:
                        if campo not in linha or not linha[campo].strip():
                            raise ValueError(f"Campo obrigatório ausente: {campo}")
                    
                    # Buscar ou criar categoria
                    categoria = self.categoria_repo.get_by_nome(linha['categoria_nome'].strip())
                    if not categoria:
                        erros_detalhados.append(f"Linha {idx}: Categoria '{linha['categoria_nome']}' não encontrada")
                        estatisticas['erros'] += 1
                        continue
                    
                    # Verificar se produto já existe (por SKU)
                    produto_existente = self.produto_repo.get_by_sku(linha['sku'].strip())
                    
                    if produto_existente:
                        # Atualizar produto existente
                        produto_existente.nome = linha['nome'].strip()
                        produto_existente.descricao = linha.get('descricao', '').strip()
                        produto_existente.preco = float(linha['preco'])
                        produto_existente.estoque = int(linha['estoque'])
                        produto_existente.categoria_id = categoria.id
                        
                        self.produto_repo.update(produto_existente)
                        estatisticas['atualizados'] += 1
                    else:
                        # Criar novo produto
                        novo_produto = Produto(
                            sku=linha['sku'].strip(),
                            nome=linha['nome'].strip(),
                            descricao=linha.get('descricao', '').strip(),
                            preco=float(linha['preco']),
                            estoque=int(linha['estoque']),
                            categoria_id=categoria.id
                        )
                        
                        self.produto_repo.create(novo_produto)
                        estatisticas['criados'] += 1
                
                except ValueError as e:
                    erros_detalhados.append(f"Linha {idx}: {str(e)}")
                    estatisticas['erros'] += 1
                except Exception as e:
                    erros_detalhados.append(f"Linha {idx}: Erro inesperado - {str(e)}")
                    estatisticas['erros'] += 1
            
            # Mensagem de resultado
            mensagem = f"Importação concluída: {estatisticas['criados']} criados, {estatisticas['atualizados']} atualizados, {estatisticas['erros']} erros"
            
            if erros_detalhados:
                mensagem += "\n\nErros:\n" + "\n".join(erros_detalhados[:10])  # Mostrar primeiros 10 erros
                if len(erros_detalhados) > 10:
                    mensagem += f"\n... e mais {len(erros_detalhados) - 10} erros"
            
            return True, mensagem, estatisticas
        
        except Exception as e:
            return False, f"Erro ao processar arquivo CSV: {str(e)}", estatisticas
    
    def atualizar_estoque_em_lote(self, atualizacoes: List[Dict[str, Any]]) -> tuple[bool, str, int]:
        """
        Atualiza estoque de múltiplos produtos em lote.
        
        Atende ao requisito RNF01.3: Processar 1000 atualizações em < 60 segundos.
        
        Args:
            atualizacoes: Lista de dicionários com formato:
                [{'sku': 'ABC123', 'estoque': 50}, ...]
                
        Returns:
            Tupla (sucesso, mensagem, quantidade_atualizada).
        """
        quantidade_atualizada = 0
        erros = []
        
        try:
            inicio = datetime.now()
            
            for atualizacao in atualizacoes:
                try:
                    sku = atualizacao.get('sku')
                    novo_estoque = atualizacao.get('estoque')
                    
                    if not sku or novo_estoque is None:
                        erros.append(f"SKU ou estoque ausente: {atualizacao}")
                        continue
                    
                    # Buscar produto
                    produto = self.produto_repo.get_by_sku(sku)
                    
                    if not produto:
                        erros.append(f"Produto não encontrado: {sku}")
                        continue
                    
                    # Atualizar estoque
                    produto.estoque = int(novo_estoque)
                    self.produto_repo.update(produto)
                    quantidade_atualizada += 1
                
                except Exception as e:
                    erros.append(f"Erro ao atualizar {sku}: {str(e)}")
            
            fim = datetime.now()
            tempo_decorrido = (fim - inicio).total_seconds()
            
            mensagem = f"Atualização concluída: {quantidade_atualizada} produtos atualizados em {tempo_decorrido:.2f}s"
            
            if erros:
                mensagem += f"\n{len(erros)} erros encontrados"
            
            return True, mensagem, quantidade_atualizada
        
        except Exception as e:
            return False, f"Erro ao atualizar estoque em lote: {str(e)}", quantidade_atualizada
    
    def exportar_produtos_csv(self) -> tuple[bool, str, str]:
        """
        Exporta todos os produtos para formato CSV.
        
        Returns:
            Tupla (sucesso, mensagem, conteudo_csv).
        """
        try:
            produtos = self.produto_repo.get_all()
            
            # Criar CSV em memória
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Cabeçalho
            writer.writerow(['SKU', 'Nome', 'Descrição', 'Preço', 'Estoque', 'Categoria'])
            
            # Dados
            for produto in produtos:
                writer.writerow([
                    produto.sku,
                    produto.nome,
                    produto.descricao,
                    f"{produto.preco:.2f}",
                    produto.estoque,
                    produto.categoria.nome if produto.categoria else ''
                ])
            
            conteudo_csv = output.getvalue()
            output.close()
            
            return True, f"{len(produtos)} produtos exportados", conteudo_csv
        
        except Exception as e:
            return False, f"Erro ao exportar produtos: {str(e)}", ""
    
    def exportar_pedidos_csv(self, data_inicio: datetime = None, data_fim: datetime = None) -> tuple[bool, str, str]:
        """
        Exporta pedidos para formato CSV (para integração com ERP).
        
        Args:
            data_inicio: Data inicial do filtro (opcional).
            data_fim: Data final do filtro (opcional).
            
        Returns:
            Tupla (sucesso, mensagem, conteudo_csv).
        """
        try:
            # Buscar todos os pedidos (em produção, filtrar por data)
            pedidos = self.pedido_repo.get_all()
            
            # Filtrar por data se fornecido
            if data_inicio:
                pedidos = [p for p in pedidos if p.data_pedido >= data_inicio]
            if data_fim:
                pedidos = [p for p in pedidos if p.data_pedido <= data_fim]
            
            # Criar CSV em memória
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Cabeçalho
            writer.writerow([
                'ID Pedido', 'Data', 'Cliente', 'CPF', 'Status',
                'Total', 'Método Pagamento', 'Endereço Entrega'
            ])
            
            # Dados
            for pedido in pedidos:
                writer.writerow([
                    pedido.id,
                    pedido.data_pedido.strftime('%Y-%m-%d %H:%M:%S'),
                    pedido.cliente.nome,
                    pedido.cliente.cpf,
                    pedido.status,
                    f"{pedido.total:.2f}",
                    pedido.metodo_pagamento,
                    pedido.endereco_entrega
                ])
            
            conteudo_csv = output.getvalue()
            output.close()
            
            return True, f"{len(pedidos)} pedidos exportados", conteudo_csv
        
        except Exception as e:
            return False, f"Erro ao exportar pedidos: {str(e)}", ""
