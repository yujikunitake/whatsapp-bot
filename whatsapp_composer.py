from __future__ import annotations

import platform
import random
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import COMPOSE_CSS, DIGITACAO_MAX_S, DIGITACAO_MIN_S, DIGITACAO_PAUSA_PONTUACAO_S


def get_compose_box(driver: WebDriver, timeout: float = 15) -> WebElement:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main"))
    )
    for css in COMPOSE_CSS:
        vis = [e for e in driver.find_elements(By.CSS_SELECTOR, css) if e.is_displayed()]
        if vis:
            return vis[-1]
    raise NoSuchElementException("Composer não encontrado em #main.")


def scroll_conversa_ate_o_fim(driver: WebDriver) -> None:
    try:
        driver.execute_script(
            """
            const main = document.querySelector('#main');
            if (!main) return;
            const box = main.querySelector('[role="application"]') || main.querySelector('.copyable-area') || main;
            box.scrollTop = box.scrollHeight;
            """
        )
    except Exception:
        pass
    time.sleep(0.4)


def _digitar_streaming(campo: WebElement, texto: str) -> None:
    for ch in texto:
        campo.send_keys(ch)
        time.sleep(random.uniform(DIGITACAO_MIN_S, DIGITACAO_MAX_S))
        if ch in ".,;:!?":
            time.sleep(random.uniform(*DIGITACAO_PAUSA_PONTUACAO_S))


def enviar_texto_no_composer(campo: WebElement, texto: str) -> None:
    mod = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
    campo.click()
    time.sleep(random.uniform(0.08, 0.18))
    try:
        campo.send_keys(mod, "a")
        campo.send_keys(Keys.BACKSPACE)
    except Exception:
        pass
    time.sleep(random.uniform(0.04, 0.1))
    _digitar_streaming(campo, texto)
    time.sleep(random.uniform(0.12, 0.28))
    campo.send_keys(Keys.ENTER)
