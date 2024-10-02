import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import textwrap
import os


def printe(texto, nivel=0):
    print() if nivel == 0 else None
    # Adiciona indentação com textwrap
    texto_formatado = textwrap.indent(texto, '\t' * nivel)

    # Imprime o texto formatado
    print(texto_formatado)

#scp root@62.72.9.249:/root/ikrazy/velas_analise.db C:\Users\dodoc\PycharmProjects\aposta\


conn = sqlite3.connect("velas_analise.db")

conn.row_factory = sqlite3.Row
cur = conn.cursor()
df = pd.read_sql_query("SELECT * FROM crashs", conn)
conn.close()

data_inicial, data_final = df.iloc[1]['data_hora'] , df.iloc[-1]['data_hora']
data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d %H:%M:%S.%f")
data_final = datetime.strptime(data_final, "%Y-%m-%d %H:%M:%S.%f")
tempo_corrido = round((data_final - data_inicial).total_seconds() / 3600, 1)
qtd_total_partidas = df.shape[0]

printe("Informações Básicas:")
printe(f"O arquivo contém um total de {tempo_corrido} horas de partidas crash.", 1)
printe(f"Total de partidas: {qtd_total_partidas}", 1)

def contar_sequencia(df, valor_vela = 1.50, qtd_sequencia_esperada = 5):

    sequencias_contadas = 0
    contador = 0
    for indice, linha in df.iterrows():

        if linha['crash'] <= valor_vela:
            contador += 1

        else:
            contador = 0  # reseta o contador
            continue
        if contador == qtd_sequencia_esperada:
            sequencias_contadas += 1


    printe(f"Uma sequência de {qtd_sequencia_esperada} velas abaixo da vela {valor_vela}x, ocorreram {sequencias_contadas} vezes nesse período de {tempo_corrido} horas de jogo.", 2)


#  Análisar sequencias
velas = [1.10, 1.20, 1.30, 1.40, 1.49, 1.50, 2.50]
for vela in velas:
    valor_vela = vela
    printe(f"Análise de sequências consecutivas {valor_vela}x")
    for i in range(1, 10):
        contar_sequencia(df, valor_vela=valor_vela, qtd_sequencia_esperada=i)





