import traceback
from logging import Logger
from config import WAIT_THRESHOLD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


def get_error_line(e) -> dict:
    tb = traceback.extract_tb(e.__traceback__)
    file_name, line_number, function_name, text = tb[-1]
    return {
        "file_name": file_name,
        "function_name": function_name,
        "text": text,
        "line_number": line_number,
    }


def resolve_path(path: str) -> By:
    path_mapping = {
        "id": By.ID,
        "xpath": By.XPATH,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
        "name": By.NAME,
        "tag_name": By.TAG_NAME,
        "class_name": By.CLASS_NAME,
        "css_selector": By.CSS_SELECTOR,
    }
    try:
        return path_mapping[path.lower()]
    except KeyError:
        raise ValueError(f"Unrecognized path: {path}")


def unpack_values(element: dict) -> tuple:
    path = element.get("path")
    path = resolve_path(path)
    value = element.get("value")
    type = element.get("type")
    name = element.get("name")
    return (name, type, value, path)


def dynamic_wait(wat: dict, element: dict):
    _, type, value, path = unpack_values(element)
    driver: WebDriver = wat.get("driver")
    web_driver_wait = WebDriverWait(driver, WAIT_THRESHOLD)
    if type == 'input': web_driver_wait.until(EC.visibility_of_element_located((path, value)))
    elif type == 'button': web_driver_wait.until(EC.element_to_be_clickable((path, value)))


def find_element_path(wat: dict, element: dict) -> WebElement:
    try:
        name, _, value, path = unpack_values(element)
        driver: WebDriver = wat.get("driver")
        lgr: Logger = wat.get("lgr")
        dynamic_wait(wat, element)
        lgr.info(f"Finding element {name}")
        return driver.find_element(path, value)
    except Exception as err:
        print(element)
        e = get_error_line(err)
        lgr.error(f"While finding element {name} at line number {e['line_number']}")


def wait_for_element_to_load(wat: dict, element: dict) -> None:
    try:
        name, _, value, path = unpack_values(element)
        driver: WebDriver = wat.get("driver")
        lgr: Logger = wat.get("lgr")
        dynamic_wait(wat, element)
        web_driver_wait = WebDriverWait(driver, WAIT_THRESHOLD)
        lgr.info(f"Waiting until {name} is located")
        web_driver_wait.until(EC.presence_of_element_located((path, value)))
        lgr.info(f"{name} is located")
    except Exception as err:
        e = get_error_line(err)
        lgr.error(f"While trying to locate {name} at line number {e['line_number']}")


def send_keys(wat: dict, text: str) -> None:
    try:
        element: WebElement = wat.get("element")
        lgr: Logger = wat.get("lgr")
        element.send_keys(text)
        lgr.info(f"Sending Input '{text}'")
    except Exception as err:
        e = get_error_line(err)
        lgr.error(f"While trying to input {text} at line number {e['line_number']}")


def click_button(wat: dict) -> None:
    try:
        element: WebElement = wat.get("element")
        lgr: Logger = wat.get("lgr")
        element.click()
        lgr.info(f"The button is clicked")
    except Exception as err:
        e = get_error_line(err)
        lgr.error(f"While trying to click the button at line number {e['line_number']}")

