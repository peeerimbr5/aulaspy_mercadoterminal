import datetime
from banco_dados.conexao import connect_db

def cadastrar_produto():
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    print("█" * 260)
    print(f"██  MERCADO SOUL PDV{'':<200}CADASTRO DE PRODUTO {data}  ██")
    print("█" * 260)
    print("Preencha os dados: ")

    try:
        nome = input("Nome do Produto: ")
        if nome == '0':
            print("Cadastro cancelado.")
            return

        marca = input("Marca: ")

        preco_str = input("Preço de Venda: ").replace(',', '.')
        preco = float(preco_str)
        
        quantidade = float(input("Quantidade em Estoque: "))

        is_kg = input("Este produto é vendido por KG? (s/n): ").lower()
        if is_kg == 'S':
            preco_kg = preco
        else:
            preco_kg = 0.0 

        setor = input("Setor: ")
        distribuidor = input("Distribuidor ou Fornecedor: ")
        validade = input("Validade (DD/MM/AAAA): ")
        custo = float(input("Custo do produto: ").replace(',', '.'))

        conexao, cursor = connect_db()

        exec = """
            INSERT INTO produtos 
            (nome, marca, preco, quantidade, preco_kg, setor, distribuidor, validade, custo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nome, marca, preco, quantidade, preco_kg, setor, distribuidor, validade, custo)
        
        cursor.execute(exec, values)
        conexao.commit()
        
        print(f"O produto [{nome} {marca}] foi cadastrado.")
        
    except ValueError as errodb:
        print(f"ERRO! {errodb}")
    except Exception as erro:
        print(f"\n ERRO NO BANCO DE DADOS {erro}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()