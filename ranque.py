import pandas as pd
from collections import Counter

def ranquearIphones():
    # Carregar os dados dos arquivos CSV
    df_iphones = pd.read_csv('iphones.csv')
    df_iphones_menor_preco = pd.read_csv('iphonesMenorPreco.csv')
    df_iphones_melhor_avaliado = pd.read_csv('iphonesMelhorAvaliado.csv')

    # Combinar todas as listas em uma única lista
    listaGeral = pd.concat([df_iphones, df_iphones_menor_preco, df_iphones_melhor_avaliado])

    # Contar a frequência de cada item (considerando o nome, preço e link do produto)
    repeticoes = Counter(tuple(row) for row in listaGeral[['Nome', 'Preço', 'Link']].values)

    # Ordenar os itens pela frequência
    itensRanqueados = repeticoes.most_common()

    # Converter para DataFrame
    df_rank = pd.DataFrame(itensRanqueados, columns=['Item', 'Frequência'])
    df_rank[['Nome', 'Preço', 'Link']] = pd.DataFrame(df_rank['Item'].tolist(), index=df_rank.index)
    df_rank.drop(columns=['Item'], inplace=True)

    # Salvar o resultado em um novo arquivo CSV
    df_rank.to_csv('iphonesRanqueados.csv', index=False)

