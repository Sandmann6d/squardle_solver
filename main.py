import utils.selenium_utils as selenium_utils


selenium_utils.open_squardle_page()
word_grid = selenium_utils.get_word_grid()
print(word_grid)