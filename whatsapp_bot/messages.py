from __future__ import annotations

import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

_RE_SO_HORA = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?$")
_RE_SO_DATA_CURTA = re.compile(r"^(ontem|hoje|today|yesterday)$", re.I)


def _texto_util_mensagem(s: str) -> bool:
    t = (s or "").strip()
    if not t:
        return False
    if _RE_SO_HORA.fullmatch(t):
        return False
    if _RE_SO_DATA_CURTA.fullmatch(t):
        return False
    return True


_ULTIMA_RECEBIDA_JS = """
(function () {
  const main = document.querySelector("#main");
  if (!main) return [null, null];
  const footer = main.querySelector("footer");
  const header = main.querySelector("header");

  function looksLikeOnlyTimeOrMeta(s) {
    const t = (s || "").trim();
    if (!t) return true;
    if (/^\\d{1,2}:\\d{2}(?::\\d{2})?$/.test(t)) return true;
    if (/^\\d{1,2}:\\d{2}\\s*(a|p)\\.?m\\.?$/i.test(t)) return true;
    if (/^(ontem|hoje|today|yesterday)$/i.test(t)) return true;
    return false;
  }

  function isOutgoing(b) {
    const preEl = b.querySelector("[data-pre-plain-text]");
    const pre = preEl ? preEl.getAttribute("data-pre-plain-text") || "" : "";
    if (
      pre.indexOf("Você:") !== -1 ||
      pre.indexOf("Voce:") !== -1 ||
      pre.indexOf("You:") !== -1 ||
      pre.indexOf("Tu:") !== -1
    )
      return true;
    return !!b.closest(`[class*="message-out"]`);
  }

  function bubbleText(root) {
    if (!root) return "";
    const sel =
      "span.selectable-text, span[dir='auto'], .copyable-text span, div span span";
    const nodes = Array.from(root.querySelectorAll(sel));
    let lastGood = "";
    for (let i = 0; i < nodes.length; i++) {
      const raw = (nodes[i].innerText || "").trim();
      if (!raw || looksLikeOnlyTimeOrMeta(raw)) continue;
      lastGood = raw;
    }
    return lastGood;
  }

  const bubbles = Array.from(main.querySelectorAll("[data-id]")).filter(function (b) {
    if (footer && footer.contains(b)) return false;
    if (header && header.contains(b)) return false;
    const r = b.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  });

  for (let i = bubbles.length - 1; i >= 0; i--) {
    const b = bubbles[i];
    if (isOutgoing(b)) continue;
    const text = bubbleText(b);
    if (text) return [text, b.getAttribute("data-id")];
  }

  const copyables = Array.from(main.querySelectorAll(".copyable-text[data-pre-plain-text]")).filter(
    function (el) {
      if (footer && footer.contains(el)) return false;
      if (header && header.contains(el)) return false;
      return true;
    }
  );
  for (let i = copyables.length - 1; i >= 0; i--) {
    const el = copyables[i];
    const pre = el.getAttribute("data-pre-plain-text") || "";
    if (
      pre.indexOf("Você:") !== -1 ||
      pre.indexOf("Voce:") !== -1 ||
      pre.indexOf("You:") !== -1 ||
      pre.indexOf("Tu:") !== -1
    )
      continue;
    const text = bubbleText(el);
    if (!text) continue;
    const host = el.closest("[data-id]");
    return [text, host ? host.getAttribute("data-id") : null];
  }

  return [null, null];
})()
"""


def ultima_mensagem_recebida_meta(driver) -> tuple[str | None, str | None]:
    try:
        raw = driver.execute_script("return " + _ULTIMA_RECEBIDA_JS)
        if raw and isinstance(raw, (list, tuple)) and len(raw) >= 2:
            texto, mid = raw[0], raw[1]
            if texto and str(texto).strip():
                return str(texto).strip(), (str(mid).strip() or None) if mid else None
    except Exception:
        pass

    return _ultima_mensagem_recebida_meta_python(driver)


def _ultima_mensagem_recebida_meta_python(driver) -> tuple[str | None, str | None]:
    main = driver.find_element(By.ID, "main")

    rows = main.find_elements(By.CSS_SELECTOR, "div.message-in[data-id]")
    if rows:
        row = rows[-1]
        mid = (row.get_attribute("data-id") or "").strip() or None
        spans = row.find_elements(
            By.CSS_SELECTOR,
            "span.selectable-text, span[dir='auto'], .copyable-text span, div span span",
        )
        best = ""
        for el in spans:
            tx = (el.text or "").strip()
            if _texto_util_mensagem(tx):
                best = tx
        if best:
            return best, mid
        return None, mid

    for css in (
        "div.message-in span.selectable-text",
        "div.message-in span[dir='auto']",
        "div.message-in .copyable-text span",
    ):
        els = main.find_elements(By.CSS_SELECTOR, css)
        best = ""
        for el in els:
            tx = (el.text or "").strip()
            if _texto_util_mensagem(tx):
                best = tx
        if best:
            return best, None

    els = main.find_elements(
        By.XPATH,
        ".//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]",
    )
    best = ""
    for el in els:
        tx = (el.text or "").strip()
        if _texto_util_mensagem(tx):
            best = tx
    if best:
        return best, None

    try:
        spans = main.find_elements(By.CSS_SELECTOR, "span.selectable-text, span[dir='auto']")
        best = ""
        for el in spans:
            if not el.is_displayed():
                continue
            try:
                el.find_element(By.XPATH, "./ancestor::div[contains(@class,'message-out')][1]")
                continue
            except NoSuchElementException:
                pass
            try:
                el.find_element(By.XPATH, "./ancestor::footer[1]")
                continue
            except NoSuchElementException:
                pass
            tx = (el.text or "").strip()
            if _texto_util_mensagem(tx):
                best = tx
        if best:
            return best, None
    except NoSuchElementException:
        pass

    return None, None
