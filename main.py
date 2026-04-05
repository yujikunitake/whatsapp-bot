"""Compat: `uv run python main.py` — equivalente a `uv run python -m whatsapp_bot`."""

from __future__ import annotations

from whatsapp_bot.cli import main

if __name__ == "__main__":
    main()
