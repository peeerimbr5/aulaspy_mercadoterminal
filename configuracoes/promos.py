import datetime
from banco_dados.conexao import connect_db

def apply_promos():
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV {'':<202} CENTRAL DE PROMOÇÕES {data} ██")
    print("█" * 260)

    try:            ##submenu 
        print("\nEscolha o que deseja desejada:")
        print(" [ 1 ] Promoção em UM Produto")
        print(" [ 2 ] Desconto em TODOS os Produtos")
        print(" [ 3 ] ENCERRAR Promoção de UM Produto ")
        print(" [ 4 ] ENCERRAR Promocao de todos produtos")
        print(" [ 0 ] Voltar ")
        
        escolha = input("\nDigite a opção desejada: ")

        if escolha == '0':
            print("\n Operação cancelada.")
            return
            
        elif escolha not in ['1', '2', '3', '4']:
            print("\n Opção Inválida.")
            return

        conexao, cursor = connect_db()

        if escolha == '1':
            id_prod = input("\nDigite o [ID] do produto: ")
            
            cursor.execute("SELECT id, nome, preco, preco_original FROM produtos WHERE id = %s AND ativo = 1", (id_prod,))
            produto = cursor.fetchone()
            
            if not produto:
                print("\nProduto não encontrado ou desativado.")
                return
                
            if produto[3] is not None:
                print(f"\n O produto '{produto[1]}' JÁ ESTÁ em promoção!")
                return
                
            print(f"\n Produto Selecionado: {produto[1]} | Preço Atual: R$ {produto[2]:.2f}")
            desconto = float(input("Digite a porcentagem de desconto: ").replace(',', '.'))
            
            novo_preco = float(produto[2]) - (float(produto[2]) * (desconto / 100))
            confirma = input(f"O preço cairá para R$ {novo_preco:.2f}. Confirmar? (s/n): ").lower()
            
            if confirma == 's':
                ##  guarda o preço atual no bc e marca a data
                conectando = """
                    UPDATE produtos 
                    SET preco_original = preco, 
                        data_promocao = NOW(), 
                        preco = ROUND(preco - (preco * %s / 100), 2) 
                    WHERE id = %s
                """
                cursor.execute(conectando, (desconto, id_prod))
                conexao.commit()
                print(f"Promoção aplicada no produto [{produto[1]}].")
            else:
                print("\nPromoção cancelada.")

        elif escolha == '2':
            print("\n" + "█" * 260)
            aviso = "Certeza que vai aplicar desconto em todos? "
            print(f"██  {aviso:<254}██")
            print("█" * 260)
            
            desconto = float(input("\nDigite a porcentagem de desconto GERAL ").replace(',', '.'))
            confirma = input(f"Tem CERTEZA que deseja aplicar {desconto}% na loja inteira? (s/n): ").lower()
            
            if confirma == 's':
                conectando = """
                    UPDATE produtos 
                    SET preco_original = preco, 
                        data_promocao = NOW(), 
                        preco = ROUND(preco - (preco * %s / 100), 2) 
                    WHERE ativo = 1 AND preco_original IS NULL
                """
                cursor.execute(conectando, (desconto,))
                conexao.commit()
                print(f"Desconto aplicado, {cursor.rowcount} produtos entraram em promoção.")
            else:
                print("\nOperação cancelada.")
        ##cancelar promos
        elif escolha == '3':
            id_prod = input("\nDigite o [ID] do produto para cancelar a promoção: ")
            
            cursor.execute("SELECT nome, preco, preco_original, data_promocao FROM produtos WHERE id = %s", (id_prod,))
            produto = cursor.fetchone()
            
            if not produto:
                print("\nProduto não encontrado.")
                return
                
            if produto[2] is None:
                print(f"\nProduto [{produto[0]}] NÃO está em promoção no momento.")
                return

            data_inicio = produto[3]
            agora = datetime.datetime.now()
            dias_em_promo = (agora - data_inicio).days
            
            # verificacao se a promo foi criada e a quantos dias esta em promo.
            texto_dias = f"{dias_em_promo} dias" if dias_em_promo > 0 else "Menos de 1 dia (Hoje)"

            print("\n" + "=" * 60)
            print(f" ENCERRAR PROMOÇÃO: {produto[0]}")
            print(f" Duração: A promoção durou {texto_dias}.")
            print(f" Preço Promocional: R$ {produto[1]:.2f}")
            print(f" Preço Original a Restaurar: R$ {produto[2]:.2f}")
            print("=" * 60)
            
            confirma = input("\nDeseja restaurar o preço original? (s/n): ").lower()
            
            if confirma == 's':
                conectando = "UPDATE produtos SET preco = preco_original, preco_original = NULL, data_promocao = NULL WHERE id = %s"
                cursor.execute(conectando, (id_prod,))
                conexao.commit()
                print(f"A promoção durou {texto_dias}. O preço de R$ {produto[2]:.2f} voltou!")
            else:
                print("\nCANCELADO.")

        elif escolha == '4':
            print("\n" + "█" * 260)
            alerta = " ALERTA: Você vai cancela as promoções ativas e voltar aos precos originais"
            print(f"██  {alerta:<254}██")
            print("█" * 260)
            
            confirma = input("\n deseja finalizar as promoções do sistema? (s/n): ").lower()
            
            if confirma == 's':
                print("\n Restaurando. . . ")
                conectando = "UPDATE produtos SET preco = preco_original, preco_original = NULL, data_promocao = NULL WHERE preco_original IS NOT NULL"
                cursor.execute(conectando)
                conexao.commit()
                print(f"PROMOÇÕES ENCERRADAS! {cursor.rowcount}")
            else:
                print("\n Operação cancelada.")

    except ValueError as errodb:
        print(f"ERRO! {errodb}")
    except Exception as erro:
        print(f"\n ERRO NO BANCO DE DADOS {erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

    input("\nENTER para ir ao menu principal. . .")