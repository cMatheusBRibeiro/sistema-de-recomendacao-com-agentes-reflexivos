from produtos import Produtos
from recomendacoes import Recomendacoes
from relatorios import Relatorios

class Administracao:
    def open(self):
        print('----------------------')
        print('Abrindo admin.')
        print('----------------------')

        while True:
            print('Selecione uma das opcoes a seguir.')
            decision = input('1 - Produtos\n'
                             '2 - Recomendacoes\n'
                             '3 - Relatorio\n'
                             '0 - Sair\n')
            if decision == '0':
                return
            else:
                if decision == '1':
                    produtos = Produtos()
                    produtos.open()
                elif decision == '2':
                    recomendacoes = Recomendacoes()
                    recomendacoes.open()
                elif decision == '3':
                    relatorios = Relatorios()
                    relatorios.open()
                else:
                    print('Opção inválida.')