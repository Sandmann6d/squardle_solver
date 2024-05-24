import json
import requests

import constants


def get_candidate_words(excluded_letters: str | list[str]) -> list[str]:
    if isinstance(excluded_letters, list):
        excluded_letters = ''.join(excluded_letters)
    res = requests.get(constants.DICTIONARY_API_URL.format(excluded_letters.lower()))
    response_dict = json.loads(res.text)
    words: list[str] = []
    for page in response_dict['word_pages']:
        if page['length'] < constants.MIN_WORD_LENGTH:
            continue
        for word_dict in page['word_list']:
            words.append(word_dict['word'])
    return words


if __name__ == '__main__':
    w = get_candidate_words("abfghjkmnopqrstuwxyz")
    print(w)