#-*- coding:utf-8 -*-
import time
from selenium import webdriver
import schedule
import os
from bs4 import BeautifulSoup

cont_cidades = 0

cont_empresas = 0

cont_cliques = 0

cont_cliques_por_cidade = 0

def doar():

    try:

        global cont_cliques

        global cont_empresas

        global cont_cidades

        global cont_cliques_por_cidade

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.binary_location = '/usr/bin/google-chrome'
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)

        url = "http://cliquealimentos.com.br/Inicial"

        driver.get(url)

        time.sleep(3)

        driver.find_element_by_css_selector('[onclick*=ShowCidades]').click()

        time.sleep(3)

        cidades = driver.find_elements_by_css_selector('[onclick*=LoadEmpresas]')

        cidades[cont_cidades].click()

        quant_cidades = (len(cidades))

        time.sleep(3)

        empresas = driver.find_elements_by_css_selector('[onclick*=EnviaDoacao]')
        
        quant_empresas = (len(empresas))

        empresas[cont_empresas].click()

        time.sleep(3)

        html_content_empresas = empresas[cont_empresas].get_attribute("outerHTML")
        html_content_cidades = cidades[cont_cidades].get_attribute("outerHTML")

        soup_empresas = BeautifulSoup(html_content_empresas, 'html.parser')
        soup_cidades = BeautifulSoup(html_content_cidades, 'html.parser')

        title_empresa = soup_empresas.img['title']
        title_cidade = soup_cidades.text

        cont_cliques = cont_cliques +1
        cont_empresas= cont_empresas+1
        cont_cliques_por_cidade = cont_cliques_por_cidade +1

        print(f'A doação número {cont_cliques} foi realizada com sucesso por {title_empresa} em {title_cidade}.')

        if cont_cliques_por_cidade % quant_empresas == 0:
            
            cont_cidades = cont_cidades +1

            cont_empresas = 0
            cont_cliques_por_cidade = 0
        
        if cont_cidades == quant_cidades:
            cont_cidades = 0
             
            
        driver.quit()

    except Exception as e:

        print(e)

        print("Houve algum problema. Repetindo processo.")

        driver.quit()

        doar()

schedule.every(2).seconds.do(doar)

while 1:
    schedule.run_pending()
    time.sleep(1) 