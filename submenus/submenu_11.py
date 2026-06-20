from banco_dados.conexao import connect_db

def delete_func():
    """ COMANDO PARA DELETAR FUNCIONARIO """
    soft_del = input("Digite [ID] do funcionario que você deseja apagar: ")

    conexao, cursor = connect_db()
    cursor.execute("UPDATE funcionarios SET ativo = 0 WHERE id = %s ", (soft_del, ))
    funcionario = cursor.rowcount 
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
    if funcionario == 1:
        print("Funcionario desativado !")
    else:
        print("ID Desconhecido, Tente de novo. . .")

def delete_client():
    """ COMANDO PARA DELETAR CLIENTE MUDADO APENAS PELAS NOMENCLATURAS """
    soft_del = input("Digite [ID] do cliente que você deseja apagar: ")

    conexao, cursor = connect_db()
    cursor.execute("UPDATE clientes SET ativo = 0 WHERE id = %s ", (soft_del, ))
    cliente = cursor.rowcount 
    conexao.commit()
    
    cursor.close()
    conexao.close()

    if cliente == 1:    
        print("Cliente desativado !")
    else:
        print("ID Desconhecido, Tente de novo. . .")\
        
def data_client():
    """ COMANDO PARA ALTERAR TODOS DADOS CLIENTE """

    change_client = input("Digite o [ID] do cliente que deseja fazer alteração: ") 
    new_name = input("Digite o novo nome: ") 
    new_tel = input("Digite o novo telefone: ")
    new_cpf = input("Digite o novo cpf: ")
    new_data_nasc = input("Digite a nova data de nascimento: ")
    new_end = input("Digite o novo endereco: ")
    new_limit = float(input("Digite o novo limite: "))

    if len(new_tel) != 11:
        print("Telefone com quantidade de numeros erradas!")
        return 
    elif len(new_cpf) != 11:
        print("CPF com quantidade de numeros erradas!")
        return 
    elif len(new_data_nasc) != 10:
        print("Data invalida!")
        return             
    elif new_limit > 1000:
        print("Nenhum cliente pode ter limite maior que R$ 1.000,00! ")
        return 

    conexao, cursor = connect_db()
    cursor.execute("UPDATE clientes SET nome = %s, telefone = %s, cpf = %s, data_nasc = %s, endereco = %s, limite = %s WHERE id = %s ", (new_name, new_tel, new_cpf, new_data_nasc, new_end, new_limit, change_client))
    alterou = cursor.rowcount
    conexao.commit()

    cursor.close()
    conexao.close()

    if alterou == 1:
        print("Sucesso! Dados do Cliente Alterado. . .")
    else:
        print("ERRO! Digite um numero de [ID]!") 

def data_func():
    """ COMANDO PARA ALTERAR TODOS DADOS DOS FUNCIONARIOS """
    change_func = input("Digite o [ID] do funcionario que deseja fazer alteração: ") 
    new_name = input("Digite o novo nome: ") 
    new_tel = input("Digite o novo telefone: ")
    new_cpf = input("Digite o novo cpf: ")
    new_data_nasc = input("Digite a nova data de nascimento: ")
    new_end = input("Digite o novo endereco: ")

    if len(new_tel) != 11:
        print("Telefone com quantidade de numeros erradas!")
        return 
    elif len(new_cpf) != 11:
        print("CPF com quantidade de numeros erradas!")
        return 
    elif len(new_data_nasc) != 10:
        print("Data invalida!")
        return             

    conexao, cursor = connect_db()
    cursor.execute("UPDATE funcionarios SET nome = %s, telefone = %s, cpf = %s, data_nasc = %s, endereco = %s WHERE id = %s ", (new_name, new_tel, new_cpf, new_data_nasc, new_end, change_func))
    alterou = cursor.rowcount
    conexao.commit()

    cursor.close()
    conexao.close()

    if alterou == 1:
        print("Sucesso! Dados do Funcionario Alterado. . .")
    else:
        print("ERRO! Digite um numero de [ID]!") 

def new_client():
    """ COMANDO PARA CADASTRAR UM NOVO CLIENTE """

    new_name = input("Digite o nome: ") 
    new_tel = input("Digite o telefone: ")
    new_cpf = input("Digite o cpf: ")
    new_data_nasc = input("Digite a data de nascimento: ")
    new_end = input("Digite o endereco: ")
    new_limit = float(input("Digite o limite: "))

    if len(new_tel) != 11:
        print("Telefone com quantidade de numeros erradas!")
        return 
    elif len(new_cpf) != 11:
        print("CPF com quantidade de numeros erradas!")
        return 
    elif len(new_data_nasc) != 10:
        print("Data invalida!")
        return             
    elif new_limit > 1000:
        print("Nenhum cliente pode ter limite maior que R$ 1.000,00! ")
        return 

    conexao, cursor = connect_db()
    cursor.execute("INSERT INTO clientes (nome, telefone, cpf, data_nasc, endereco, limite) VALUES (%s, %s, %s, %s, %s, %s)", (new_name, new_tel, new_cpf, new_data_nasc, new_end, new_limit ))

    alterou = cursor.rowcount
    conexao.commit()

    cursor.close()
    conexao.close()

    if alterou == 1:
        print("Sucesso! Cliente cadastrado com sucesso!. . .")
    else:
        print("ERRO! 404 CONSULTE O SISTEMA. . . . . ") 

def new_func():
    """ COMANDO PARA CADASTRAR UM NOVO FUNCIONARIO """

    new_name = input("Digite o nome: ") 
    new_tel = input("Digite o telefone: ")
    new_cpf = input("Digite o cpf: ")
    new_data_nasc = input("Digite a data de nascimento: ")
    new_end = input("Digite o endereco: ")

    if len(new_tel) != 11:
        print("Telefone com quantidade de numeros erradas!")
        return 
    elif len(new_cpf) != 11:
        print("CPF com quantidade de numeros erradas!")
        return 
    elif len(new_data_nasc) != 10:
        print("Data invalida!")
        return             
    
    conexao, cursor = connect_db()
    cursor.execute("INSERT INTO funcionarios (nome, telefone, cpf, data_nasc, endereco) VALUES (%s, %s, %s, %s, %s )", (new_name, new_tel, new_cpf, new_data_nasc, new_end ))

    alterou = cursor.rowcount
    conexao.commit()
    
    cursor.close()
    conexao.close()

    if alterou == 1:
        print("Sucesso! Funcionario cadastrado com sucesso!. . .")
    else:
        print("ERRO! 404 CONSULTE O SISTEMA. . . . . ") 