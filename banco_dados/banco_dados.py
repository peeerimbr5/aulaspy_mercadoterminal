import mysql.connector
from conexao import connect_db

def start_db():

    conexao, cursor = connect_db()
    cursor = conexao.cursor()
    try:
            ##tabela de produtos criacao
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,           
                marca VARCHAR(255) NOT NULL,
                preco DECIMAL(7, 2),            
                quantidade NUMERIC NOT NULL, 
                preco_kg NUMERIC,
                setor VARCHAR(255) NOT NULL,
                distribuidor VARCHAR(255) NOT NULL,
                validade VARCHAR(255) NOT NULL,
                ativo INT DEFAULT 1            
            )
            """)

            ##tabela de vendas criacao
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                id_venda INT PRIMARY KEY AUTO_INCREMENT,
                horario_venda DATETIME NOT NULL,
                id_nome INT NOT NULL,
                qtd INT NOT NULL,
                valor DECIMAL(7, 2) NOT NULL,
                pagamento VARCHAR(255) NOT NULL,
                FOREIGN KEY (id_nome) REFERENCES produtos (id)
            )
            """)

            ## selecione e conte TODOS dos produtos 
        cursor.execute("SELECT COUNT(*) FROM produtos")
            ## se cursor nao pegar nada ele abre essa tabela pre montada de itens
        if cursor.fetchone()[0] == 0:
            produtos_iniciais = [
                ("Arroz Integral", "Camil", 5.99, 12, None, "Mercearia", "Camil Alimentos", "08/08/2026", 2.99)
                ]
            cursor.executemany("""
                INSERT INTO produtos (nome, marca, preco, quantidade, preco_kg, setor, distribuidor, validade, custo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, produtos_iniciais)

            ##tabela do caixa para guardar o meu caixa 
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS caixas_dia (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    caixa_atual DECIMAL(7, 2) NOT NULL,
                    caixa_anterior DECIMAL(7, 2) NOT NULL
                )
            """)

            ## tabela para guardar os fechamentos de caixa  
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS caixa (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    data_caixa VARCHAR(255) NOT NULL,
                    faturamento_dia DECIMAL(7, 2) NOT NULL, 
                    forma_pgto VARCHAR(255) NOT NULL,
                    total DECIMAL(7, 2) NOT NULL, 
                    media_ticket DECIMAL(7, 2) NOT NULL,
                    dinheiro DECIMAL(7, 2) NOT NULL,
                    cartao DECIMAL(7, 2) NOT NULL,
                    pix DECIMAL(7, 2) NOT NULL,
                    prazo DECIMAL(7, 2) NOT NULL,
                    cliente VARCHAR(255) NOT NULL
                )          
            """)

        cursor.execute("SELECT COUNT(*) FROM caixas_dia")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO caixas_dia (caixa_atual, caixa_anterior) VALUES (100.00, 100.00)")

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    telefone VARCHAR(255) NOT NULL,
                    cpf VARCHAR(255) NOT NULL,
                    data_nasc VARCHAR(255) NOT NULL,
                    endereco VARCHAR(255) NOT NULL,
                    ativo INTEGER DEFAULT 1
                )        
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    telefone VARCHAR(255) NOT NULL,
                    cpf VARCHAR(255) NOT NULL,
                    data_nasc VARCHAR(255) NOT NULL,
                    endereco VARCHAR(255) NOT NULL,
                    limite DECIMAL(7, 2) NOT NULL,
                    ativo INT DEFAULT 1
                )        
            """)
        
        conexao.commit()
    
    except mysql.connector.Error as erro    :
        print(f"ERRO DE CONEXAO COM O BANCO DE DADOS: {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

