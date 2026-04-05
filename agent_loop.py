from __future__ import annotations

import time
import traceback

import config
from selenium.webdriver.remote.webdriver import WebDriver

from faq_agente import responder
from whatsapp_composer import enviar_texto_no_composer, get_compose_box, scroll_conversa_ate_o_fim
from whatsapp_io import ultima_mensagem_recebida_meta
from whatsapp_sidebar import (
    click_chat,
    find_chat_row_by_name,
    main_mostrando_alvo,
    row_has_unread,
)

_cache_msg: dict[str, str] = {}


def _chave_cache(alvo: str, texto: str, msg_id: str | None) -> str:
    return msg_id if msg_id else f"t:{texto.casefold()}"


def _processar_alvo(driver: WebDriver, alvo: str) -> None:
    chat_aberto = main_mostrando_alvo(driver, alvo)
    linha = None if chat_aberto else find_chat_row_by_name(driver, alvo)

    if not chat_aberto and not linha:
        print(f"Não achei: {alvo!r}")
        return

    if config.ENVIAR_SOMENTE_COM_NAO_LIDA and not chat_aberto:
        if not linha or not row_has_unread(linha):
            print(f"Sem não lidas: {alvo!r}")
            return

    if chat_aberto:
        time.sleep(0.8)
    else:
        click_chat(driver, linha)
        time.sleep(2.0)

    scroll_conversa_ate_o_fim(driver)

    pergunta, msg_id = ultima_mensagem_recebida_meta(driver)
    if config.DEBUG_MENSAGENS:
        print(
            f"[debug] alvo={alvo!r}\n        texto_lido={pergunta!r}\n        msg_id={msg_id!r}",
            flush=True,
        )

    if not pergunta:
        print(
            f"Sem texto recebido em {alvo!r} — abra o chat, envie texto; "
            "mensagens suas precisam aparecer com 'Você:' no data-pre-plain-text do Web."
        )
        return

    chave = _chave_cache(alvo, pergunta, msg_id)
    if _cache_msg.get(alvo) == chave:
        if config.DEBUG_MENSAGENS:
            print(f"[debug] já respondido chave={chave!r}", flush=True)
        print(f"Já respondido nesta mensagem: {alvo!r}")
        return

    resposta = responder(pergunta)
    enviar_texto_no_composer(get_compose_box(driver), resposta)
    _cache_msg[alvo] = chave
    print(f"Respondido {alvo!r}: {pergunta[:40]!r}…")
    if config.DEBUG_MENSAGENS:
        print(f"[debug] resposta_enviada={resposta[:120]!r}…", flush=True)

    time.sleep(2)


def executar_loop_agente(driver: WebDriver, alvos: list[str]) -> None:
    while True:
        print("Verificando chats...")
        time.sleep(3)
        for alvo in alvos:
            try:
                _processar_alvo(driver, alvo)
            except Exception as e:
                print(f"Erro em {alvo!r}: {e}")
                traceback.print_exc()
                time.sleep(2)
