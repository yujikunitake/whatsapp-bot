from __future__ import annotations

import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .config import LIST_ROW_XPATH, NAO_LIDA_XPATH


def row_has_unread(row: WebElement) -> bool:
    try:
        return bool(row.find_elements(By.XPATH, NAO_LIDA_XPATH))
    except (StaleElementReferenceException, NoSuchElementException):
        return False


def row_matches_name(row: WebElement, name_cf: str) -> bool:
    try:
        for el in row.find_elements(By.XPATH, ".//span[@title]"):
            t = (el.get_attribute("title") or "").strip().casefold()
            if name_cf in t or t == name_cf:
                return True
        return name_cf in (row.text or "").strip().casefold()
    except StaleElementReferenceException:
        return False


def find_chat_row_by_name(driver: WebDriver, name: str) -> WebElement | None:
    name_cf = name.strip().casefold()
    if not name_cf:
        return None

    side = driver.find_element(By.ID, "pane-side")
    driver.execute_script("arguments[0].scrollTop = 0", side)
    time.sleep(0.1)

    last_top = None
    stagnant = 0
    for _ in range(120):
        for row in side.find_elements(By.XPATH, LIST_ROW_XPATH):
            try:
                if row.is_displayed() and row_matches_name(row, name_cf):
                    return row
            except StaleElementReferenceException:
                continue
        driver.execute_script("arguments[0].scrollTop += 320", side)
        time.sleep(0.12)
        top = driver.execute_script("return arguments[0].scrollTop", side)
        stagnant = stagnant + 1 if top == last_top else 0
        if stagnant >= 3:
            break
        last_top = top

    driver.execute_script("arguments[0].scrollTop = 0", side)
    return None


def click_chat(driver: WebDriver, el: WebElement) -> None:
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center', inline:'nearest'});", el
    )
    time.sleep(0.2)
    try:
        el.click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)


def main_mostrando_alvo(driver: WebDriver, alvo: str) -> bool:
    name_cf = alvo.strip().casefold()
    if not name_cf:
        return False
    try:
        header = driver.find_element(By.ID, "main").find_element(By.CSS_SELECTOR, "header")
    except NoSuchElementException:
        return False
    blob = (header.text or "").strip().casefold()
    if name_cf in blob:
        return True
    try:
        for span in header.find_elements(By.CSS_SELECTOR, "span[title]"):
            t = (span.get_attribute("title") or "").strip().casefold()
            if name_cf in t or t == name_cf:
                return True
    except StaleElementReferenceException:
        return False
    return False
