import mariadb
from connection import Connection

class Produtos:
    def open(self):
        print('----------------------')
        print('Abrindo produtos.')
        print('----------------------')

        while True:
            print('Selecione uma das opcoes a seguir.')
            decision = input('1 - Buscar produtos\n'
                             '2 - Adicionar produto\n'
                             '0 - Sair\n')
            if decision == '0':
                return
            else:
                if decision == '1':
                    self.buscarProdutos()
                elif decision == '2':
                    self.adicionarProduto()
                else:
                    print('Opção inválida.')

    def buscarProdutos(self):
        cur = Connection().getCur()
        cur.execute('SELECT * FROM produto')

        print('----------------------')
        print('Código - Nome')
        print('----------------------')
        for id, nome in cur:
            print(f'{id} - {nome}')
        print('----------------------')

    def adicionarProduto(self):
        nomeProduto = input('Informe o nome do produto: ')

        try:
            cur = Connection().getCur()

            cur.execute(f'INSERT INTO produto (descricao) VALUES (?)', [(nomeProduto)])

            print('Produto inserido com sucesso!')
        except mariadb.Error as e:
            print(f'Problema ao realizar a operação: {e}')