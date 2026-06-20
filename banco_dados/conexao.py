import mysql.connector

def connect_db():

    conexao = mysql.connector.connect(\
            host = "localhost",
            user = "vinicius",
            password = "soul_code",
            database = "mercado"
        )
    cursor = conexao.cursor()
    return conexao, cursor