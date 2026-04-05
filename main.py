"""Ponto de entrada: uv run python main.py"""

from __future__ import annotations

from agent_loop import executar_loop_agente
from config import load_alvos
from whatsapp_session import criar_driver, preparar_sessao_whatsapp


def main() -> None:
    alvos = load_alvos()
    if not alvos:
        raise SystemExit("Preencha ALVOS_CHATS em config.py")

    driver = criar_driver()
    preparar_sessao_whatsapp(driver, alvos)
    executar_loop_agente(driver, alvos)


if __name__ == "__main__":
    main()
