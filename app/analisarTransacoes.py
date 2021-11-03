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

def support(Ix, Iy, transacoes):
    sup = 0
    for transacao in transacoes:
        if (Ix.union(Iy)).issubset(transacao):
            sup += 1
    sup = sup/len(transacoes)
    return sup

def confidence(Ix, Iy, transacoes):
    Ix_count = 0
    Ixy_count = 0
    for transacao in transacoes:
        if Ix.issubset(transacao):
            Ix_count += 1
            if (Ix.union(Iy)).issubset(transacao):
                Ixy_count += 1
    conf = Ixy_count / Ix_count
    return conf

def prune(ass_rules, min_sup, min_conf):
    prune_ass_rules = []
    for ar in ass_rules:
        if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
            prune_ass_rules.append(ar)
    return prune_ass_rules

def apriori(produtos, transacoes, min_sup, min_conf):
    ass_rules = []
    ass_rules.append([])
    for produto in produtos:
        sup = support({produto}, {produto}, transacoes)
        ass_rules[0].append({'rule': produto, \
                             'support': sup, \
                             'confidence': 1})
    ass_rules[0] = prune(ass_rules[0], min_sup, min_conf)
    ass_rules.append([])
    for produto_1 in ass_rules[0]:
        for produto_2 in ass_rules[0]:
            if produto_1['rule'] != produto_2['rule']:
                rule = str(produto_1['rule']) + '_' + str(produto_2['rule'])
                Ix = {produto_1['rule']}
                Iy = {produto_2['rule']}
                sup = support(Ix, Iy, transacoes)
                conf = confidence(Ix, Iy, transacoes)
                ass_rules[1].append({'rule': rule, \
                                     'support': sup, \
                                     'confidence': conf})
    ass_rules[1] = prune(ass_rules[1], min_sup, min_conf)
    return ass_rules

def identificarAssociacoes():
    # Buscando transações
    cur.execute("SELECT idTransacao FROM transacao")
    transacoesBruto = []
    [transacoesBruto.append(transacao[0]) for transacao in cur]
    transacoes = []
    for transacao in transacoesBruto:
        cur.execute("SELECT p.idProduto "
                    "FROM produto p, produtotransacao pt "
                    "WHERE p.idProduto = pt.idProduto AND pt.idTransacao = ?",
                    (transacao,))
        produtos = []
        for produto in cur:
            produtos.append(produto[0])
        transacoes.append(produtos)

    # Buscando produtos
    cur.execute("SELECT idProduto FROM produto")
    produtos = []
    [produtos.append(produto[0]) for produto in cur]

    # Chamando apriori
    return apriori(produtos, transacoes, 0.09, 0.15)

def gerarRelatorio():
    buscarQuantidadeDeVendasDosItens('Total de vendas por produto')

def gerarRelatorioDaManha():
    buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da manhã', 'morning')

def gerarRelatorioDaTarde():
    buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da tarde', 'afternoon')

def gerarRelatorioDaNoite():
    buscarQuantidadeDeVendasDosItens('Total de vendas por produto no período da noite', 'evening')

def totalItensExistentes():
    buscarQuantidadeDeItensExistentes()
