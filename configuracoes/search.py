import datetime
from banco_dados.conexao import connect_db

def products():
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("\n")
    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<203}VER PRODUTOS {'':<4} {data} ██")
    print("█" * 260)

    title = f"{'ID':<6} | {'NOME':<40} | {'MARCA':<30} | {'PREÇO':<13} | {'ESTOQUE':<12} | {'SETOR':<30}"

    print(f"██  {title:<254}██")

    print("██" + "-" * 256 + "██")

    try:
        conexao, cursor = connect_db()
        cursor.execute("SELECT id, nome, marca, preco, quantidade, setor FROM produtos WHERE ativo = 1")
        produtos = cursor.fetchall()

        if not produtos:
            print(f"██  {'Sem produtos cadastrados.':<254}██")
        else:
            for p in produtos:
                price_f = f"R$ {p[3]:.2f}"
                linha = f"{p[0]:<6} | {p[1]:<40.40} | {p[2]:<30.30} | {price_f:<13} | {p[4]:<12} | {p[5]:<30.30}"
                
                print(f"██  {linha:<254}██")

    except Exception as erro:
        print(f"██ ERRO = {str(erro):<225}██")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

    print("█" * 260)
    input("ENTER PARA VOLTAR . . . . . ")