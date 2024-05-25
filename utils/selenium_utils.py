
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import constants


DRIVER = webdriver.Firefox()
AC = ActionChains(DRIVER)


def open_squardle_page(url: str = constants.SQUARDLE_URL):
    DRIVER.get(url)
    skip_tutorial()
    deny_cookies()
    # t = threading.Thread(target=deny_cookies, daemon=True)
    # t.start()
    # t.join()
    

def skip_tutorial():
    skip_tutorial_button = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "skipTutorial")))
    if skip_tutorial_button:
        AC.click(skip_tutorial_button).perform()
        confirm_skip_button = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable((By.ID, "confirmAccept")))
        AC.click(confirm_skip_button).perform()
        WebDriverWait(DRIVER, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "notTutorial")))


def deny_cookies():
    try:
        privacy_notice = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'We value your privacy')]")))
        continue_button = DRIVER.find_element(By.XPATH, "//button/span[contains(text(),'Continue')]")
        AC.click(continue_button).perform()
    except TimeoutException:
        pass
    accept_necessary_button = DRIVER.find_element(By.XPATH, "//button[contains(text(),'Accept necessary')]")
    if accept_necessary_button:
        AC.click(accept_necessary_button).perform()


def get_letter_from_square() -> list[list[str]]:
    letter_boxes = DRIVER.find_elements(By.XPATH, "//div[@class='board']//div[@class='unnecessaryWrapper']")
    letters: list[str] = []
    for box in letter_boxes:
        if box.location == constants.HIDDEN_ELEMENT_DOM_LOCATION:
            continue
        letters.append(box.text or constants.PLACEHOLDER_CHAR)
    return letters


def close_popups():
    for popup_id in ["bonusWordDialog", "wordOfTheDay"]:
        try:
            popup_panel = DRIVER.find_element(By.ID, popup_id)
            #if EC.visibility_of(popup_panel):
            if popup_panel.location != constants.HIDDEN_ELEMENT_DOM_LOCATION:
                #WebDriverWait(DRIVER, 0.1).until(EC.visibility_of(popup_panel))
                close_button = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[42]/h2/div/a")))  # TODO: more robust locator
                AC.click(close_button).perform()
        except (NoSuchElementException, MoveTargetOutOfBoundsException, TimeoutException) as e:
            pass
    try:
        close_button = DRIVER.find_element(By.XPATH, "//button[@id='explainerClose']")
        if close_button.location != constants.HIDDEN_ELEMENT_DOM_LOCATION:
            AC.click(close_button).perform()
    except (NoSuchElementException, MoveTargetOutOfBoundsException):
        pass

def enter_word(word: str):
    AC.send_keys(word).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
