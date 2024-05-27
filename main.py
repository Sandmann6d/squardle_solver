from typing import Callable

from utils import settings
from utils import constants
from utils import selenium_utils as sel
from utils.word_utils import get_candidate_words, enter_word_with_keyboard
from utils.squardle_square import SquardleSquarePathFinder


enter_word: Callable = sel.enter_word_webdriver if settings.ENTER_WORDS_WITH_WEBDRIVER else enter_word_with_keyboard

def main(squaredle_url: str = constants.SQUARDLE_URL):
    sel.open_squardle_page(squaredle_url)
    found_letters = sel.get_letter_from_square()
    print(''.join(found_letters))

    squardle_solver = SquardleSquarePathFinder(found_letters)
    squardle_solver.candidate_words = get_candidate_words(excluded_letters=squardle_solver.letters_to_exclude)
    squardle_solver.candidate_words.sort()

    for word in squardle_solver.candidate_words:
        if squardle_solver.find_path(word):
            print(word)
            enter_word(word)
            sel.close_popups()


if __name__ == "__main__":
    squardle_url = "https://squaredle.app/?puzzle=arbor-day-24"
    main(squardle_url)