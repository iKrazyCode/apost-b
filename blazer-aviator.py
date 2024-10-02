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


class BlazerAviator:

    def __init__(self, email, senha, demo=True, headless=False):
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

        self.__demo = demo
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 8020)

        # Config básica
        self.valor_limite_vela = 1.50

        self.login(email, senha)
        self.__btn_automatico()
        self.__btn_checkbox_automatico()

    def login(self, email, senha):
        driver = self.driver
        wait = self.wait

        try:
            driver = self.driver
            wait = self.wait
            print("Fazendo login...")
            driver.get('https://blaze-4.com/pt?modal=auth&tab=login')

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
            if self.__demo == True:
                aviator = driver.get('https://blaze-4.com/pt/games/aviator/fun')
            else:
                aviator = driver.get('https://blaze-4.com/pt/games/aviator')

            sleep(1)  # 10.10 deixa esse sleep para poder carregar o banner inteiro do AVIATOR

            fecha_banner = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#forced-banner-close')))
            fecha_banner.click()

            fecha_chat = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#close-chat')))
            fecha_chat.click()
            sleep(2.20)
            return True

        except:
            print("Falha no login.")
            raise Exception

    def __iframe(self, acao):
        """
        Responsável por entrar e sair do iframe de aposta
        Parametros: 'entrar', 'sair'
        :return:
        """
        try:
            match acao:
                case 'entrar':
                    self.driver.switch_to.frame(
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#game_wrapper > iframe"))))
                case 'sair':
                    self.driver.switch_to.default_content()
        except:
            pass

    def __btn_automatico(self):
        """
        Função que clica no botão de automático.
        Entra no iframe e saí ao final do código.
        para manter o padrão default da página. para ações futuras
        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')

        try:
            automatico = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > app-navigation-switcher > div > button:nth-child(3)")))
            automatico.click()
            resp = True
        except:
            resp = False

        self.__iframe('sair')
        return resp


    def __btn_checkbox_automatico(self):
        driver = self.driver
        wait = self.wait

        self.__iframe('entrar')

        try:
            # Antes preciso selecionar o checkbox, para
            # selecionar o input
            btn_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.second-row > div.cashout-block > div.cash-out-switcher > app-ui-switcher")))
            btn_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.second-row > div.cashout-block > div.cash-out-switcher > app-ui-switcher")))
            btn_checkbox.click()

            resp = True
        except:
            resp = False

        self.__iframe('sair')
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
        self.__iframe('entrar')
        #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature.auto-game > div.bet-block > app-spinner > div > div.input > input")))

        try:
            input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature.auto-game > div.bet-block > app-spinner > div > div.input > input")))
            [input.send_keys(Keys.BACKSPACE) for i in range(8)]
            input.send_keys(valor)
            resp = True
        except:
            resp = False

        self.__iframe('sair')
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
        self.__iframe('entrar')

        try:
            #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.second-row > div.cashout-block > div.cashout-spinner-wrapper > div > app-spinner > div > div.input.full-width > input")))
            input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.second-row > div.cashout-block > div.cashout-spinner-wrapper > div > app-spinner > div > div.input.full-width > input")))

            [input.send_keys(Keys.BACKSPACE) for i in range(8)]
            input.send_keys(vela)
            resp = True
        except:
            resp = False

        self.__iframe('sair')
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
        self.__iframe('entrar')

        crash_before = self.__get_last_crash()
        self.__iframe('entrar')

        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature.auto-game > div.buttons-block > button")))
        btn.click()
        resp = True


        #  Loop para verificar se ainda está na aposta
        crash_atual = 0
        loop = True
        while loop == True:
            crash_atual = self.__get_last_crash()
            if crash_atual != crash_before:
                loop = False


        if crash_atual > self.valor_limite_vela:
            resp = True
        else:
            resp = False

        self.__iframe('sair')
        return resp


    def get_saldo(self):
        """

        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')

        try:
            meu_saldo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.main-header > app-header > div > div.second-block.d-flex > div > div.balance.px-2.d-flex.justify-content-end.align-items-center > div > span.amount.font-weight-bold")))
            resp = meu_saldo.text
        except:
            resp = False

        self.__iframe('sair')
        return resp

    def __get_all_navbar_crash(self):
        """
        Responsável por pegar o ultimo crash que houver
        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')


        last_crash = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.result-history.disabled-on-game-focused.my-2 > app-stats-widget > div > div.payouts-wrapper > div")))
        resp = [i.text.replace('x', '') for i in last_crash]

        self.__iframe('sair')
        return resp

    def __get_last_crash(self):
        """
        Responsável por pegar todos os crashs do navbar
        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')

        while True:
            try:
                last_crash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.result-history.disabled-on-game-focused.my-2 > app-stats-widget > div > div.payouts-wrapper > div :first-child")))
                resp = last_crash.text
                break
            except StaleElementReferenceException:
                pass

        resp = float(resp.replace('x', ''))
        self.__iframe('sair')

        return resp




    def __get_list_apostas(self):
        """
        Retorna uma lista de elementos webdriver, que contem as apostas feitas recente no navegador em questão
        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')
        # Clicar na aba de minhas apostas

        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.info-board.pt-2 > app-bets-widget > div > div > app-navigation-switcher > div > button:nth-child(3)")))

        btn.click()


        # Pegar lista
        lista_apostas = driver.find_elements(By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.info-board.pt-2 > app-bets-widget > div > app-my-bets-tab > div.h-100.scroll-y > app-bet-item")

        self.__iframe('sair')
        return lista_apostas

    def __get_source_list_apostados(self):
        """
        Responsável por retornar o codigo fonte da aba de lista de apostas recentes
        :return:
        """
        driver = self.driver
        wait = self.wait
        self.__iframe('entrar')

        source = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.info-board.pt-2 > app-bets-widget > div > app-my-bets-tab > div.h-100.scroll-y")))
        source = source.get_attribute("outerHTML")

        self.__iframe('sair')
        return source



    def __ganhou_aposta(self):
        """
        Usar sempre depois de clicar no botão de apostar
        :return: True | False
        """
        last_crash_antes_de_apostar = self.__get_last_crash()

        if (float(self.__get_last_crash().text.replace('x', ''))) > self.valor_limite_vela:
            ret = True
        else:
            ret = False
        self.__iframe('sair')
        return ret  # sucesso ao terminar partida

        return ret


    def __apostar(self, valor_aposta, valor_vela):
        """
        Função que aposta e retorna True ou False para ganhou ou perdeu a aposta
        :return:
        """
        self.__selecionar_valor_dinheiro(valor_aposta)
        self.__selecionar_valor_limite_vela(valor_vela)

        resultado = self.__clicar_apostar()

        return resultado

    def __esperar_velas_baixas(self, qtd_velas_baixas=3, valor_de_velas_baixas=2.50):
        """
        Responsável por aguardar até que a quantidade de velas baixas, seja a solicitada nos parametros
        :param qtd_velas_baixas:
        :param valor_vela:
        :return:
        """
        print(f"Esperando {qtd_velas_baixas} velas abaixo de {valor_de_velas_baixas}")
        qtd_passadas = 0
        while qtd_passadas < qtd_velas_baixas:
            crash_before = self.__get_last_crash()
            while True:
                crash_atual = self.__get_last_crash()
                if crash_atual == crash_before:
                    continue # mudar para break talvez
                else:
                    # entra aqui, se a vela estiver mudado
                    if crash_atual <= valor_de_velas_baixas:
                        qtd_passadas += 1
                        break
                    elif crash_atual > valor_de_velas_baixas:
                        qtd_passadas = 0  # Reinicia a contagem, se vier vela alta, antes do tempo esperado

                    if qtd_passadas == qtd_velas_baixas:
                        # Retorna True, quando alcançar o objetivo
                        return True



    def reiniciar_navegador(self):
        """
        Responsável por reiniciar o navegador
        :return:
        """
        self.driver.quit()
        self.driver = self.__init__(demo=self.__demo)

    def jogar_aviator_apos_velas_baixas(self, qtd_velas_baixas: int=0, valor_de_velas_baixas=2.50, gales=[0.1, 0.30, 0.90, 2.6, 7.8, 23.4, 70.2], apostar_na_vela: float=1.50):
        """
        Responsável por apostar após a quantidade de velas baixas, especificada
        :param qtd_velas_baixas: Quantidade de velas baixas, que deseja esperar, até fazer a jogada (Default = 0: Irá jogar sem esperar velas baixas)
        :param gales: Gales para cada aposta, sabendo que o limite de $ na aposta é 500
        :param apostar_na_vela: Vela que deseja que seja usada na aposta
        :return: None
        """
        while True:
            [print() for _ in range(3)]
            print('-' * 30)
            print(f" + Saldo atual: {self.get_saldo()}")

            self.__esperar_velas_baixas(qtd_velas_baixas=qtd_velas_baixas, valor_de_velas_baixas=valor_de_velas_baixas)  # Espera até achar velas baixas
            valores_apostar = gales
            indice_aposta = 0  # Começa no primeiro valor da lista
            apostar_na_vela = apostar_na_vela

            for i in range(1, 9999):
                valor_aposta = valores_apostar[indice_aposta]

                print(fr"{' ' * 4}({i}) Apostando\\\\")

                ganhou = self.__apostar(valor_aposta, apostar_na_vela)

                if (ganhou == True):
                    indice_aposta = 0
                    print(f"{' ' * 10}Valor da aposta: {valor_aposta} - Ganhou")
                    break  # Vai para a análise de velas novamente
                elif (ganhou == False):
                    if indice_aposta < len(valores_apostar) - 1:
                        indice_aposta += 1
                    print(f"{' ' * 10}Valor da aposta: {valor_aposta} - Perdeu")



aviator = BlazerAviator("dodochavescadete13@gmail.com", "Usuario@1", demo=False, headless=False)
aviator.jogar_aviator_apos_velas_baixas(qtd_velas_baixas=6, valor_de_velas_baixas=2.50, gales=[1, 2.20, 6.40, 19.20, 57.6], apostar_na_vela=1.50)


