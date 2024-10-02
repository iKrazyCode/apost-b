from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
import re
import os
from selenium.common.exceptions import TimeoutException
import random
import requests
import re
import logging
logging.basicConfig(level=logging.INFO, filename="log_demo.txt")


class BlazerCrash:

    def __init__(self, email, senha, banca_inicial, headless=False):
        """
        Classe onde fica o inicializador do webdriver e toda a sequencia de execução do código
        """
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless") if headless is True else None
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-webgl")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 7020)

        # Config básica
        self.valor_limite_vela = 1.50

        self.login(email, senha)
        self.__btn_normal()

        # Cria o arquivo se não existir
        try:
            with open("demo_saldo.txt", "x") as fp:
                fp.write(f"{float(banca_inicial)}")
        except:
            logging.info("Carregando arquivo com saldo já existente...")


    def login(self, email, senha):
        driver = self.driver
        wait = self.wait
        logging.info("Fazendo login...")
        try:
            # Fechar obstaculos
            game_link = driver.get('https://blaze-4.com/pt/games/crash_2')

            sleep(1)  # 10.10 deixa esse sleep para poder carregar o banner inteiro do AVIATOR

            logging.info("Login feito...")
            return True

        except:
            logging.info("Falha no login.")
            raise Exception


    def __btn_normal(self):
        """
        Função que clica no botão de automático.
        Entra no iframe e saí ao final do código.
        para manter o padrão default da página. para ações futuras
        :return:
        """
        driver = self.driver
        wait = self.wait
        

        try:
            normal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-controller__tabs > button.grey.selected")))
            normal.click()
            resp = True
        except:
            resp = False

        
        return resp



    def __selecionar_valor_dinheiro(self, valor):
        """
        Função que seleciona os gales: 1.50
        Entra no iframe e saí ao final do código.
        para manter o padrão default da página. para ações futuras
        :return:
        """
        driver = self.driver
        wait = self.wait
        
        #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature.auto-game > div.bet-block > app-spinner > div > div.input > input")))

        try:
            input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#crash-controller > div > div.crash-controller__panel > div > div.inputs-wrapper > div.bet-input-row.bet-input-row--regular-bets > div > div.input-field-wrapper > input")))
            [input.send_keys(Keys.BACKSPACE) for i in range(8)]
            input.send_keys(valor)
            resp = True
        except:
            resp = False

        
        return resp

    def __selecionar_valor_limite_vela(self, vela):
        """
        Função que seleciona os gales: 1.50
        Entra no iframe e saí ao final do código.
        para manter o padrão default da página. para ações futuras
        :return:
        """
        driver = self.driver
        wait = self.wait

        inputs = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-controller > div > div.crash-controller__panel > div > div.inputs-wrapper > div:nth-child(2) > div.input-wrapper > input")))
        inputs.click()
        [inputs.send_keys(Keys.BACKSPACE) for i in range(8)]
        inputs.send_keys(vela)
        resp = True
        return resp

    def __clicar_apostar(self):
        """
        Função que clica no botão de automático.
        Entra no iframe e saí ao final do código.
        para manter o padrão default da página. para ações futuras
        :return:
        """
        driver = self.driver
        wait = self.wait

        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#crash-controller > div > div.crash-controller__panel > div > div.place-bet > button")))
        btn.click()
        resp = True
        
        return resp


    def __wait_and_get_last_crash_by_navbar(self):
        driver = self.driver
        wait = self.wait

        crash_before1, crash_before2 = [
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-recent-v2 > div > div.entries > div:nth-child(1)"))),
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-recent-v2 > div > div.entries > div:nth-child(2)")))
        ]

        while True:
            crash_atual1, crash_atual2 = [
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-recent-v2 > div > div.entries > div:nth-child(1)"))),
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-recent-v2 > div > div.entries > div:nth-child(2)")))
            ]

            if crash_before1 == crash_atual1 and crash_before2 == crash_atual2:
                continue  # mudar para break talvez
            else:
                break

        #  Pegar o crash
        last_crash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-main-canvas-v2 > div > div.crash-board > div:nth-child(3) > div > div.crash-canvas__payout-title-and-payout-value > p")))
        last_crash = float(last_crash.text.replace("X", "").replace(",", "."))

        return last_crash


    def __wait_and_get_last_crash(self):
        """
        Responsável por esperar até o crash, e retorna o ultimo crash atual

        OBS: Começa a partir do foguete voando, e pega quando ele crasha. NÃO VERIFICA A SUBIDA DO FOGUETE
        :return:
        """
        driver = self.driver
        wait = self.wait


        #  Esperar o foguete subir
        string = "crash-animation-up"
        #wait.until(EC.text_to_be_present_in_element_attribute((By.ID, "crash-main-canvas-v2"), atributo, string))
        elem1 = wait.until(
            lambda driver: re.search(fr".*{string}(?!-).*", wait.until(EC.presence_of_element_located((By.ID, "crash-main-canvas-v2"))).get_attribute("class") )
        )

        #  Esperar o foguete crashar
        atributo = "class"
        string = "crash-animation-up-paused"
        wait.until(EC.text_to_be_present_in_element_attribute((By.ID, "crash-main-canvas-v2"), atributo, string))

        #  Pegar o crash
        last_crash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-main-canvas-v2 > div > div.crash-board > div:nth-child(3) > div > div.crash-canvas__payout-title-and-payout-value > p")))
        last_crash = float(last_crash.text.replace("X", "").replace(",", "."))
        return last_crash


    def __esperar_velas_baixas(self, qtd_velas_baixas: int, valor_vela: float=1.50):
        """
        Responsável por aguardar até que a quantidade de velas baixas, seja a solicitada nos parametros
        :param qtd_velas_baixas:
        :param valor_vela:
        :return:
        """
        logging.info(f"Esperando {qtd_velas_baixas} {'vela'if qtd_velas_baixas == 1 else 'velas'} - abaixo de:  {valor_vela}X")

        qtd_passadas = 0
        while qtd_passadas < qtd_velas_baixas:
            crash_atual = self.__wait_and_get_last_crash_by_navbar()

            if crash_atual <= valor_vela:
                qtd_passadas += 1
            elif crash_atual > valor_vela:
                qtd_passadas = 0  # Reinicia a contagem, se vier vela alta, antes do tempo esperado
            if qtd_passadas == qtd_velas_baixas:
                # Retorna True, quando alcançar o objetivo
                return True

    def get_saldo(self):
        """
        Responsável por pegar o saldo atual, do jogador $$
        :return:
        """
        driver = self.driver
        wait = self.wait

        try:
            with open("demo_saldo.txt", "r") as fp:
                meu_saldo = fp.read()
            resp = float(round(float(meu_saldo), 2))
        except:
            resp = False

        return resp

    def set_saldo(self, valor: float):
        """
        Responsável por setar o saldo atual, do jogador $$
        :return:
        """
        driver = self.driver
        wait = self.wait
        try:
            with open("demo_saldo.txt", "w") as fp:
                fp.write(f"{valor}")
        except:
            resp = False


    def jogar(self, qtd_velas_baixas: int = 0, valor_de_velas_baixas: float = 1.50, gales: list = [1, 3, 9, 26, 78], apostar_na_vela: float = 1.50):
        """
        Responsável por apostar após a quantidade de velas baixas, especificada
        :param qtd_velas_baixas: Quantidade de velas baixas, que deseja esperar, até fazer a jogada (Default = 0: Irá jogar sem esperar velas baixas)
        :param gales: Gales para cada aposta, sabendo que o limite de $ na aposta é 500
        :param apostar_na_vela: Vela que deseja que seja usada na aposta
        :return: None
        """
        while True:
            [print() for _ in range(3)]

            self.__esperar_velas_baixas(qtd_velas_baixas=qtd_velas_baixas, valor_vela=valor_de_velas_baixas)  # Espera até achar velas baixas
            valores_apostar = gales
            indice_aposta = 0  # Começa no primeiro valor da lista

            for i in range(1, 9999):


                valor_aposta = valores_apostar[indice_aposta]
                """
                self.__selecionar_valor_dinheiro(valor_aposta)
                self.__selecionar_valor_limite_vela(apostar_na_vela)
                self.__clicar_apostar()
                """
                # Esperar o próximo inicio de subida do foguete
                self.wait.until(EC.text_to_be_present_in_element_attribute((By.ID, "crash-main-canvas-v2"), "class", "crash-animation-waiting"))

                vela_resultado = self.__wait_and_get_last_crash_by_navbar()

                if vela_resultado > apostar_na_vela:
                    ganhou = True
                else:
                    ganhou = False


                if ganhou:
                    indice_aposta = 0
                    #logging.info(f"{' ' * 10}Valor da aposta: R$ {valor_aposta} - Ganhou")
                    n = round(self.get_saldo() + ((valor_aposta * apostar_na_vela) - valor_aposta), 2)
                    self.set_saldo(n)
                    logging.info(f"{' ' * 5}Ganhou: R$ {valor_aposta} * {apostar_na_vela} -> SALDO ATUAL: {n}")
                    break

                elif not ganhou:
                    if indice_aposta < len(valores_apostar) - 1:
                        indice_aposta += 1
                    n = round(self.get_saldo(), 2) - round(valor_aposta, 2)
                    self.set_saldo(n)
                    logging.info(f"{' ' * 5}PERDEU: R$ -{valor_aposta} -> SALDO ATUAL: {n}")



crash = BlazerCrash("@gmail.com", "0", headless=True, banca_inicial=1000)
crash.jogar(qtd_velas_baixas=0, valor_de_velas_baixas=2.50, gales=[0.1, 0.30, 0.90, 2.6, 7.8, 23.4, 70.2, 210.6, 631.8, 1895.4], apostar_na_vela=1.50)
# [0.1, 0.30, 0.90, 2.6, 7.8, 23.4, 70.2]
# [0.50, 1.50, 4.50, 13.50, 40, 120, 360]
# [0.25, 0.80, 2.2, 6.50, 19.5, 58.5, 175.5, 526]
# [0.25, 0.50, 1.50, 4.5, 13.5, 40.5, 121.5, 364.5, 1093.5, 3280.5]

# OBS: não está detectando crashs na vela 1.00x (APARENTEMENTE CORRIGIDO. TESTANDO....)

