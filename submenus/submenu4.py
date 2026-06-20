import datetime
from banco_dados.conexao import connect_db

def change_prod():
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<197}CENTRAL DE ALTERAÇÕES {'':<4} {data} ██")
    print("█" * 260)

    try:

        print("\n" + "=" * 60)
        print(" 🛠️  ESCOLHA O MODO DE ALTERAÇÃO")
        print("=" * 60)
        print(" [ 1 ] Edição Completa de UM Produto Específico")
        print(" [ 2 ] Reposição de Estoque em Lote")
        print(" [ 0 ] Cancelar / Voltar")
        print("=" * 60)

        changevar = input("\nDigite a opção desejada: ")

        if changevar == '0':
            print("\nSaindo da Central de Alterações. . .")
            return

        elif changevar == '2':
            print("\n" + "█" * 260)
            print(f"██  {' REPOSIÇÃO DE ESTOQUE EM LOTE':<254}██")
            print("█" * 260)
            
            qtd = int(input("\nQual a quantidade recebida para CADA item do lote? "))
            
            if qtd <= 0:
                print(" ERRO: A quantidade deve ser maior que zero.")
                return
                
            entrada_ids = input("Digite os [IDs] dos produtos separados por vírgula (Ex: 1,2,5): ")
            
            lista_ids = {int(numero.strip()) for numero in entrada_ids.split(',') if numero.strip().isdigit()}

            if len(lista_ids) == 0:
                print(" ERRO: Nenhum ID válido.")
                return

            conexao, cursor = connect_db()
            print(f"\n Iniciando reposição")

            for id_prod in lista_ids:
                cursor.execute("SELECT nome FROM produtos WHERE id = %s", [id_prod])
                resultado = cursor.fetchone()

                if not resultado:
                    print(f"    AVISO: Produto com ID {id_prod} não existe. Pulando. . .")
                    continue

                nome_prod = resultado[0]

                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade + %s
                    WHERE id = %s
                """, [qtd, id_prod])
                
                print(f"    Estoque Atualizado: {nome_prod} (ID: {id_prod})")

            conexao.commit()
            print("\nReposição em lote salva . . .")

        elif changevar == '1':
            id_prod = input("\nDigite o ID do produto que deseja alterar (ou 0 para cancelar): ")
            
            if id_prod == '0':
                print("\n CANCELADO . . . RETORNANDO.")
                return
                
            conexao, cursor = connect_db()
            
            cursor.execute("SELECT id, nome, marca, preco, quantidade, setor, validade, custo FROM produtos WHERE id = %s", (id_prod,))
            product = cursor.fetchone()

            if not product:
                print("Produto não encontrado com este ID.")
                return

            while True:
                print("\n")
                print("█" * 260)

                titulo_prod = f" PRODUTO SELECIONADO: {product[1]} (ID: {product[0]})"
                print(f"██  {titulo_prod:<254}██")
                print("██" + "-" * 256 + "██")

                custo = f"R$ {product[7]:.2f}" if product[7] is not None else "Não cadastrado"

                linhas_menu = [
                    f"[ 1 ] NOME Atual: {product[1]}",
                    f"[ 2 ] MARCA Atual: {product[2]}",
                    f"[ 3 ] PREÇO Atual: R$ {product[3]:.2f}",
                    f"[ 4 ] ESTOQUE Atual: {product[4]}",
                    f"[ 5 ] SETOR Atual: {product[5]}",
                    f"[ 6 ] VALIDADE Atual: {product[6]}",
                    f"[ 7 ] CUSTO Atual: {custo}",
                    "",
                    f"[ 0 ] CANCELAR / VOLTAR"
                ]

                for linha in linhas_menu:
                    print(f"██  {linha:<254}██")

                print("█" * 260)
                opcao = input("\nO que você deseja alterar? (0 a 7): ")

                if opcao == '0':
                    print("\nSaindo do modo de edição...")
                    break

                comando = ""
                novo_valor = None

                if opcao == '1':
                    comando = "nome"
                    novo_valor = input("Digite o NOVO NOME: ")
                    
                elif opcao == '2':
                    comando = "marca"
                    novo_valor = input("Digite a NOVA MARCA: ")
                    
                elif opcao == '3':
                    comando = "preco"
                    novo_valor = float(input("Digite o NOVO PREÇO: ").replace(',', '.'))
                    
                elif opcao == '4':
                    comando = "quantidade"
                    novo_valor = float(input("Digite o NOVO ESTOQUE: ").replace(',', '.'))
                    
                elif opcao == '5':
                    comando = "setor"
                    novo_valor = input("Digite o NOVO SETOR: ")
                    
                elif opcao == '6':
                    comando = "validade"
                    novo_valor = input("Digite a NOVA VALIDADE (DD/MM/AAAA): ")
                    
                elif opcao == '7':
                    comando = "custo"
                    novo_valor = float(input("Digite o NOVO CUSTO: ").replace(',', '.'))
                    
                else:
                    print("\n❌ Opção Inválida. Tente novamente.")
                    continue

                if comando:
                    ativar_db = f"UPDATE produtos SET {comando} = %s WHERE id = %s"
                    cursor.execute(ativar_db, (novo_valor, id_prod))
                    conexao.commit()
                    
                    print(f" O campo '{comando}' foi atualizado com sucesso!")

                    cursor.execute("SELECT id, nome, marca, preco, quantidade, setor, validade, custo FROM produtos WHERE id = %s", (id_prod,))
                    product = cursor.fetchone()
                    
        else:
            print("\n Modo inválido.")

    except ValueError:
        print("\n ERRO DE DIGITAÇÃO . . .")
    except Exception as erro:
        print(f"\n ERRO {erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            
    input("\nAperte ENTER para retornar ao menu principal. . .")