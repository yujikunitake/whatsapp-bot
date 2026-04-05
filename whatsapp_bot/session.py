from __future__ import annotations

import time

from . import config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def criar_driver() -> webdriver.Chrome:
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def esperar_lista_conversas(driver: webdriver.Chrome, timeout: float = 90) -> None:
    print("Procurando #pane-side...", flush=True)
    fim = time.time() + timeout
    ultimo_aviso = 0.0
    while time.time() < fim:
        try:
            el = driver.find_element(By.ID, "pane-side")
            if el.is_displayed():
                print("Lista de conversas ok.", flush=True)
                return
        except NoSuchElementException:
            pass
        agora = time.time()
        if agora - ultimo_aviso >= 4:
            print(f"  ... ~{int(fim - agora)}s restantes", flush=True)
            ultimo_aviso = agora
        time.sleep(0.35)
    raise SystemExit("Timeout em #pane-side. Confira login e rode de novo.")


def preparar_sessao_whatsapp(driver: webdriver.Chrome, alvos: list[str]) -> None:
    print("Abrindo web.whatsapp.com...", flush=True)
    driver.get("https://web.whatsapp.com/")
    try:
        driver.maximize_window()
    except Exception:
        pass
    print(
        "No terminal: Enter para seguir; ou B=DEBUG e Enter para log das mensagens lidas.",
        flush=True,
    )
    linha = input(">>> ").strip()
    config.DEBUG_MENSAGENS = linha.casefold() == "b=debug"
    if config.DEBUG_MENSAGENS:
        print("Debug de leitura ativado.\n", flush=True)

    esperar_lista_conversas(driver, timeout=90)

    print(
        f"\nAlvos: {alvos} | só não lidas: {config.ENVIAR_SOMENTE_COM_NAO_LIDA}\n"
        "Chat aberto na lateral some a bolinha; o cabeçalho #main ainda identifica o contato.",
        flush=True,
    )
    input("\n>>> Enter para iniciar o loop: ")
    print("Rodando. Ctrl+C encerra.\n", flush=True)
