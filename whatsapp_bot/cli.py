from __future__ import annotations

from .config import load_alvos
from .loop import executar_loop_agente
from .session import criar_driver, preparar_sessao_whatsapp


def main() -> None:
    alvos = load_alvos()
    if not alvos:
        raise SystemExit("Preencha ALVOS_CHATS em whatsapp_bot/config.py")

    driver = criar_driver()
    preparar_sessao_whatsapp(driver, alvos)
    executar_loop_agente(driver, alvos)
