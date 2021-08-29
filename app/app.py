from carrinho import Carrinho
from administracao import Administracao

carrinho = Carrinho()
administracao = Administracao()

while True:
    print('Selecione uma das opções a seguir.')
    decision = input('1 - Carrinho\n'
                     '2 - Administracao\n'
                     '0 - Sair\n')
    if decision == '0':
        break
    else:
        if decision == '1':
            carrinho.open()
        elif decision == '2':
            administracao.open()
        else:
            print('Opção inválida.')