PRINT_POLLED_WORDS: bool = False

ENTER_WORDS_WITH_WEBDRIVER: bool = True  # if True, uses selenium typing methods, else the "keyboard" library

# delays to account for browser lagging, thus swallowing keystrokes
TYPING_DELAY_BETWEEN_CHARACTERS: float = 0.1  # in seconds, delay after each character
TYPING_DELAY_AFTER_LAST_CHARACTER: float = 0.5
TYPING_DELAY_AFTER_WORD: float = 0.3  # in seconds, delay after typing a word and hitting "enter"