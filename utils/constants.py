import string


SQUARDLE_URL = "https://squaredle.app/"
SQUARDLE_EXPRESS_URL = f"{SQUARDLE_URL}?level=xp"


DICTIONARY_API_URL = "https://fly.wordfinderapi.com/api/search?exclude_letters={}&word_sorting=points&group_by_length=true&dictionary=otcwl"


LETTERS: str = string.ascii_uppercase
MIN_WORD_LENGTH: int = 4

if __name__ == '__main__':
    print(LETTERS)