# WhatsApp Web — FAQ automatizado

Bot em Python que controla o WhatsApp Web no Chrome (Selenium), monitora chats por nome e responde com regras locais — sem API de modelo de linguagem. O conteúdo das respostas é um FAQ fictício de charter de helicóptero (**Helisky Charter**), em `faq_agente.py`.

---

## Índice

1. [Início rápido](#início-rápido)  
2. [Requisitos](#requisitos)  
3. [Configuração](#configuração)  
4. [Como rodar](#como-rodar)  
5. [Guia por sistema operacional](#guia-por-sistema-operacional)  
6. [Variáveis de ambiente](#variáveis-de-ambiente)  
7. [Arquitetura do código](#arquitetura-do-código)  
8. [Limitações](#limitações)  

---

## Início rápido

Na pasta do projeto, com Python 3.13 e [uv](https://docs.astral.sh/uv/getting-started/installation/) instalados:

```bash
uv sync
uv run python main.py
```

Ajuste os nomes em **`ALVOS_CHATS`** (`config.py`) para bater com o título do chat na lista do WhatsApp. Na primeira execução, escaneie o **QR code** na janela do Chrome.

---

## Requisitos

| Item | Detalhe |
|------|---------|
| Python | 3.13+ (`pyproject.toml`) |
| Navegador | Google Chrome instalado; o `ChromeDriverManager` baixa o driver compatível |
| Conta | WhatsApp Web autenticado na sessão que o Selenium abre |

---

## Configuração

| O quê | Onde |
|--------|------|
| Chats monitorados | `ALVOS_CHATS` em `config.py` |
| Log das mensagens lidas | No terminal, após o QR: digite `B=DEBUG` e Enter (senão só Enter) |
| Só responder com “não lida” | Padrão ligado; desligue com `WHATSAPP_ONLY_UNREAD` (ver [abaixo](#variáveis-de-ambiente)) |

Arquivos auxiliares: `fluxo_perguntas.txt` (roteiro) e `agente_whatsapp.ipynb` (experimentos). O fluxo principal é `main.py`.

---

## Como rodar

### Com uv (recomendado)

```bash
uv sync
uv run python main.py
```

### Sem uv

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# ou: .venv\Scripts\activate   # Windows (CMD/PowerShell)
pip install selenium webdriver-manager
python main.py
```

(Se o projeto estiver empacotado, `pip install -e .` também serve.)

### Observações

- **Windows (PowerShell):** se o `uv` não aparecer no comando, feche e abra o terminal depois de instalar.
- **Terminal interativo:** o programa usa `input()` (Enter, `B=DEBUG`). Rode em terminal com TTY.

---

## Guia por sistema operacional

### Windows

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | [Python 3.13](https://www.python.org/downloads/) com “Add python.exe to PATH”; Chrome; `uv` (instalador oficial ou `pip install uv`). Na pasta do projeto: `uv sync` e `uv run python main.py`. |
| **Dica** | `Ctrl+Shift+V` no PowerShell ajuda a colar ao usar o QR code. |

### macOS

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | Python 3.13 (python.org, `brew install python@3.13` ou pyenv); Chrome; `uv` (documentação oficial). No Terminal: `uv sync` e `uv run python main.py`. |

### Linux

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | Python 3.13 (pacotes da distro, [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) no Ubuntu ou pyenv). Google Chrome (.deb/.rpm) ou Chromium compatível. `uv` + `uv sync` + `uv run python main.py`. |

---

## Variáveis de ambiente

| Variável | Efeito |
|----------|--------|
| `WHATSAPP_ONLY_UNREAD` | `0`, `false` ou `no`: o bot pode responder sem bolinha de não lida (útil com o chat já aberto). Qualquer outro valor: padrão (só não lidas quando o chat não está em foco). |

---

## Arquitetura do código

Fluxo: **sessão do navegador** → **loop** pelos contatos em `ALVOS_CHATS`.

| Arquivo | Função |
|---------|--------|
| `main.py` | Entrada: carrega alvos, cria o driver, prepara sessão, inicia o loop. |
| `whatsapp_session.py` | Abre `web.whatsapp.com`, espera `#pane-side`, prompts no terminal; driver via `ChromeDriverManager`. |
| `config.py` | Alvos, seletores, tempos de digitação, `load_alvos()`, leitura de `WHATSAPP_ONLY_UNREAD`. |
| `agent_loop.py` | Por alvo: sidebar ou `#main` aberto, não lida (opcional), abre chat, lê última mensagem recebida, cache por `data-id`/texto, `faq_agente.responder`, envio. |
| `whatsapp_sidebar.py` | `#pane-side`, nome do chat, não lidas, clique. |
| `whatsapp_composer.py` | Campo de mensagem em `#main`, digitação pausada, Enter. |
| `whatsapp_io.py` | JS + fallback Python para última bolha recebida (`message-in` / `data-id`). |
| `faq_agente.py` | Normalização, saudações, palavras-chave → texto fixo. |

---

## Limitações

- O **DOM do WhatsApp Web** muda: CSS/XPath podem quebrar e precisar de manutenção.
- Mensagens **suas** precisam ser detectadas como saída (ex.: `Você:` em `data-pre-plain-text`); caso contrário o remetente pode ser confundido.
- O FAQ é **fixo** e limitado ao que está em `faq_agente.py`.
