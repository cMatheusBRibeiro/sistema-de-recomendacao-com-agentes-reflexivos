from analisarTransacoes \
    import gerarRelatorio, \
           gerarRelatorioDaManha, \
           gerarRelatorioDaTarde, \
           gerarRelatorioDaNoite, \
           totalItensExistentes

class Relatorios:
    def open(self):
        print('----------------------')
        print('Abrindo relatorios.')
        print('----------------------')

        while True:
            print('Selecione uma das opcoes a seguir.')
            decision = input('1 - Geral\n'
                             '2 - Manhã\n'
                             '3 - Tarde\n'
                             '4 - Noite\n'
                             '5 - Total de itens\n'
                             '0 - Sair\n')
            if decision == '0':
                return
            else:
                if decision == '1':
                    gerarRelatorio()
                elif decision == '2':
                    gerarRelatorioDaManha()
                elif decision == '3':
                    gerarRelatorioDaTarde()
                elif decision == '4':
                    gerarRelatorioDaNoite()
                elif decision == '5':
                    totalItensExistentes()
                else:
                    print('Opção inválida.')
