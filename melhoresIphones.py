import pandas as pd
from bs4 import BeautifulSoup
import requests

def obterDescricao(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    descricao = soup.find('div', {'class': 'DetailsContent_MasonryColumn__RTZdN'}).text.strip()
    return descricao

def melhoresIphones():
    # Carregar o arquivo de iPhones ranqueados
    df_rank = pd.read_csv('iphonesRanqueados.csv')

    # Selecionar as colunas necessárias
    df_rank = df_rank[['Nome', 'Preço', 'Link']]

    # Criar a coluna 'Descrição' com as configurações dos iPhones
    df_rank['Descrição'] = df_rank['Link'].apply(obterDescricao)

    # Selecionar os top 5 iPhones ranqueados
    top5 = df_rank.head(5)

    # Salvar o resultado em um novo arquivo CSV
    top5.to_csv('top5IphonesComConfiguracoes.csv', index=False)

