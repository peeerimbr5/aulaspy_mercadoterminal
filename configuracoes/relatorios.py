import datetime
from banco_dados.conexao import connect_db

def relatxt():
    data_atual = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<197} HISTÓRICO E EMISSÃO NF-E {data_atual}  ██")
    print("█" * 260)

    try:
        print("\nEscolha a operação desejada:")
        print(" [ 1 ] GERAR RELATÓRIO GERAL DE VENDAS (Terminal + TXT)")
        print(" [ 2 ] REIMPRIMIR CUPOM FISCAL / NF-E DE UMA VENDA ESPECÍFICA")
        print(" [ 0 ] Voltar ao Menu Principal")
        
        opcao = input("\nDigite a opção desejada: ")

        if opcao == '0':
            return

        conexao, cursor = connect_db()
        if opcao == '1':
            sql = """
                SELECT v.id_venda, v.horario_venda, p.nome, v.qtd, v.valor, v.pagamento 
                FROM vendas v
                INNER JOIN produtos p ON v.id_nome = p.id
                ORDER BY v.id_venda DESC
            """
            cursor.execute(sql)
            vendas = cursor.fetchall()

            if not vendas:
                print("\n Nenhuma venda registrada até o momento.")
                return

            ##desenho de interface
            print("\n")
            print("█" * 260)
            titulos = f"{'ID VENDA':<10} | {'DATA/HORA':<20} | {'PRODUTO':<40} | {'QTD':<6} | {'SUBTOTAL':<14} | {'FORMA PGTO'}"
            print(f"██  {titulos:<254}██")
            print("██" + "-" * 256 + "██")

            faturamento_total = 0.0
            
            for v in vendas:
                id_venda, data_venda, nome_prod, qtd, valor, pgto = v
                faturamento_total += float(valor)
                
                data_formatada = data_venda.strftime("%Y-%m-%d %H:%M")
                valor_formatado = f"R$ {valor:.2f}"
                
                linha = f"{id_venda:<10} | {data_formatada:<20} | {nome_prod:<40.40} | {qtd:<6} | {valor_formatado:<14} | {pgto}"
                print(f"██  {linha:<254}██")

            print("██" + "-" * 256 + "██")
            resumo_total = f" FATURAMENTO TOTAL ACUMULADO em R$ {faturamento_total:.2f}"
            print(f"██  {resumo_total:<254}██")
            print("█" * 260)

            print("\n Gravando arquivo 'relatorio_vendas.txt'")
            with open("relatorio_vendas.txt", "w", encoding="utf-8") as arquivo:
                arquivo.write("=================================================================================\n")
                arquivo.write(f"                MERCADO SOUL PDV - RELATÓRIO DE VENDAS\n")
                arquivo.write(f"                Gerado em: {data_formatada}\n")
                arquivo.write("=================================================================================\n\n")
                arquivo.write(f"{'ID':<6} | {'DATA/HORA':<17} | {'PRODUTO':<30} | {'QTD':<4} | {'VALOR':<10} | {'PGTO'}\n")
                arquivo.write("-" * 81 + "\n")
                
                for v in vendas:
                    id_venda, data_venda, nome_prod, qtd, valor, pgto = v
                    d_form = data_venda.strftime("%d/%m/%Y %H:%M")
                    arquivo.write(f"{id_venda:<6} | {d_form:<17} | {nome_prod:<30.30} | {qtd:<4} | R$ {valor:<7.2f} | {pgto}\n")
                
                arquivo.write("-" * 81 + "\n")
                arquivo.write(f"TOTAL DO CAIXA: R$ {faturamento_total:.2f}\n")
                
            print("Arquivo 'relatorio_vendas.txt' gerado.")

        elif opcao == '2':
            id_busca = input("\nDigite o [ID] que deseja gerar o Cupom Fiscal: ")
            
            sql = """
                SELECT v.id_venda, v.horario_venda, p.nome, p.marca, v.qtd, v.valor, v.pagamento, p.preco 
                FROM vendas v
                INNER JOIN produtos p ON v.id_nome = p.id
                WHERE v.id_venda = %s
            """
            cursor.execute(sql, (id_busca,))
            venda_detalhe = cursor.fetchone()

            if not venda_detalhe:
                print("\n❌ [ID] inválido ")
                return

            id_venda, data_venda, nome_prod, marca_prod, qtd, valor, pgto, preco_un = venda_detalhe
            d_form = data_venda.strftime("%d/%m/%Y %H:%M:%S")
            
            nome_arquivo_cupom = f"cupom_fiscal_{id_venda}.txt"
            
            with open(nome_arquivo_cupom, "w", encoding="utf-8") as cupom:
                cupom.write("================================================\n")
                cupom.write("               MERCADO SOUL PDV                 \n")                    
                cupom.write("================================================\n")
                cupom.write(f" FISCAL: {id_venda:<15} DATA: {d_form}\n         ")
                cupom.write("------------------------------------------------\n")
                cupom.write("CUPOM FISCAL (NFE)\n                              ")
                cupom.write("------------------------------------------------\n")
                cupom.write(f"ITEM  DESCRIÇÃO\n")
                cupom.write(f"      QTD x UN                    TOTAL (R$)\n")
                cupom.write("------------------------------------------------\n")
                cupom.write(f"001   {nome_prod} {marca_prod}\n")
                cupom.write(f"      {qtd} un x R$ {preco_un:<15.2f} R$ {valor:.2f}\n")
                
                cupom.write("------------------------------------------------\n")
                cupom.write(f"  TOTAL DA COMPRA:               R$ {valor:.2f}\n")
                cupom.write(f"  FORMA DE PGTO:                 {pgto}\n")
                cupom.write("================================================\n")
                cupom.write("          OBRIGADO PELA PREFERÊNCIA!            \n")
                cupom.write("                     :)                         \n")
                cupom.write("================================================\n")

            print(f"\n Cupom Fiscal Gerado! Verifique o arquivo '{nome_arquivo_cupom}'")

    except ValueError as errodb:
        print(f"ERRO! {errodb}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
    input("\nENTER para ir ao menu principal. . .")

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\n matplotlib nao instalada")
    print("terminal - pip install matplotlib")
    exit()

def stats():
    while True:
        data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        ##cabecalho
        print("\n")
        print("█" * 260)
        print(f"██  MERCADO SOUL PDV{'':<197}DASHBOARD E RELATÓRIOS {data}  ██")
        print("█" * 260)

        linhas_menu = [
            "",
            "   [ 1 ] Produtos Mais e menos vendidos max5",
            "   [ 2 ] Desempenho por Setor ",
            "   [ 3 ] Ranking de Marcas ",
            "   [ 4 ] Formas de Pagamento ",
            "   [ 5 ] Controle de Validades",
            "   [ 6 ] Relatório de Clientes e Limites",
            "   [ 7 ] Nível de Estoque - Maior e Menor max5",
            "   [ 8 ] Curva de Preços - Mais Caros e Mais Baratos max5",
            "",
            "   [ 0 ] Voltar ao Menu ",
            ""
        ]

        for linha in linhas_menu:
            print(f"██  {linha:<254}██")
        print("█" * 260)

        try:
            opcao = input("\nDigite qual relatório deseja gerar: ")

            if opcao == '0':
                print("\nSaindo do módulo de relatórios...")
                break

            conexao, cursor = connect_db()
            ##vendas
            if opcao == '1':
                print("\n Gerando gráficos de vendas. . .")
                
                cursor.execute("""
                    SELECT p.nome, SUM(v.qtd) as total_vendido 
                    FROM vendas v JOIN produtos p ON v.id_nome = p.id 
                    GROUP BY p.id ORDER BY total_vendido DESC LIMIT 5
                """)
                mais_vendidos = cursor.fetchall()

                cursor.execute("""
                    SELECT p.nome, SUM(v.qtd) as total_vendido 
                    FROM vendas v JOIN produtos p ON v.id_nome = p.id 
                    GROUP BY p.id ORDER BY total_vendido ASC LIMIT 5
                """)
                menos_vendidos = cursor.fetchall()

                if not mais_vendidos:
                    print("Não há dados de vendas suficientes.")
                    continue

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                ax1.bar([item[0] for item in mais_vendidos], [item[1] for item in mais_vendidos], color='green')
                ax1.set_title(' Mais Vendidos. . . ')
                ax1.tick_params(axis='x', rotation=45)

                ax2.bar([item[0] for item in menos_vendidos], [item[1] for item in menos_vendidos], color='red')
                ax2.set_title(' TOP 5: Menos Vendidos')
                ax2.tick_params(axis='x', rotation=45)

                plt.tight_layout()
                plt.show()
            ##setores
            elif opcao == '2':
                print("\n gráfico de setores. . .")
                cursor.execute("""
                    SELECT p.setor, SUM(v.valor) FROM vendas v 
                    JOIN produtos p ON v.id_nome = p.id 
                    GROUP BY p.setor ORDER BY SUM(v.valor) DESC
                """)
                setores = cursor.fetchall()

                if not setores:
                    print("Não há dados de vendas.")
                    continue

                plt.figure(figsize=(8, 8))
                plt.pie([item[1] for item in setores], labels=[item[0] for item in setores], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
                plt.title('por Setor')
                plt.show()
            #m#carcas
            elif opcao == '3':
                print("\ngráfico de marcas. . .")
                cursor.execute("""
                    SELECT p.marca, SUM(v.qtd) FROM vendas v 
                    JOIN produtos p ON v.id_nome = p.id 
                    GROUP BY p.marca ORDER BY SUM(v.qtd) DESC LIMIT 10
                """)
                marcas = cursor.fetchall()

                if not marcas:
                    print(" Não há dados de vendas.")
                    continue

                plt.figure(figsize=(10, 6))
                plt.barh([item[0] for item in marcas], [item[1] for item in marcas], color='royalblue')
                plt.title('As 10 Marcas Mais Vendidas :)')
                plt.xlabel('Volume')
                plt.gca().invert_yaxis()
                plt.tight_layout()
                plt.show()
            ##pgtos
            elif opcao == '4':
                print("\nGerando gráfico de pagamentos. . .")
                cursor.execute("SELECT pagamento, SUM(valor) FROM vendas GROUP BY pagamento")
                pagamentos = cursor.fetchall()

                if not pagamentos:
                    print("Não há dados de vendas.")
                    continue

                plt.figure(figsize=(8, 8))
                plt.pie([item[1] for item in pagamentos], labels=[item[0] for item in pagamentos], autopct='%1.1f%%', colors=["#154217", "#163F61", "#A88417", "#9B322A"])
                plt.title('Faturamento por Forma de Pagamento')
                plt.show()
            ##validades
            elif opcao == '5':
                cursor.execute("SELECT id, nome, quantidade, validade FROM produtos WHERE ativo = 1 ORDER BY validade ASC")
                produtos = cursor.fetchall()

                print("\n" + "█" * 260)
                titulos = f"{'ID':<6} | {'PRODUTO':<40} | {'ESTOQUE':<10} | {'VALIDADE':<15}"
                print(f"██  {titulos:<254}██")
                print("██" + "-" * 256 + "██")

                for p in produtos:
                    linha = f"{p[0]:<6} | {p[1]:<40.40} | {p[2]:<10} | {p[3]:<15}"
                    print(f"██  {linha:<254}██")
                print("█" * 260)
                input("\nENTER para continuar. . . ")
            ##clientes
            elif opcao == '6':
                cursor.execute("SELECT id, nome, cpf, limite FROM clientes WHERE ativo = 1 ORDER BY limite DESC")
                clientes = cursor.fetchall()

                if not clientes:
                    print("\n Nenhum cliente cadastrado.")
                    continue

                print("\n" + "█" * 260)
                titulos = f"{'ID':<6} | {'NOME DO CLIENTE':<40} | {'CPF':<18} | {'LIMITE DISPONÍVEL':<18}"
                print(f"██  {titulos:<254}██")
                print("██" + "-" * 256 + "██")

                for c in clientes:
                    linha = f"{c[0]:<6} | {c[1]:<40.40} | {c[2]:<18} | R$ {c[3]:<15.2f}"
                    print(f"██  {linha:<254}██")
                print("█" * 260)
                input("\nAperte ENTER para continuar...")

            elif opcao == '7':
                print("\n análise de inventário . . .")
                
                            ##5 com mais e menos produtos
                cursor.execute("SELECT nome, quantidade FROM produtos WHERE ativo = 1 ORDER BY quantidade DESC LIMIT 5")
                maior_estoque = cursor.fetchall()

                cursor.execute("SELECT nome, quantidade FROM produtos WHERE ativo = 1 ORDER BY quantidade ASC LIMIT 5")
                menor_estoque = cursor.fetchall()

                if not maior_estoque:
                    print("Não há produtos ativos cadastrados.")
                    continue

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                ##graffico 1
                ax1.bar([item[0] for item in maior_estoque], [item[1] for item in maior_estoque], color='dodgerblue')
                ax1.set_title(' MAIOR Estoque')
                ax1.set_ylabel('Quantidade nas Prateleiras')
                ax1.tick_params(axis='x', rotation=45)

                ##graffico 2
                ax2.bar([item[0] for item in menor_estoque], [item[1] for item in menor_estoque], color='darkorange')
                ax2.set_title('MENOR Estoque')
                ax2.set_ylabel('Quantidade nas Prateleiras')
                ax2.tick_params(axis='x', rotation=45)

                plt.tight_layout()
                plt.show()

            elif opcao == '8':
                print("\n análise de preços. . .")
                
                # 5 mais caros
                cursor.execute("SELECT nome, preco FROM produtos WHERE ativo = 1 ORDER BY preco DESC LIMIT 5")
                mais_caros = cursor.fetchall()

                #5 mnais baratps
                cursor.execute("SELECT nome, preco FROM produtos WHERE ativo = 1 ORDER BY preco ASC LIMIT 5")
                mais_baratos = cursor.fetchall()

                if not mais_caros:
                    print(" Não há produtos ativos cadastrados.")
                    continue

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                ax1.bar([item[0] for item in mais_caros], [item[1] for item in mais_caros], color='purple')
                ax1.set_title('PRODUTOS MAIS CAROS ')
                ax1.set_ylabel('Preço de Venda (R$)')
                ax1.tick_params(axis='x', rotation=45)

                ax2.bar([item[0] for item in mais_baratos], [item[1] for item in mais_baratos], color='red')
                ax2.set_title(' PRODUTOS MAIS BARATOS ')
                ax2.set_ylabel('Preço de Venda (R$)')
                ax2.tick_params(axis='x', rotation=45)

                plt.tight_layout()
                plt.show()

            else:
                input("\n Opção Inválida!")
        except ValueError as errodb:
            print(f"ERRO! {errodb}")
        except Exception as erro:
            print(f"\n ERRO NO BANCO DE DADOS {erro}")
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()

def relats_caixas():
    data_atual = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<197} RELATÓRIO DE CAIXAS DIÁRIOS {data_atual}  ██")
    print("█" * 260)

    try:
        conexao, cursor = connect_db()

        sql = """
            SELECT DATE(horario_venda) as data_caixa, 
                   COUNT(id_venda) as total_operacoes, 
                   SUM(valor) as faturamento_dia 
            FROM vendas 
            GROUP BY DATE(horario_venda) 
            ORDER BY data_caixa DESC
        """
        cursor.execute(sql)
        caixas = cursor.fetchall()

        if not caixas:
            print(f"██  {' Nenhum históricoencontrado no sistema.':<254}██")
        else:
            titulos = f"{'DATA DO CAIXA':<20} | {'QTD DE VENDAS':<15} | {'FATURAMENTO DO DIA':<30}"
            print(f"██  {titulos:<254}██")
            print("██" + "-" * 256 + "██")

            faturamento_geral = 0.0

            for c in caixas:
                data_caixa, total_op, faturamento = c
                faturamento_geral += float(faturamento)
                data_formatada = data_caixa.strftime("%d/%m/%Y")
                valor_formatado = f"R$ {faturamento:.2f}"
                
                linha = f"{data_formatada:<20} | {total_op:<15} | {valor_formatado:<30}"
                print(f"██  {linha:<254}██")
            print("██" + "-" * 256 + "██")
            resumo = f"SOMA DOS CAIXAS R$ {faturamento_geral:.2f}"
            print(f"██  {resumo:<254}██")

    except ValueError as errodb:
        print(f"ERRO! {errodb}")
    except Exception as erro:
        print(f"\n ERRO NO BANCO DE DADOS {erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

    print("█" * 260)

    input("\nENTER para ir ao menu principal. . .")