import json
import requests

try:
    import constants
except ModuleNotFoundError:
    from utils import constants


def parse_response(url: str) -> list[str]:
    res = requests.get(url)
    
    response_dict = json.loads(res.text)
    words: list[str] = []
    for page in response_dict["word_pages"]:
        if page["length"] < constants.MIN_WORD_LENGTH:
            continue
        for word_dict in page["word_list"]:
            words.append(word_dict["word"])
    print(words)
    return words


def get_candidate_words(excluded_letters: str | list[str]) -> list[str]:
    print("polling for words...")
    if isinstance(excluded_letters, list):
        excluded_letters = ''.join(excluded_letters)
    res = requests.get(constants.DICTIONARY_API_URL.format(excluded_letters.lower()))
    response_dict = json.loads(res.text)
    words: list[str] = []
    for page in response_dict["word_pages"]:
        if page["length"] < constants.MIN_WORD_LENGTH:
            continue
        for word_dict in page["word_list"]:
            words.append(word_dict["word"])
        if page["num_pages"] > 1:
            for i in range(2, page["num_pages"]+1):
                url = constants.DICTIONARY_API_URL_PAGINATED.format(excluded_letters, page["length"], i)
                words += parse_response(url)
    print(f"got {len(words)} words!")
    return words



if __name__ == '__main__':
    l = {'K', 'Y', 'V', 'C', 'H', 'J', 'P', 'X', 'U', 'Q', 'B', 'W', 'N', 'F', 'Z'}
    w = get_candidate_words(excluded_letters=''.join(l).lower())
    print(w)