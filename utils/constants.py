import string

# URLs
SQUARDLE_URL = "https://squaredle.app"
SQUARDLE_EXPRESS_URL = f"{SQUARDLE_URL}/?level=xp"

# immutable facts of life
LETTERS: str = string.ascii_uppercase
MIN_WORD_LENGTH: int = 4

# North American Scrabble dictionary API. Its max word length is 15, whereas Squardle might have longer words.
DICTIONARY_API_URL = f"https://fly.wordfinderapi.com/api/search?exclude_letters={{}}&word_sorting=az&page_size=50&group_by_length=true&dictionary=otcwl&longer_than={MIN_WORD_LENGTH-1}"
DICTIONARY_API_URL_PAGINATED = "https://fly.wordfinderapi.com/api/search?exclude_letters={}&length={}&page_token={}&word_sorting=az&page_size=50&group_by_length=true&dictionary=otcwl"

# internally used constants
PLACEHOLDER_CHAR = "#"
HIDDEN_ELEMENT_DOM_LOCATION = {"x": 0, "y": 0}

if __name__ == "__main__":
    print(LETTERS)