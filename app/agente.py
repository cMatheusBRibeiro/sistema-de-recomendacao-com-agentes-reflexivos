import mariadb
from connection import Connection
from produtos import Produtos

class Agente:
    def analisarCompra(self, carrinho):
        cur = Connection().getCur()
        try:
            cur.execute('SELECT * FROM recomendacao')
            produtosRecomendados = []
            recomendacoes = []
            for recomendacao in cur:
                recomendacoes.append(recomendacao)

            for recomendacao in recomendacoes:
                cur.execute('SELECT idProduto FROM produtorecomendacao WHERE idRecomendacao = (?)',
                            (str(recomendacao[0]), ))
                recomendar = True
                for idProduto in cur:
                    if not self.verificarExistenciaProduto(carrinho, idProduto[0]):
                        recomendar = False

                if recomendar and not self.verificarExistenciaProduto(carrinho, recomendacao[1]):
                    produtosRecomendados.append(recomendacao[1])

            novasAdicoes = []
            print(produtosRecomendados)

            if produtosRecomendados.__len__() > 0:
                print('----------------------')
                print('Gostaria de adicionar os seguintes produtos em seu carrinho?')
                print('----------------------')
                for idProdutoRecomendado in produtosRecomendados:
                    produto = Produtos().buscarProdutoPeloId(idProdutoRecomendado)
                    print(f"{produto['codigo']} - {produto['descricao']}")
                print('----------------------')
                decision = input('1 - Sim\n'
                                 '2 - Não\n')
                if decision == '1':
                    print('Quais? (digite 0 para sair)')
                    while True:
                        opcao = input('Informe o código do produto: ')
                        if opcao == '0':
                            break
                        else:
                            if opcao in novasAdicoes:
                                print('Produto já foi adicionado.')
                            elif int(opcao) not in produtosRecomendados:
                                print('Este produto não está presente na lista.')
                            else:
                                novasAdicoes.append(opcao)
                                print('Produto adicionado.')
            return novasAdicoes
        except mariadb.Error as e:
            print(f'Problema ao executar tal operacao: {e}')

    def verificarExistenciaProduto(self, carrinho, produto):
        produtoExiste = False
        for item in carrinho:
            if str(item['codigo']) == str(produto):
                produtoExiste = True
        return produtoExiste