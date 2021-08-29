import mariadb
from connection import Connection
from produtos import Produtos

class Agente:
    def analisarCompra(self, carrinho):
        cur = Connection().getCur()
        try:
            cur.execute('SELECT pa.idProduto, pr.idProduto FROM produto pa, produto pr, recomendacao r '
                        'WHERE r.produtoAnalisado = pa.idProduto AND r.produtoRecomendado = pr.idProduto')
            produtosRecomendados = []
            for analisado, recomendado in cur:
                if self.verificarExistenciaProduto(carrinho, analisado) and not self.verificarExistenciaProduto(carrinho, recomendado):
                    produtosRecomendados.append(recomendado)

            novasAdicoes = []

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