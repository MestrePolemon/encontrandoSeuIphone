from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

def capturar_produtos(driver):
    lista_iphones = []
    for page in range(1, 4):  # Itera sobre as 3 primeiras páginas
        iphones = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Hits_ProductCard__Bonl_'))
        )

        # Verificação do tamanho da lista de produtos
        print(f"Número de produtos encontrados na página {page}: {len(iphones)}")

        for iphone in iphones:
            link_element = iphone.find_element(By.TAG_NAME, 'a')
            link = link_element.get_attribute('href') if link_element else "Link não encontrado"

            nome = iphone.find_element(By.CSS_SELECTOR, '[data-testid="product-card::name"]').text

            try:
                vendedor = iphone.find_element(By.CLASS_NAME,
                                               'Text_Text__ARJdp.Text_MobileLabelXs__dHwGG.Text_MobileLabelSAtLarge__m0whD.ProductCard_ProductCard_BestMerchant__JQo_V').text
            except:
                vendedor = "Vendedor não encontrado"

            preco = iphone.find_element(By.CLASS_NAME, 'Text_Text__ARJdp.Text_MobileHeadingS__HEz7L').text

            print(nome, preco, vendedor, link)
            lista_iphones.append([nome, preco, vendedor, link])

        if page < 3:  # Navega para a próxima página apenas se não estiver na última página
            try:
                proximaPagina = driver.find_element(By.CSS_SELECTOR, '[data-testid="page-next"]')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proximaPagina)
                sleep(1)
                proximaPagina.click()
                sleep(5)
            except Exception as e:
                print(f"Não foi possível encontrar o link de próxima página: {e}")
                break
    return lista_iphones

driver = webdriver.Chrome()
driver.get('https://www.zoom.com.br/')
sleep(5)

produtos = driver.find_element(By.TAG_NAME, 'nav')
clicar = produtos.find_element(By.XPATH, '//a[@href="/celular/apple"]')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clicar)
sleep(1)
clicar.click()

sleep(5)

# Captura os produtos antes de aplicar o filtro
lista_iphones = capturar_produtos(driver)
df = pd.DataFrame(lista_iphones, columns=['Nome', 'Preço', 'Vendedor', 'Link'])
df.to_csv('iphones.csv', index=False)

# Volta para a primeira página
driver.get('https://www.zoom.com.br/celular/apple')
sleep(5)

# Aplica o filtro de "menor preço"
filtrar = driver.find_element(By.TAG_NAME, 'select')
filtrar.click()
sleep(1)
filtrar.find_element(By.XPATH, '//option[text()="Menor preço"]').click()
sleep(5)

# Captura os produtos após aplicar o filtro
lista_iphones_menor_preco = capturar_produtos(driver)
df_menor_preco = pd.DataFrame(lista_iphones_menor_preco, columns=['Nome', 'Preço', 'Vendedor', 'Link'])
df_menor_preco.to_csv('iphonesMenorPreco.csv', index=False)

driver.get('https://www.zoom.com.br/celular/apple')
sleep(5)

filtrar = driver.find_element(By.TAG_NAME, 'select')
filtrar.click()
sleep(1)
filtrar.find_element(By.XPATH, '//option[text()="Melhor avaliado"]').click()
sleep(5)

# Captura os produtos após aplicar o filtro
lista_iphones_melhor_avaliado = capturar_produtos(driver)
df_melhor_avaliado = pd.DataFrame(lista_iphones_melhor_avaliado, columns=['Nome', 'Preço', 'Vendedor', 'Link'])
df_melhor_avaliado.to_csv('iphonesMelhorAvaliado.csv', index=False)

driver.close()

from ranque import ranquearIphones

ranquearIphones()

from melhoresIphones import melhoresIphones

melhoresIphones()