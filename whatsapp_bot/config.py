from __future__ import annotations

import os

ALVOS_CHATS: list[str] = [
    "Roberto Tossio",
]

ENVIAR_SOMENTE_COM_NAO_LIDA = os.environ.get("WHATSAPP_ONLY_UNREAD", "1").strip().lower() not in (
    "0",
    "false",
    "no",
)

DEBUG_MENSAGENS = False

NAO_LIDA_XPATH = ".//span[" + " or ".join(
    f"contains(@aria-label, '{s}')"
    for s in (
        "unread",
        "não lida",
        "não lidas",
        "mensagem não lida",
        "mensagens não lidas",
    )
) + "]"

COMPOSE_CSS = (
    "#main div[contenteditable='true'][data-lexical-editor='true']",
    "#main footer div[contenteditable='true']",
    "#main [contenteditable='true'][role='textbox']",
    "#main div[contenteditable='true']",
)

LIST_ROW_XPATH = ".//div[@role='listitem' or @role='row' or @role='gridcell']"

DIGITACAO_MIN_S = 0.012
DIGITACAO_MAX_S = 0.045
DIGITACAO_PAUSA_PONTUACAO_S = (0.02, 0.06)


def load_alvos() -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for n in (s.strip() for s in ALVOS_CHATS if str(s).strip()):
        k = n.casefold()
        if k not in seen:
            seen.add(k)
            out.append(n)
    return out
