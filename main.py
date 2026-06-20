
import datetime

from configuracoes.cadastro import cadastrar_produto
from configuracoes.closecx import end_day
from configuracoes.deactivate import deact_prod
from configuracoes.promos import apply_promos
from configuracoes.relatorios import relatxt, stats, relats_caixas
from configuracoes.search import products 
from configuracoes.venda_carrinho import menu_vendas
from interfaces.interfaceconfigs import configsmenu
from interfaces.login import users
from interfaces.menu import call_menu
from submenus.submenu4 import change_prod


##PARA A AULA FOI MONTADO JUNTO COM O PROFESSOR QUE TINHA EM BASE UMA LIVRARIA DECIDI MONTAR UM MERCADO. 
# FAVOR AO INICIAR O PROGRAMA ESTEJA DE TELA CHEIA NO TERMINAL PARA QUE A INTERFACE DE TERMINAL FIQUE COM TAMANHO CORRETO. 
# LOGIN INICIAL = id 999 user admin senha 0000

##NAO ESQUECA DE INICIAR EM TELA CHEIA



funcionario_logado = users() 

while True:
    data = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    call_menu() 

    try:
        comando = int(input("\nDigite a opção desejada: "))

        if comando == 0:
            print("\nEncerrando o Mercado Soul PDV.")
            break
            
        elif comando == 1:
            menu_vendas()

        elif comando == 2:
            products()

        elif comando == 3:
            cadastrar_produto()

        elif comando == 4:
            change_prod()

        elif comando == 5:
            deact_prod()

        elif comando == 6:
            apply_promos()
        
        elif comando == 7:
            relatxt()

        elif comando == 8:
            stats()

        elif comando == 9:
            relats_caixas()

        elif comando == 10:
            end_day()   

        elif comando == 11:
            configsmenu()

        else:
            input("\n] Opção Inválida! Digite um número de 0 a 11.")

    except ValueError:
        input(" ERRO: Digite apenas o número da opção!")
                
