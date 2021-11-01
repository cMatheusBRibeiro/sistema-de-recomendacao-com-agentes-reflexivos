from connection import Connection
import pandas as pd
from io import StringIO

cur = Connection().getCur()

def adicionarProduto(nomeProduto):
    cur.execute("SELECT idProduto id FROM produto WHERE descricao = ?",
                (nomeProduto,))
    id = None
    for linha in cur:
        id = linha[0]

    if id == None:
        cur.execute("INSERT INTO produto (descricao) VALUES (?)",
                    (nomeProduto,))
        print(cur.lastrowid)
        id = cur.lastrowid

    return id

def adicionarTransacoes(transacoes):
    for i, row in transacoes.iterrows():
        row['date_time'] = pd.Timestamp.to_pydatetime(pd.to_datetime(row['date_time']))

        idTransacao = None
        cur.execute("SELECT * FROM transacao WHERE idTransacao = ?", (row['Transaction'],))
        for linha in cur:
            idTransacao = linha[0]

        if idTransacao == None:
            cur.execute("INSERT INTO transacao (idTransacao, data, periodo_dia, weekday_weekend) VALUES (?,?,?,?)",
                        (row['Transaction'], row['date_time'], row['period_day'], row['weekday_weekend']))
            idTransacao = row['Transaction']

        idProduto = adicionarProduto(row['Item'])
        cur.execute("INSERT INTO produtoTransacao (idProduto, idTransacao) VALUES (?,?)",
                    (idProduto, idTransacao))


caminhoArquivo = input('Informe a localização do CSV para importação: ')
arquivo = ''
for linha in open(caminhoArquivo, 'r').read():
    arquivo = arquivo + linha

transacoes = pd.read_csv(StringIO(arquivo), dtype=object)

adicionarTransacoes(transacoes)