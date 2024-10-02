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
import sys
from selenium.common.exceptions import TimeoutException
import random
import requests
import re
import logging



def logging_edit():
    if os.path.exists(f"{os.getcwd()}/ikrazy/"):
        vps_path = f"{os.getcwd()}/ikrazy/"
    else:
        vps_path = ""
    logging.basicConfig(level=logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s -> %(message)s')
    console_handler.setFormatter(log_format)
    logging.getLogger().addHandler(console_handler)
    file_handler = logging.FileHandler(f"{vps_path}ikrazy.log")
    file_handler.setLevel(logging.INFO)
    # Adiciona o formato ao handler do arquivo
    file_handler.setFormatter(log_format)
    # Adiciona o handler do arquivo ao logger padrão
    logging.getLogger().addHandler(file_handler)


logging_edit()
logging.info(f":::::::::: Iniciando script-path:{sys.argv[0]} ::")


class BlazerCrash:

    def __init__(self, email, senha, headless=False, run_na_vps=False):
        """
        Classe onde fica o inicializador do webdriver e toda a sequencia de execução do código
        """
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless") if headless is True else None
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-webgl")
        self.email = email
        self.senha = senha
        self.run_na_vps = run_na_vps
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 7020)

        # Config básica
        self.valor_limite_vela = 1.50

    def login(self):
        email = self.email
        senha = self.senha

        driver = self.driver
        wait = self.wait
        logging.info("[*] Fazendo login...")
        driver.get('https://blaze-7.com/pt?modal=auth&tab=login')

        input_email = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#auth-modal > div > form > div:nth-child(1) > div > input[type=text]')))
        input_email.click()
        input_email.send_keys(email)

        input_senha = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#auth-modal > div > form > div:nth-child(2) > div > input[type=password]')))
        input_senha.click()
        input_senha.send_keys(senha)

        login = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#auth-modal > div > form > div.input-footer > button')))
        login.click()
        sleep(2.50)

        # Fechar obstaculos
        game_link = driver.get('https://blaze-7.com/pt/games/crash_2')

        self.verificar_manutencao()  # Verifica se o site está manutenção sempre que inicia o script

        sleep(1)  # 10.10 deixa esse sleep para poder carregar o banner inteiro do AVIATOR

        fecha_banner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#forced-banner-close')))
        fecha_banner.click()

        fecha_chat = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#close-chat')))
        fecha_chat.click()
        sleep(2.20)
        logging.info("[*] Login feito...")
        self.__btn_normal()



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
        last_crash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#crash-recent-v2 > div > div.entries > div:nth-child(1)")))
        if self.run_na_vps:
            last_crash = float(last_crash.text.replace("X", "").replace(",", ""))
        else:
            last_crash = float(last_crash.text.replace("X", "").replace(".", "").replace(",", "."))
        logging.info(last_crash)
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
        last_crash = float(last_crash.text.replace("X", "").replace(".", "").replace(",", "."))
        return last_crash


    def __esperar_velas_baixas(self, qtd_velas_baixas: int, valor_vela: float=1.50):
        """
        Responsável por aguardar até que a quantidade de velas baixas, seja a solicitada nos parametros
        :param qtd_velas_baixas:
        :param valor_vela:
        :return:
        """
        logging.info(f"[*] Esperando {qtd_velas_baixas} {'vela'if qtd_velas_baixas == 1 else 'velas'} - abaixo de:  {valor_vela}X")

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
            meu_saldo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#header > div.right > div > div.routes > div > div.wallet-dropdown > div > a > div > div > div.currency")))
            resp = meu_saldo.text
        except:
            resp = False

        return resp

    def verificar_manutencao(self):
        """
        Vai verificar se o site está em manutenção quando iniciar o script.
        Caso entre em manutenção durante o processo do script, o wait vai ficar ativo até que o mesmo retorne um erro e a vps reinicie o script.
        """
        try:
            try:
                WebDriverWait(self.driver, 40).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".waitlist-feature-on-maintenance-container")))  # 30 minutos
            except:
                logging.info(">>>>>>>> >>>>>>>> >>>>>>>>> >>>>>>>>> SITE EM MANUTENÇÃO < << <<<")

            WebDriverWait(self.driver, 1800).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".waitlist-feature-on-maintenance-container")))  # 30 minutos
        except Exception as e:
            logging.info(f"{e}")
            self.driver.quit()
            raise e
        logging.info("[*] A página não se encontra em manutenção.")

    def jogar(self, qtd_velas_baixas: int = 0, valor_de_velas_baixas: float = 1.50, gales: list = [0, 0, 0, 0, 0], velas_apostar: list = [0, 0, 0, 0, 0]):
        """
        Responsável por apostar após a quantidade de velas baixas, especificada
        Gales e velas_apostar tem que ser de mesmo tamanho

        :param qtd_velas_baixas: Quantidade de velas baixas, que deseja esperar, até fazer a jogada (Default = 0: Irá jogar sem esperar velas baixas)
        :param gales: Gales para cada aposta, sabendo que o limite de $ na aposta é 500
        :param apostar_na_vela: Vela que deseja que seja usada na aposta
        :return: None
        """
        logging.info("[*] Iniciando jogo")
        while True:
            [print() for _ in range(3)]
            logging.info(f"[*] Saldo atual ${crash.get_saldo()}")
            self.__esperar_velas_baixas(qtd_velas_baixas=qtd_velas_baixas, valor_vela=valor_de_velas_baixas)  # Espera até achar velas baixas
            valores_apostar = gales
            velas_apostar = velas_apostar
            indice_aposta = 0  # Começa no primeiro valor da lista

            for i in range(0, len(gales)):
                valor_aposta = valores_apostar[indice_aposta]
                vela_aposta = velas_apostar[indice_aposta]
                self.__selecionar_valor_dinheiro(valor_aposta)
                self.__selecionar_valor_limite_vela(vela_aposta)
                self.__clicar_apostar()
                logging.info(f"{' ' * 2} Apostando: ${valor_aposta} - na vela {vela_aposta}")
                # Esperar o próximo inicio de subida do foguete
                self.wait.until(EC.text_to_be_present_in_element_attribute((By.ID, "crash-main-canvas-v2"), "class", "crash-animation-waiting"))
                vela_resultado = self.__wait_and_get_last_crash_by_navbar()

                if vela_resultado > vela_aposta:
                    ganhou = True
                else:
                    ganhou = False

                if ganhou:
                    indice_aposta = 0
                    logging.info(f"[-]{' ' * 5} - Ganhou.")
                    break

                elif not ganhou:
                    if indice_aposta < len(valores_apostar) - 1:
                        indice_aposta += 1
                    logging.info(f"[-]{' ' * 5} - Perdeu")


crash = BlazerCrash("dodochavescadete13@gmail.com", "Usuario@1", headless=False, run_na_vps=False)

try:
    crash.login()
    crash.jogar(qtd_velas_baixas=10, valor_de_velas_baixas=2.50, gales=[5, 11], velas_apostar=[1.50, 1.50])  #45 reais

except Exception as e:
    logging.info(f"[ ! ] {e}")

finally:
    # Certifique-se de fechar a sessão do WebDriver, mesmo em caso de falha
    crash.driver.quit()
    logging.info("-------------------{x} Sessao do driver fechada.")
    exit()
