import datetime
from banco_dados.conexao import connect_db 

def menu_vendas():
    
    itens_car = []
    data_car = [] 
    total = 0.0

    while True:
    
        data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        ##submenu
        menu_esquerdo = [
            "",
            "   [ 1 ] CONSULTAR PRODUTOS",
            "",
            "   [ 2 ] ADICIONAR PRODUTO AO CARRINHO",
            "",
            "   [ 3 ] FINALIZAR VENDA",
            "",
            "   [ 0 ] SAIR DO MENU DE VENDAS",
            "",
            "-" * 40,
            f"   TOTAL DA COMPRA: R$ {total:.2f}",
            "-" * 40,
            ""
        ]

        menu_direito = ["  CARRINHO DE COMPRAS  ", ""]
        if len(itens_car) == 0:
            menu_direito.append("      O carrinho está vazio.")
        else:
            menu_direito.extend(itens_car) 

        print("\n") 
        print("█" * 260)
        print(f"██  MERCADO SOUL PDV{'':<180}CAIXA ABERTO {'':<4}                       {data}  ██")
        print("█" * 260)

        tt_lines = max(len(menu_esquerdo), len(menu_direito))

        for i in range(tt_lines):
            linha_e = menu_esquerdo[i] if i < len(menu_esquerdo) else ""
            linha_d = menu_direito[i] if i < len(menu_direito) else ""

            print(f"██  {linha_e:<126.126}{linha_d:<126.126}  ██")

        print("█" * 260)
