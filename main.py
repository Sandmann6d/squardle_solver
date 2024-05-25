import keyboard
import time

from utils import settings
from utils import constants
from utils import selenium_utils as su
from utils.squardle_square import SquardleSquarePathFinder


def main(squaredle_url = constants.SQUARDLE_URL):
    su.open_squardle_page(squaredle_url)
    found_letters = su.get_letter_from_square()

    squardle_solver = SquardleSquarePathFinder(found_letters)

    for word in squardle_solver.candidate_words:
        if not word.startswith('g'):
            continue
        if squardle_solver.find_path(word):
            print(word)
            keyboard.write(word, delay=settings.TYPING_DELAY_BETWEEN_CHARACTERS)
            keyboard.press_and_release('enter')
            #su.enter_word(word)
            time.sleep(settings.TYPING_DELAY_BETWEEN_WORDS)
            su.close_popups()

if __name__ == "__main__":
    squardle_url = "https://squaredle.app/?puzzle=hanukkah23"
    main(squardle_url)