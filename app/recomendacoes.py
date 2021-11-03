import mariadb

from connection import Connection
from produtos import Produtos
from analisarTransacoes import identificarAssociacoes


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
                             '4 - Gerar recomendacoes\n'
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
                elif decision == '4':
                    self.atualizarRecomendacoesAutomaticamente()
                else:
                    print('Opção inválida.')

    def buscarRecomendacoes(self):
        cur = Connection().getCur()

        cur.execute('SELECT * FROM recomendacao')
        recomendacoesSQL = []
        [recomendacoesSQL.append(recomendacao) for recomendacao in cur]
        recomendacoes = []
        for idRecomendacao, idProduto in recomendacoesSQL:
            print(idRecomendacao, idProduto)
            cur.execute(f'SELECT p.descricao produto FROM produto p, produtorecomendacao pr '
                        f'WHERE pr.idRecomendacao = (?) AND pr.idProduto = p.idProduto', (idRecomendacao, ))
            produtosAnalisados = []
            for produto in cur:
                produtosAnalisados.append(produto[0])

            cur.execute(f'SELECT p.descricao produto FROM produto p WHERE p.idProduto = (?)',
                        (idProduto, ))
            produtoRecomendado = ''
            for produto in cur:
                produtoRecomendado = produto[0]

            recomendacoes.append({
                'codigo': idRecomendacao,
                'produtos': produtosAnalisados,
                'recomendacao': produtoRecomendado
            })

        print('----------------------')
        print('Código: Produtos -> Recomendacao')
        print('----------------------')
        for recomendacao in recomendacoes:
            print(f'{recomendacao["codigo"]}: {", ".join(recomendacao["produtos"])} -> {recomendacao["recomendacao"]}')

        print('----------------------')

    def adicionarRecomendacao(self):
        Produtos().buscarProdutos()
        produtosAnalisado = input('Informe os códigos dos produtos a serem analisados (separado por espaço): ').split()
        produtoRecomendado = input('Informe o códuigo do produto a ser recomendado: ')

        cur = Connection().getCur()

        try:
            cur.execute(f'INSERT INTO recomendacao (produtoRecomendado) VALUES (?)',
                        (produtoRecomendado,))
            idRecomendacao = cur.lastrowid
            for produto in produtosAnalisado:
                cur.execute(f'INSERT INTO produtorecomendacao (idRecomendacao, idProduto) VALUES (?, ?)',
                            (idRecomendacao, produto))
        except mariadb.Error as e:
            print(f'Problema ao realizar a operação: {e}')

    def excluirRecomendacao(self):
        self.buscarRecomendacoes()
        codigo = input('Código da recomendacao a ser excluída: ')
        cur = Connection().getCur()

        try:
            cur.execute(f'DELETE FROM produtorecomendacao WHERE idRecomendacao = {codigo}')
            cur.execute(f'DELETE FROM recomendacao WHERE idRecomendacao = {codigo}')
            print('Recomendação excluída com sucesso!')
        except mariadb.Error as e:
            print(f'Problema ao realizar a operação: {e}')

    def atualizarRecomendacoesAutomaticamente(self):
        associacoesGeradas = identificarAssociacoes()
        cur = Connection().getCur()
        for associacao in associacoesGeradas[1]:
            idProdutos = associacao['rule'].split('_')
            try:
                cur.execute(f'INSERT INTO recomendacao (produtoRecomendado) VALUES (?)',
                            (idProdutos[0],))
                idRecomendacao = cur.lastrowid
                cur.execute(f'INSERT INTO produtorecomendacao (idRecomendacao, idProduto) VALUES (?, ?)',
                            (idRecomendacao, idProdutos[1]))
            except mariadb.Error as e:
                print(f'Problema ao realizar a operação: {e}')
        print('As novas recomendações foram geradas')