##abaixo comeca o codigo acima eh so questao visual e de interface 
        try:
            comando = int(input("Digite a funcao :  "))

            if comando == 0:
                if total > 0:
                    cancela = input("Há itens no carrinho. Deseja cancelar a venda e sair? (s/n): ").lower()
                    if cancela == 's':
                        break
                else:
                    print("\nFechando PDV de Vendas. . .")
                    break

            elif comando == 1:
                search = input("\nDigite o ID ou NOME do produto para consulta: ")
                conexao, cursor = connect_db()
                cursor.execute("SELECT id, nome, preco, quantidade FROM produtos WHERE id = %s OR nome LIKE %s", (search, f"%{search}%"))
                results = cursor.fetchall()                                                         ## or nome lIKE = onde parecer o nome ou o iD por ex 3 aparece o arroz tipo 3 
                
                if results:
                    print(" ███ RESULTADOS DA BUSCA ███ ")
                    for prods in results:
                        print(f"ID: {prods[0]:<5} | Nome: {prods[1]:<20} | Preço: R${prods[2]:<7.2f} | Estoque: {prods[3]}")
                else:
                    print("Produto não encontrado.")
                    
                cursor.close()
                conexao.close()
                input("\nAperte ENTER para retornar ao Caixa . . .")

            elif comando == 2:
                id_prod = input("\nDigite o ID do produto: ")
                
                # 1. PRIMEIRO conectamos e buscamos o produto pelo ID
                conexao, cursor = connect_db()
                cursor.execute("SELECT id, nome, preco, quantidade FROM produtos WHERE id = %s AND ativo = 1", (id_prod,))
                produto = cursor.fetchone()
                
                if produto:
                    nome_produto = produto[1]
                    estoque_atual = produto[3]
                    
                    try:
                        if nome_produto.upper().lower().endswith("KG" or "kg"):
                            entrada_qtd = input(f"Digite a quantidade em quilos {nome_produto} ").replace(',', '.')
                            qtd = float(entrada_qtd) 
                        else:
                            entrada_qtd = input(f"Digite a quantidade de {nome_produto} ")
                            qtd = int(entrada_qtd) 
                        
                        if estoque_atual >= qtd:
                            subtotal = float(produto[2]) * qtd
                            total += subtotal
                            
                            itens_car.append(f"   {qtd}x {produto[1]} - Un: R${produto[2]:.2f} | Sub: R${subtotal:.2f}")
                            data_car.append({
                                "id_produto": produto[0],
                                "qtd": qtd,
                                "subtotal": subtotal
                            })
                            print(f"\n {qtd}x {produto[1]} adicionado com sucesso!")
                        else:
                            print(f"\n Estoque insuficiente! Somente {estoque_atual} disponíveis.")
                            
                    except ValueError:
                        print("\n ERRO! Digite um formato numérico válido (inteiro para unidades, decimal para KG).")
                else:
                    print("\n Produto não encontrado.") 
                
                cursor.close()
                conexao.close()
                
                input("\nAperte ENTER para continuar . . .")

            elif comando == 3:
                if total == 0:
                    input("\n O carrinho está vazio!")
                    continue
                
                print(f"\n███████████████████████████████████████")
                print(f" FECHAMENTO - TOTAL: R$ {total:.2f}")
                print(f"███████████████████████████████████████")
                

                nfe = input("\nDeseja CPF na Nota Fiscal? (s/n): ").lower()
                cpf_nota = " [CPF] Não informado"
                if nfe == 's':
                    cpf_nota = input("Digite o CPF do cliente: ")

                print("[ 1 ] DINHEIRO")
                print("[ 2 ] CARTÃO (Crédito/Débito)")
                print("[ 3 ] PIX")
                print("[ 4 ] A PRAZO (Requer Cadastro de Cliente)")
                
                pgto_opcao = input("Escolha a forma de pagamento: ")
                forma_pgto = ""
                approved = False

                if pgto_opcao == '1':
                    forma_pgto = "Dinheiro"
                    recebido = float(input("Valor recebido do cliente: R$ "))
                    if recebido >= total:
                        troco = recebido - total
                        print(f"Pagamento aprovado!TROCO: R$ {troco:.2f}")
                        approved = True
                    else:
                        print(" Dinheiro insuficiente!")
                        
                elif pgto_opcao == '2':
                    forma_pgto = "Cartão"
                    print("Transação Aprovada!")
                    approved = True
                    
                elif pgto_opcao == '3':
                    forma_pgto = "Pix"
                    print("Transferência Recebida!")
                    approved = True
                    
                elif pgto_opcao == '4':
                    forma_pgto = "A Prazo"
                    cpf_cliente = input("Digite o CPF do cliente cadastrado: ")
                    
                    conexao, cursor = connect_db()
                    cursor.execute("SELECT id, nome, limite FROM clientes WHERE cpf = %s AND ativo = 1", (cpf_cliente,))
                    cliente = cursor.fetchone()
                    
                    if cliente:
                        limite_atual = float(cliente[2])
                        if limite_atual >= total:
                            novo_limite = limite_atual - total
                            cursor.execute("UPDATE clientes SET limite = %s WHERE id = %s", (novo_limite, cliente[0]))
                            conexao.commit()
                            print(f" Venda a prazo autorizada para {cliente[1]}.")
                            print(f"Limite restante do cliente: R$ {novo_limite:.2f}")
                            approved = True
                        else:
                            print(f" Venda Negada! O limite de {cliente[1]} e de: (R$ {limite_atual:.2f}) ")
                    else:
                        print(" Cliente não encontrado ou inativo no sistema.")
                    
                    cursor.close()
                    conexao.close()
                    
                else:
                    print("Opção de pagamento inválida.")

                if approved:
                    print("\nGerando Cupom Fiscal. . .")
                    conexao, cursor = connect_db()
                    data_venda = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    try:
                        for item in data_car:

                            cursor.execute("""
                                INSERT INTO vendas (horario_venda, id_nome, qtd, valor, pagamento) 
                                VALUES (%s, %s, %s, %s, %s)
                            """, (data_venda, item['id_produto'], item['qtd'], item['subtotal'], forma_pgto))

                            cursor.execute("""
                                UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s
                            """, (item['qtd'], item['id_produto']))

                        conexao.commit()
                        print(f" VENDA FINALIZADA   {cpf_nota})")

                        itens_car.clear()
                        data_car.clear()
                        total = 0.0
                        
                    except Exception as erro:
                        print(f"ERRO no Banco de Dados: {erro}")
                        conexao.rollback()
                    finally:
                        cursor.close()
                        conexao.close()

                    input("\nENTER para ir ao menu principal. . .")

            else: 
                input("\n Digite um número de 0 a 3. [ENTER] ")
        
        except ValueError:
            input("\nERRO: Digite apenas números!")