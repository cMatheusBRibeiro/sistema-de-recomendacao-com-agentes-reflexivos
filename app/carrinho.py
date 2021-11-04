from produtos import Produtos
from agente import Agente
from datetime import datetime
from connection import Connection

class Carrinho:
    def __init__(self):
        self.produtos = []

    def open(self):
        print('----------------------')
        print('Abrindo carrinho.')
        print('----------------------')
        while True:
            print('Selecione uma das opcoes a seguir.')
            decision = input('1 - Listar produtos\n'
                             '2 - Adicionar produto\n'
                             '3 - Remover produto\n'
                             '4 - Finalizar compra\n'
                             '0 - Sair\n')
            if decision == '0':
                return
            else:
                if decision == '1':
                    self.listarProdutos()
                elif decision == '2':
                    self.adicionarProduto()
                elif decision == '3':
                    self.removerProduto()
                elif decision == '4':
                    self.finalizarCompra()
                else:
                    print('Opção inválida.')

    def listarProdutos(self):
        print('----------------------')
        print('Produtos presentes no carrinho.')
        print('Código - Nome')
        print('----------------------')

        if self.produtos.__len__() == 0:
            print('Carrinho vazio.')
        else:
            for produto in self.produtos:
                print(f"{produto['codigo']} - {produto['descricao']}")

        print('----------------------')

    def adicionarProduto(self):
        Produtos().buscarProdutos()
        print('----------------------')
        codigo = input('Informe o código do produto a ser inserido no carrinho: ')

        for produto in self.produtos:
            if str(produto['codigo']) == codigo:
                print('Produto já foi adicionado ao seu carrinho.')
                return

        produto = Produtos().buscarProdutoPeloId(codigo)
        self.produtos.append(produto)
        print(f"O produto '{produto['descricao']}' foi adicionado com sucesso!")
        print('----------------------')

    def removerProduto(self):
        self.listarProdutos()
        codigo = input('Informe o código do produto a ser removido: ')
        remocao = False

        for produto in self.produtos:
            if str(produto['codigo']) == codigo:
                self.produtos.remove(produto)
                remocao = True

        if remocao:
            print('Produto removido com sucesso!')
        else:
            print('O produto informado não estava estava presente em seu carrinho.')
        print('----------------------')

    def finalizarCompra(self):
        novosProdutos = Agente().analisarCompra(self.produtos)
        for produto in novosProdutos:
            self.produtos.append(Produtos().buscarProdutoPeloId(produto))

        self.adicionarTransacao()

        print('----------------------')
        print('Finalizando compra.')
        print('----------------------')
        print('----------------------')
        print('Produtos comprados:')
        for produto in self.produtos:
            print(f"{produto['codigo']} - {produto['descricao']}")
        self.produtos = []
        print('----------------------')
        print('----------------------')
        print('Volte sempre :)')
        print('----------------------')
        print('----------------------')

    def adicionarTransacao(self):
        now = datetime.now()
        cur = Connection().getCur()
        cur.execute('INSERT INTO transacao (data, periodo_dia, weekday_weekend) VALUES (?, ?, ?)',
                    (now, 'morning', 'weekend'))
        idTransacao = cur.lastrowid
        for produto in self.produtos:
            cur.execute('INSERT INTO produtotransacao (idProduto, idTransacao) VALUES (?, ?)',
                        (produto['codigo'], idTransacao))