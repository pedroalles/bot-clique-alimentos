import time
from selenium import webdriver
import schedule
import os
from bs4 import BeautifulSoup

cont_empresas = 0

cont_cliques = 0

def doar():

    try:

        global cont_cliques

        global cont_empresas

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.binary_location = '/usr/bin/google-chrome'
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)

        url = "http://cliquealimentos.com.br/Inicial"

        driver.get(url)

        time.sleep(3)

        driver.find_element_by_css_selector('[onclick*=ShowCidades]').click()

        time.sleep(3)

        driver.find_element_by_xpath("//*[@id='DoeCidades']/div/table/tbody/tr//*[text()='Porto Alegre']").click()

        time.sleep(3)

        empresas = driver.find_elements_by_css_selector('[onclick*=EnviaDoacao]')
        
        quant_empresas = (len(empresas))

        empresas[cont_empresas].click()

        time.sleep(3)

        html_content = empresas[cont_empresas].get_attribute("outerHTML")

        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.img['title']

        cont_cliques = cont_cliques +1

        cont_empresas= cont_empresas+1

        print(f'A doaçao número {cont_cliques} foi realizada com sucesso por: {title}')

        if cont_cliques % quant_empresas == 0:

            cont_empresas = 0

        driver.quit()

    except:

        print("Houve algum problema. Repetindo processo.")
        # driver.quit()
        doar()

schedule.every(3).seconds.do(doar)

while 1:

    schedule.run_pending()

    time.sleep(1) 