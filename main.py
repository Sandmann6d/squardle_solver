from typing import Callable

from utils import settings
from utils.settings import debug_print
from utils import constants
from utils import selenium_utils as sel
from utils.word_utils import get_candidate_words, enter_word_with_keyboard
from utils.squardle_square import SquardleSquarePathFinder


enter_word: Callable = sel.enter_word_webdriver if settings.ENTER_WORDS_WITH_WEBDRIVER else enter_word_with_keyboard

def main(squaredle_url: str = constants.SQUARDLE_URL):
    sel.open_squardle_page(squaredle_url)
    found_letters = sel.get_letter_from_square()
    debug_print("found letters", "".join(found_letters))

    squardle_solver = SquardleSquarePathFinder(found_letters)
    squardle_solver.candidate_words = get_candidate_words(excluded_letters=squardle_solver.letters_to_exclude)
    squardle_solver.candidate_words.sort()

    for word in squardle_solver.candidate_words:
        if squardle_solver.find_path(word):
            print(word)
            enter_word(word)
            sel.close_popups()


if __name__ == "__main__":
    import os
    import sys
    squardle_url: str = constants.SQUARDLE_URL

    if sys.argv[0] == os.path.basename(__file__):
        """ started from command line """
        if len(sys.argv) > 1:  
            squardle_url = sys.argv[1]
    else:
        """ started in IDE, enter Squardle URL by altering code here """
        pass
        # squardle_url = "https://squaredle.app/?puzzle=arbor-day-24"
        # squardle_url = constants.SQUARDLE_EXPRESS_URL

    assert squardle_url.startswith(constants.SQUARDLE_URL), \
        f"entered URL {squardle_url} needs to start with {constants.SQUARDLE_URL}!"

    main(squardle_url)
