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
    # O suporte representa o valor, em percentual, da presença dos dois conjuntos dividido pelo total de transações. No caso,
    # se os dois produtos passados estiver presente na transação já será o suficiente para contabilizar.
    sup = 0
    for transacao in transacoes:
        # Verifica a presença de os dos dois itens na transação
        if (Ix.union(Iy)).issubset(transacao):
            sup += 1
    # Calcula o percentual do suporte perante a lista de transações
    sup = sup/len(transacoes)
    return sup

def confidence(Ix, Iy, transacoes):
    # A confiança representa o valor, em percentual, do seguinte procedimento:
    # - se X estiver presente na transação, conta +1
    # - se nessa mesma transação estiver presente o Y, conta +1 para os dois, indicando que nessa transação o cliente
    # pegou o produto X e também o Y
    # - caso contrário, X esteja presente e Y não, indica que o cliente pegou o produto X mas não o Y
    # o percentual se dá pela a quantidade de vezes que o cliente pegou os dois produtos (X e Y) dividido pela quantidade
    # de vezes que o cliente pegou o produto X.
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
    # Inicia a lista de regras filtradas
    prune_ass_rules = []
    for ar in ass_rules:
        # Verifica se a regra atende aos valores mínimos
        if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
            prune_ass_rules.append(ar)
    # Retorno das regras filtradas
    return prune_ass_rules

def apriori(produtos, transacoes, min_sup, min_conf):
    # Criando lista de regras que serão separadas em 2, a primeira sendo as regras de cada produto, a segunda as regras
    # de recomendação.
    ass_rules = []
    # Criando a lista de regras de cada produto
    ass_rules.append([])
    for produto in produtos:
        # Calculando o suporte do produto
        sup = support({produto}, {produto}, transacoes)
        # Adicionando a regra do produto na primeira lista
        ass_rules[0].append({'rule': produto, \
                             'support': sup, \
                             'confidence': 1})
    # Filtrando as regras de cada produto buscando todos os que atendem aos requisitos minimos
    ass_rules[0] = prune(ass_rules[0], min_sup, min_conf)

    # Iniciando a lista de regras de recomendação
    ass_rules.append([])

    # Pegando o primeiro produto
    for produto_1 in ass_rules[0]:
        # Pegando o segundo produto
        for produto_2 in ass_rules[0]:
            # Verificando se os 2 produtos são iguais
            if produto_1['rule'] != produto_2['rule']:
                # Nomeando a regra de recomendação dos dois produtos
                rule = str(produto_1['rule']) + '_' + str(produto_2['rule'])

                # Criando o conjunto do primeiro produto
                Ix = {produto_1['rule']}

                # Criando o conjunto do segundo produto
                Iy = {produto_2['rule']}

                # Calculando o suporte e a confiança da recomendação, sendo o produto 1 estando no carrinho e o 2 a ser
                # recomendado
                sup = support(Ix, Iy, transacoes)
                conf = confidence(Ix, Iy, transacoes)

                # Adicionando a listagem de recomendação
                ass_rules[1].append({'rule': rule, \
                                     'support': sup, \
                                     'confidence': conf})
    # Filtrando as regras de recomendação, buscando os que apresentem os valores minimos de suporte e confiança
    ass_rules[1] = prune(ass_rules[1], min_sup, min_conf)

    # Retornando as regras
    return ass_rules

def identificarAssociacoes():
    # Buscando transações
    cur.execute("SELECT idTransacao FROM transacao")
    transacoesBruto = []
    [transacoesBruto.append(transacao[0]) for transacao in cur]
    transacoes = []
    for transacao in transacoesBruto:
        # Buscando os produtos referente a transação
        cur.execute("SELECT p.idProduto "
                    "FROM produto p, produtotransacao pt "
                    "WHERE p.idProduto = pt.idProduto AND pt.idTransacao = ?",
                    (transacao,))
        produtos = []
        for produto in cur:
            produtos.append(produto[0])
        transacoes.append(produtos)

    # Buscando a lista de produtos presente no banco
    cur.execute("SELECT idProduto FROM produto")
    produtos = []
    [produtos.append(produto[0]) for produto in cur]

    # Chamando apriori
    return apriori(produtos, transacoes, 0.09, 0.15) # os parâmetros 0.09 e 0.15 são os valores mínimos de, respectivamente, suporte e confiança

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
