import keyboard

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import constants
from utils import settings


try:
    DRIVER = webdriver.Firefox()
except Exception as e:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # keep browser open after script is done
    DRIVER = webdriver.Chrome(options=chrome_options)

AC = ActionChains(DRIVER)


def open_squardle_page(url: str = constants.SQUARDLE_URL):
    """
    Starts a browser and opens a Squardle. Blocks execution until tutorial and cookie popups are clicked away.

    Args:
        url: a URL to a Squardle puzzle. Default URL is the daily Squardle.
    """
    assert url.startswith(constants.SQUARDLE_URL), f"{url} needs to start with {constants.SQUARDLE_URL}"
    DRIVER.get(url)
    skip_tutorial()
    deny_cookies()
    

def skip_tutorial():
    """
    Clicks away the tutorial.
    """
    skip_tutorial_button = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "skipTutorial")))
    if skip_tutorial_button:
        AC.click(skip_tutorial_button).perform()
        confirm_skip_button = WebDriverWait(DRIVER, 10).until(EC.element_to_be_clickable((By.ID, "confirmAccept")))
        AC.click(confirm_skip_button).perform()
        WebDriverWait(DRIVER, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "notTutorial")))


def deny_cookies():
    """
    Clicks away cookie notices. (Since login is not implented, the WebDriver instance does not have stored cookies.)
    """
    try:
        privacy_notice = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'We value your privacy')]")))
        continue_button = DRIVER.find_element(By.XPATH, "//button/span[contains(text(), 'Continue')]")
        AC.click(continue_button).perform()
    except TimeoutException:
        pass
    accept_necessary_button = DRIVER.find_element(By.XPATH, "//button[contains(text(), 'Accept necessary')]")
    AC.click(accept_necessary_button).perform()


def get_letter_from_square() -> list[str]:
    """
    Reads out the letters of the Squaredle. Empty squares are filled with a placeholder character.

    Returns:
        one-dimensional list of letters on the square
    """
    letter_boxes = DRIVER.find_elements(By.XPATH, "//div[@class='board']//div[@class='unnecessaryWrapper']")
    letters: list[str] = []
    for box in letter_boxes:
        if box.location == constants.HIDDEN_ELEMENT_DOM_LOCATION:
            continue
        letters.append(box.text or constants.PLACEHOLDER_CHAR)
    return letters


def close_popups():
    """
    After entering a word, some popups might appear, some with a delayed close button. Clicks those away.
    """
    for popup_id in ["bonusWordDialog", "wordOfTheDay", "dialog", "allBonusWordsFound"]:
        try:
            popup_panel = DRIVER.find_element(By.ID, popup_id)
            if popup_panel.location != constants.HIDDEN_ELEMENT_DOM_LOCATION:
                close_button = WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[42]/h2/div/a")))  # TODO: more robust locator
                AC.click(close_button).perform()
        except TimeoutException as e:
            # TODO: close_button is not located reliably on every popup.
            # For now, we close those by pressing the Esc key.
            if settings.ENTER_WORDS_WITH_WEBDRIVER:
                    AC.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
            else:
                keyboard.press_and_release("esc")
            WebDriverWait(DRIVER, 5).until(EC.invisibility_of_element_located(popup_panel))
        except (NoSuchElementException, MoveTargetOutOfBoundsException, TimeoutException) as e:
            print(e.stacktrace)
    try:
        small_popup_close_button = DRIVER.find_element(By.XPATH, "//button[@id='explainerClose']")
        if small_popup_close_button.location != constants.HIDDEN_ELEMENT_DOM_LOCATION:
            AC.click(small_popup_close_button).perform()
    except (NoSuchElementException, MoveTargetOutOfBoundsException):
        pass


def enter_word_webdriver(word: str):
    """
    Enters the word by typing it with webdriver-native methods.
    
    Args:
        word: word found on the square consisting only of lower-case English letters
    """
    for i, char in enumerate(word):
        AC.send_keys(char).pause(settings.TYPING_DELAY_AFTER_LAST_CHARACTER if i == len(word) -1 
                                 else settings.TYPING_DELAY_BETWEEN_CHARACTERS)
    AC.key_down(Keys.ENTER).key_up(Keys.ENTER).pause(settings.TYPING_DELAY_AFTER_WORD).perform()
