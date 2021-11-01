from connection import Connection
import matplotlib.pyplot as plt
import numpy as np

cur = Connection().getCur()

def buscarQuantidadeDeItensExistentes():
    cur.execute('SELECT count(*) FROM produto')
    total = None
    for dado in cur:
        total = dado[0]
    print('Existem ' + str(total) + ' produtos diferentes no mercado.')

def buscarQuantidadeDeVendasDosItens(titulo, periodo = None):
    if periodo != None:
        cur.execute("SELECT descricao, count(*) FROM produto p, produtotransacao pt, transacao t WHERE p.idProduto = pt.idProduto AND pt.idTransacao = t.idTransacao AND t.periodo_dia = ? GROUP BY p.descricao",
                    (periodo,))
    else:
        cur.execute("SELECT descricao, count(*) FROM produto p, produtotransacao pt WHERE p.idProduto = pt.idProduto GROUP BY p.descricao")

    labels = []
    data = []
    for dado in cur:
        labels.append(dado[0])
        data.append(dado[1])
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects = ax.bar(x - width / 2, data, width, label='Produto')
    ax.set_ylabel('Total de Vendas')
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.bar_label(rects, padding=3)

    fig.tight_layout()
    plt.show()

def identificarAssociacoes():
    cur.execute("SELECT idTransacao FROM transacao")
    transacoes = []
    [transacoes.append(transacao[0]) for transacao in cur]
    produtosTransacao = []
    for transacao in transacoes:
        cur.execute("SELECT p.idProduto "
                    "FROM produto p, produtotransacao pt "
                    "WHERE p.idProduto = pt.idProduto AND pt.idTransacao = ?",
                    (transacao,))
        produtos = []
        for produto in cur:
            produtos.append(produto[0])
        produtosTransacao.append(produtos)
        print(produtos)

'''
buscarQuantidadeDeItensExistentes()
buscarQuantidadeDeVendasDosItens('Total de vendas por produto')
buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da manhã', 'morning')
buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da tarde', 'afternoon')
buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da noite', 'evening')
'''

identificarAssociacoes()