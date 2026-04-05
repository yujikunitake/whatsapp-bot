# WhatsApp Web — FAQ automatizado

Bot em Python que controla o WhatsApp Web no Chrome (Selenium), monitora chats por nome e responde com regras locais — sem API de modelo de linguagem. O conteúdo das respostas é um FAQ fictício de charter de helicóptero (**Helisky Charter**), em `whatsapp_bot/faq_agente.py`.

---

## Índice

1. [Estrutura do repositório](#estrutura-do-repositório)  
2. [Notebook Jupyter (FAQ isolado)](#notebook-jupyter-faq-isolado)  
3. [Início rápido](#início-rápido)  
4. [Requisitos](#requisitos)  
5. [Configuração](#configuração)  
6. [Como rodar](#como-rodar)  
7. [Guia por sistema operacional](#guia-por-sistema-operacional)  
8. [Variáveis de ambiente](#variáveis-de-ambiente)  
9. [Arquitetura do pacote](#arquitetura-do-pacote)  
10. [Limitações](#limitações)  

---

## Estrutura do repositório

Na raiz ficam só o que não é código importável do bot e o atalho de execução:

| Caminho | Função |
|---------|--------|
| `pyproject.toml` / `uv.lock` | Projeto instalável (pacote `whatsapp_bot`) |
| `main.py` | Atalho: chama o mesmo que `python -m whatsapp_bot` |
| `README.md` | Documentação |
| `fluxo_perguntas.txt` | Roteiro manual de testes |
| `agente_whatsapp.ipynb` | Ver [Notebook Jupyter](#notebook-jupyter-faq-isolado) |
| **`whatsapp_bot/`** | Pacote Python com toda a lógica (ver tabela abaixo) |

---

## Notebook Jupyter (FAQ isolado)

Arquivo: **`agente_whatsapp.ipynb`**. Serve para **exercitar só o “cérebro” do bot** (`whatsapp_bot.faq_agente.responder`), **sem Chrome, sem Selenium e sem WhatsApp**. Útil para conferir respostas por palavras-chave ao editar `faq_agente.py`.

O que ele faz, em ordem:

- **Introdução em markdown** — resume o projeto Helisky Charter, lista os módulos do pacote `whatsapp_bot/` e como rodar o bot no terminal; inclui link para um [exemplo de FAQ por regras no Colab](https://colab.research.google.com/drive/1nF_5EoNisjk8kLdiwZjZI8iwnEw6mrnM?usp=sharing).
- **Célula de import** — `from whatsapp_bot.faq_agente import responder` (exige ambiente com o projeto instalado: `uv sync` ou `pip install -e .`).
- **Célula de casos** — uma lista de frases típicas (preço, reserva, piloto, cancelamento, fora do escopo, etc.); para cada uma imprime pergunta e resposta retornada pelo FAQ.
- **Roteiro** — aponta para `fluxo_perguntas.txt` como lista mais longa de ideias de teste.
- **Resumo** — indica onde está a lógica de leitura/envio no pacote quando você for do notebook de volta ao bot completo.

Abra o arquivo no Jupyter, VS Code ou `uv run jupyter lab` a partir da pasta do repositório.

---

## Início rápido

Na pasta do projeto, com Python 3.13 e [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv sync
uv run python -m whatsapp_bot
```

Equivalente: `uv run python main.py` ou, com o venv ativo, o comando `whatsapp-bot`.

Ajuste **`ALVOS_CHATS`** em `whatsapp_bot/config.py` para bater com o título do chat na lista do WhatsApp. Na primeira execução, escaneie o **QR code** na janela do Chrome.

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
| Chats monitorados | `ALVOS_CHATS` em `whatsapp_bot/config.py` |
| Log das mensagens lidas | No terminal, após o QR: digite `B=DEBUG` e Enter (senão só Enter) |
| Só responder com “não lida” | Padrão ligado; desligue com `WHATSAPP_ONLY_UNREAD` (ver [abaixo](#variáveis-de-ambiente)) |

Arquivos auxiliares na raiz: `fluxo_perguntas.txt` e o notebook `agente_whatsapp.ipynb` ([descrição](#notebook-jupyter-faq-isolado)).

---

## Como rodar

### Com uv (recomendado)

```bash
uv sync
uv run python -m whatsapp_bot
```

### Sem uv

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# ou: .venv\Scripts\activate   # Windows
pip install -e .
python -m whatsapp_bot
# ou: whatsapp-bot
```

### Observações

- **`uv sync`** instala o projeto em modo editável; o import `whatsapp_bot` fica disponível para o notebook e para testes.
- **Terminal interativo:** o programa usa `input()` (Enter, `B=DEBUG`). Rode em terminal com TTY.

---

## Guia por sistema operacional

### Windows

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | [Python 3.13](https://www.python.org/downloads/) com “Add python.exe to PATH”; Chrome; `uv`. Na pasta do projeto: `uv sync` e `uv run python -m whatsapp_bot`. |
| **Dica** | `Ctrl+Shift+V` no PowerShell ajuda a colar ao usar o QR code. |

### macOS

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | Python 3.13 (python.org, Homebrew ou pyenv); Chrome; `uv`. `uv sync` e `uv run python -m whatsapp_bot`. |

### Linux

| Tópico | O que fazer |
|--------|-------------|
| **Setup** | Python 3.13 (distro, [deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) no Ubuntu ou pyenv). Google Chrome ou Chromium compatível. `uv sync` e `uv run python -m whatsapp_bot`. |

---

## Variáveis de ambiente

| Variável | Efeito |
|----------|--------|
| `WHATSAPP_ONLY_UNREAD` | `0`, `false` ou `no`: o bot pode responder sem bolinha de não lida (útil com o chat já aberto). Qualquer outro valor: padrão (só não lidas quando o chat não está em foco). |

---

## Arquitetura do pacote

Fluxo: **`cli.main()`** → sessão Chrome (`session`) → **`loop.executar_loop_agente`** pelos nomes em `ALVOS_CHATS`.

| Módulo (`whatsapp_bot/`) | Função |
|-------------------------|--------|
| `cli.py` | `main()`: carrega alvos, driver, sessão, loop. |
| `__main__.py` | Permite `python -m whatsapp_bot`. |
| `session.py` | Abre `web.whatsapp.com`, espera `#pane-side`, prompts no terminal; `ChromeDriverManager`. |
| `config.py` | Alvos, seletores, tempos de digitação, `load_alvos()`, `WHATSAPP_ONLY_UNREAD`. |
| `loop.py` | Por contato: sidebar ou `#main`, não lida (opcional), chat aberto, última mensagem recebida, cache, `faq_agente.responder`, envio. |
| `sidebar.py` | Lista lateral, nome do chat, não lidas, clique. |
| `composer.py` | Campo de mensagem, digitação pausada, Enter. |
| `messages.py` | JS + fallback Python para última bolha recebida (`data-id` / `message-in`). |
| `faq_agente.py` | Normalização, saudações, palavras-chave → respostas fixas. |

O `main.py` na raiz só reexporta `whatsapp_bot.cli:main` para quem prefere `python main.py`.

---

## Limitações

- O **DOM do WhatsApp Web** muda: CSS/XPath podem quebrar e precisar de manutenção.
- Mensagens **suas** precisam ser detectadas como saída (ex.: `Você:` em `data-pre-plain-text`); caso contrário o remetente pode ser confundido.
- O FAQ é **fixo** e limitado ao que está em `whatsapp_bot/faq_agente.py`.
