from __future__ import annotations

import html
import re
import unicodedata


def _normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKC", texto or "")
    for ch in (
        "\u200b",
        "\u200c",
        "\u200d",
        "\u200e",
        "\u200f",
        "\u202a",
        "\u202c",
        "\u2066",
        "\u2069",
    ):
        t = t.replace(ch, "")
    t = html.unescape(t)
    t = re.sub(r"<[^>]*>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = t.casefold()
    t = re.sub(r"[\s,!.?…]+$", "", t)
    t = re.sub(r"^[\s,!.?…]+", "", t)
    return t


def _eh_saudacao(t: str) -> bool:
    if not t:
        return False
    if re.match(r"^(oi|olá|ola|hey)\b", t):
        return True
    if re.fullmatch(r"(oi|olá|ola|hey)", t):
        return True
    if t in ("bom dia", "boa tarde", "boa noite", "bdia", "btarde", "bnoite"):
        return True
    if re.search(r"\b(bom dia|boa tarde|boa noite)\b", t) and len(t) < 40:
        return True
    return False


def responder(pergunta: str) -> str:
    t = _normalizar(pergunta)
    if not t:
        return (
            "Olá! Sou o assistente virtual da Helisky Charter. "
            "Pergunte sobre reserva, preços, rotas, piloto, documentos ou seguro."
        )

    if _eh_saudacao(t):
        return (
            "Olá! Sou o assistente da Helisky Charter (aluguel de helicóptero). "
            "Posso ajudar com reserva, preços, rotas, piloto, passageiros, documentos, seguro e contato."
        )

    if any(p in t for p in ("obrigado", "obrigada", "valeu", "thanks")):
        return "Por nada! Bons voos e conte conosco quando quiser decolar de novo."

    if any(
        p in t
        for p in (
            "cancelar",
            "cancelamento",
            "desmarcar",
            "reembolso",
            "devolução do dinheiro",
            "devolucao do dinheiro",
        )
    ):
        return (
            "Cancelamento: até 48h antes do voo o reembolso é de 90% do valor; "
            "entre 48h e 24h, 50%. Com menos de 24h não há reembolso, salvo motivo de força maior comprovada. "
            "Solicite pelo e-mail reservas@helisky-charter.exemplo."
        )

    if any(
        p in t
        for p in (
            "preço",
            "preco",
            "quanto custa",
            "valor",
            "cobrança",
            "cobranca",
            "orçamento",
            "orcamento",
        )
    ):
        return (
            "Valores partem de R$ 4.500 por hora de voo em rota panorâmica padrão (até 3 passageiros), "
            "variando por aeronave e rota. Translados e fretamento fechado têm tabela sob consulta. "
            "Peça orçamento em reservas@helisky-charter.exemplo com data, rota e número de passageiros."
        )

    if any(
        p in t
        for p in (
            "reservar",
            "reserva",
            "agendar",
            "marcar voo",
            "quero alugar",
            "alugar helicóptero",
            "alugar helicoptero",
        )
    ):
        return (
            "Para reservar: envie data preferida, horário aproximado, número de passageiros e rota desejada "
            "para reservas@helisky-charter.exemplo. A confirmação depende de disponibilidade da aeronave e do piloto."
        )

    if any(
        p in t
        for p in (
            "piloto",
            "pilota",
            "quem voa",
            "posso pilotar",
            "eu piloto",
            "licença de piloto",
            "licenca de piloto",
        )
    ):
        return (
            "Todos os voos são realizados por pilotos comercialmente habilitados (CHTA) e credenciados na empresa. "
            "Clientes não pilotam as aeronaves de aluguel; experiências com comando duplo só em programas específicos "
            "divulgados no site."
        )

    if any(
        p in t
        for p in (
            "seguro",
            "segurança",
            "seguranca",
            "acidente",
            "é seguro",
            "e seguro",
        )
    ):
        return (
            "As operações seguem regulamentação da ANAC; aeronaves com manutenção em dia e seguro aeronáutico obrigatório. "
            "Passageiros são orientados no briefing pré-voo. Dúvidas sobre cobertura: operacoes@helisky-charter.exemplo."
        )

    if any(
        p in t
        for p in (
            "documento",
            "rg",
            "cpf",
            "identidade",
            "preciso levar",
            "o que levar",
        )
    ):
        return (
            "No dia do voo, traga documento com foto (RG ou CNH) e comprovante da reserva. "
            "Menores precisam de autorização dos responsáveis conforme termo enviado no e-mail de confirmação."
        )

    if any(
        p in t
        for p in (
            "passageiro",
            "lugares",
            "capacidade",
            "quantas pessoas",
            "cabe quantos",
        )
    ):
        return (
            "Nossos helicópteros leves comportam em geral até 3 passageiros + piloto; "
            "modelos maiores (sob consulta) até 5 passageiros + piloto. Informe o número de pessoas no pedido de orçamento."
        )

    if any(
        p in t
        for p in (
            "tempo de voo",
            "duração",
            "duracao",
            "quanto tempo",
            "percurso",
            "rota",
            "passeio",
            "panorâmico",
            "panoramico",
        )
    ):
        return (
            "Passeios panorâmicos padrão têm cerca de 15 a 30 minutos de voo; rotas personalizadas e fretamentos "
            "seguem o tempo contratado. O tempo no ar pode variar por condições operacionais e tráfego aéreo."
        )

    if any(
        p in t
        for p in (
            "tempo ruim",
            "chuva",
            "tempo fechado",
            "neblina",
            "voo cancelado",
            "condição meteorológica",
            "condicao meteorologica",
        )
    ):
        return (
            "Voos podem ser adiados ou cancelados por condições meteorológicas ou ordem operacional. "
            "Nesses casos reagendamos sem custo ou devolvemos conforme política de cancelamento."
        )

    if any(p in t for p in ("heliponto", "decolagem", "embarque", "onde embarca", "saída", "saida", "base")):
        return (
            "Embarques partem dos helipontos credenciados informados no e-mail de confirmação (ex.: base na zona sul — "
            "endereço completo no site). Não realizamos embarque em locais não autorizados pela ANAC."
        )

    if any(p in t for p in ("email", "e-mail", "telefone", "contato", "endereço", "endereco", "onde fica")):
        return (
            "Helisky Charter | reservas@helisky-charter.exemplo | (11) 4002-8922 | "
            "Av. das Rotas, 1000 — Hangar 3, São Paulo/SP."
        )

    if any(p in t for p in ("horário", "horario", "atendimento", "funciona")):
        return (
            "Central de reservas: segunda a sábado, 9h às 19h. Voos comerciais em horários acordados na reserva."
        )

    return (
        "Não encontrei uma resposta automática para isso. "
        "Tente perguntar sobre: agendar voo, preço, rota/duração, piloto, passageiros, documentos, seguro, "
        "cancelamento ou contato. Para orçamentos personalizados: reservas@helisky-charter.exemplo."
    )
