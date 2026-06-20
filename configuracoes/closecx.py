import datetime
from banco_dados.conexao import connect_db

def end_day():
    data_hora_atual = datetime.datetime.now()
    datatxt = data_hora_atual.strftime("%Y/%m/%d %H:%M")
    sqldate = data_hora_atual.strftime("%Y-%m-%d")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<198}FECHAMENTO DE CAIXA {datatxt}  ██")
    print("█" * 260)

    try:
        conexao, cursor = connect_db()

        cursor.execute("SELECT SUM(valor), COUNT(id_venda) FROM vendas WHERE DATE(horario_venda) = %s", (sqldate,))
        resultado = cursor.fetchone()
        ttvendas = float(resultado[0]) if resultado[0] else 0.0
        vendas = int(resultado[1]) if resultado[1] else 0

        if vendas == 0:
            print(f"██  {'O Caixa está zerado hoje. :(':<254}██")
            print("█" * 260)
            input("\n ENTER para retornar ao menu. . .")
            return

        cursor.execute("SELECT pagamento, SUM(valor) FROM vendas WHERE DATE(horario_venda) = %s GROUP BY pagamento", (sqldate,))
        pagamentos = cursor.fetchall()

        ## dicionario p achhar o dinheiro
        totais_pgto = {p[0].upper(): float(p[1]) for p in pagamentos}
        
        ## O .get() tenta pegar o valor da chave dinheiro
        esperado_dinheiro = totais_pgto.get('DINHEIRO', 0.0)

        print("\n" + "█" * 60)
        print("(FECHAMENTO)")
        print("=" * 60)
        gaveta_str = input(" Valor da gaveta: R$ ").replace(',', '.')
        
        valor_gaveta = float(gaveta_str)
        diferenca = valor_gaveta - esperado_dinheiro

        print("\n")
        print("█" * 260)
        titulo = f" RELATÓRIO DATA: {datatxt}"
        print(f"██  {titulo:<254}██")
        print("██" + "=" * 256 + "██")

        linha_op = f"   >> TOTAL DE CUPONS EMITIDOS HOJE: {vendas}"
        print(f"██  {linha_op:<254}██")
        
        linha_fat = f"   >> FATURAMENTO BRUTO DO DIA: R$ {ttvendas:.2f}"
        print(f"██  {linha_fat:<254}██")
        print("██" + "-" * 256 + "██")
        
        print(f"██  {' RESUMO POR FORMA DE PAGAMENTO:':<254}██")
        for pgto, valor in totais_pgto.items():
            linha_p = f"      - {pgto:<15}: R$ {valor:.2f}"
            print(f"██  {linha_p:<254}██")

        print("██" + "-" * 256 + "██")
        print(f"██  {'  RESULTADO :':<254}██")
        
        if diferenca == 0:
            status = "Confere Caixa OK!"
        elif diferenca > 0:
            status = f"SOBRA DE CAIXA: Sobrou R$ {abs(diferenca):.2f}."
        else:
            status = f" QUEBRA DE CAIXA: FALTOU R$ {abs(diferenca):.2f}."

        print(f"██  {status:<254}██")
        print("█" * 260)


        nome_arquivo = f"fechamento_caixa_{sqldate}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write(f"          RELATORIO DE  FECHAMENTO DE CAIXA       \n")
            f.write(f"          GERADO EM: {datatxt}                   \n")
            f.write("==================================================\n")
            f.write(f"TOTAL DE OPERAÇÕES: {vendas} cupons\n")
            f.write(f"FATURAMENTO BRUTO:  R$ {ttvendas:.2f}\n")
            f.write("██████████████████████████████████████████████████\n")
            f.write("SUBTOTAIS POR PAGAMENTO:\n")
            for pgto, valor in totais_pgto.items():
                f.write(f" > {pgto:<15}: R$ {valor:.2f}\n")
            f.write("--------------------------------------------------\n")
            f.write("DINHEIRO EM CAIXA\n")
            f.write(f" Esperado no Sistema : R$ {esperado_dinheiro:.2f}\n")
            f.write(f" Informado p/ Operador: R$ {valor_gaveta:.2f}\n")
            f.write(f"\n PARECER FINAL: {status}\n")
            f.write("==================================================\n")

        print(f"\n Arquivo '{nome_arquivo}' foi gerado e salvo.")

    except ValueError:
        print("\n ERRO DIGITE NUMEROS.")
    except Exception as erro:
        print(f"\nERRO:{erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            
    input("\nENTER para ir ao menu principal...")