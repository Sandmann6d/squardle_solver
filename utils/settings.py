import sys


PRINT_POLLED_WORDS: bool = False  # if True, prints words extracted for ever request

ENTER_WORDS_WITH_WEBDRIVER: bool = True  # if True, uses selenium typing methods, else the "keyboard" library (key inputs on OS level instead of browser)

# delays for nicer watching and perhaps to account for browser lagging
TYPING_DELAY_BETWEEN_CHARACTERS: float = 0.01  # in seconds, delay between each character
TYPING_DELAY_AFTER_LAST_CHARACTER: float = 0.1  # in seconds, delay after last character
TYPING_DELAY_AFTER_WORD: float = 0.1  # in seconds, delay after typing a word and hitting "enter"

# debug mode
DEBUG: bool = hasattr(sys, "gettrace") and sys.gettrace() is not None

def debug_print(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs)
