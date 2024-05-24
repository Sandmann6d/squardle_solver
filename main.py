import keyboard
import time

from utils import selenium_utils as su
from utils import word_utils as wu
from utils.squardle_square import SquardleSquare



su.open_squardle_page()
found_letters = su.get_letter_square()

squardle_solver = SquardleSquare(found_letters)

for word in squardle_solver.candidate_words:
    if squardle_solver.find_path(word):
        print(word)
        keyboard.write(word, delay=0.05)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        #su.close_popups()