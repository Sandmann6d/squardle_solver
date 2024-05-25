import string


SQUARDLE_URL = "https://squaredle.app/"
SQUARDLE_EXPRESS_URL = f"{SQUARDLE_URL}?level=xp"


DICTIONARY_API_URL = "https://fly.wordfinderapi.com/api/search?exclude_letters={}&word_sorting=az&page_size=50&group_by_length=true&dictionary=otcwl&longer_than=3"
DICTIONARY_API_URL_PAGINATED = "https://fly.wordfinderapi.com/api/search?exclude_letters={}&length={}&page_token={}&page_size=50&word_sorting=az&group_by_length=true&dictionary=otcwl&longer_than=3"

LETTERS: str = string.ascii_uppercase
MIN_WORD_LENGTH: int = 4

PLACEHOLDER_CHAR = '#'

HIDDEN_ELEMENT_DOM_LOCATION = {'x': 0, 'y': 0}

if __name__ == '__main__':
    print(LETTERS)