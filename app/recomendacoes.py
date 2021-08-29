import mariadb

from connection import Connection
from produtos import Produtos

class Recomendacoes:
    def open(self):
        print('----------------------')
        print('Abrindo recomendacoes.')
        print('----------------------')

        while True:
            print('Selecione uma das opcoes a seguir.')
            decision = input('1 - Buscar recomendacoes\n'
                             '2 - Adicionar recomendacao\n'
                             '3 - Excluir recomendacao\n'
                             '0 - Sair\n')
            if decision == '0':
                return
            else:
                if decision == '1':
                    self.buscarRecomendacoes()
                elif decision == '2':
                    self.adicionarRecomendacao()
                elif decision == '3':
                    self.excluirRecomendacao()
                else:
                    print('Opção inválida.')

    def buscarRecomendacoes(self):
        cur = Connection().getCur()

        cur.execute('SELECT '
                    '   r.idRecomendacao codigo, '
                    '   pa.descricao analisado, '
                    '   pr.descricao recomendado '
                    'FROM'
                    '   produto pa, '
                    '   produto pr, '
                    '   recomendacao r '
                    'WHERE '
                    '   r.produtoAnalisado = pa.idProduto AND '
                    '   r.produtoRecomendado = pr.idProduto ')

        print('----------------------')
        print('Código: Produto analisado -> Produto recomendado')
        print('----------------------')
        for codigo, analisado, recomendado in cur:
            print(f'{codigo}: {analisado} -> {recomendado}')
        print('----------------------')

    def adicionarRecomendacao(self):
        Produtos().buscarProdutos()
        produtoAnalisado = input('Informe o código do produto a ser analisado: ')
        produtoRecomendado = input('Informe o códuigo do produto a ser recomendado: ')

        cur = Connection().getCur()

        try:
            cur.execute(f'INSERT INTO recomendacao (produtoAnalisado, produtoRecomendado) VALUES (?, ?)',
                        (produtoAnalisado, produtoRecomendado))
        except mariadb.Error as e:
            print(f'Problema ao realizar a operação: {e}')

    def excluirRecomendacao(self):
        self.buscarRecomendacoes()
        codigo = input('Código da recomendacao a ser excluída: ')
        cur = Connection().getCur()

        try:
            cur.execute(f'DELETE FROM recomendacao WHERE idRecomendacao = {codigo}')
            print('Recomendação excluída com sucesso!')
        except mariadb.Error as e:
            print(f'Problema ao realizar a operação: {e}')