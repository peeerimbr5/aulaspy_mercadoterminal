import datetime
from banco_dados.conexao import connect_db

def deact_prod():
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<202}SOFT DELETE {data} ██")
    print("█" * 260)

    try:
        id_prod = input("\nDigite o ID do produto que deseja DESATIVAR (ou 0 para cancelar): ")
        
        if id_prod == '0':
            print("\n Operação cancelada pelo usuário.")
            return

        conexao, cursor = connect_db()

        cursor.execute("SELECT id, nome, marca, ativo FROM produtos WHERE id = %s", (id_prod,))
        produto = cursor.fetchone()

        if not produto:
            print("\n Produto não encontrado.")
            return

        if produto[3] == 0:
            print(f"\n O produto {produto[1]} ja esta desativado.")
            return

        print("\n")
        print("█" * 260)
        aviso = f"{produto[1]} {produto[2]} Prestes a ser desativado."
        print(f"██  {aviso:<254}██")
        print("█" * 260)

        confirmacao = input(f"\nConfirma Delete neste produto? (s/n): ").lower()

        if confirmacao == 'S':
            print("\nAplicando Delete . . .")

            cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = %s", (id_prod,))
            conexao.commit()
            
            print(f" SUCESSO! O produto {produto[1]} foi removido.")
        else:
            print("\nOperação cancelada.")

    except ValueError as errodb:
        print(f"ERRO! {errodb}")
    except Exception as erro:
        print(f"\n ERRO NO BANCO DE DADOS {erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            
    input("\nENTER para ir ao menu principal...")