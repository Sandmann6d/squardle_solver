import aiohttp
import asyncio
import json
import requests

try:
    import constants
    import settings
except ModuleNotFoundError:
    from utils import constants
    from utils import settings


async def get_additional_words(word_list: list[str], url: str, session: aiohttp.ClientSession):
    async with session.get(url=url) as response:
        res = await response.read()
        response_dict = json.loads(res)
        words: list[str] = []
        for page in response_dict["word_pages"]:
            if page["length"] < constants.MIN_WORD_LENGTH:
                continue
            for word_dict in page["word_list"]:
                words.append(word_dict["word"])
        word_list += words
        if settings.PRINT_POLLED_WORDS:
            print(words)

async def gather_additional_requests(word_list: list[str], urls: list[str]):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(get_additional_words(word_list, url, session) for url in urls))


def get_candidate_words(excluded_letters: str | list[str]) -> list[str]:
    if isinstance(excluded_letters, list):
        excluded_letters = ''.join(excluded_letters)
    print(f"polling for words with excluded letters '{excluded_letters}'...")
    res = requests.get(constants.DICTIONARY_API_URL.format(excluded_letters.lower()))
    response_dict = json.loads(res.text)
    words: list[str] = []
    additional_urls = []
    for page in response_dict["word_pages"]:
        # if page["length"] < constants.MIN_WORD_LENGTH:
        #     continue
        for word_dict in page["word_list"]:
            words.append(word_dict["word"])
        if page["num_pages"] > 1:
            for i in range(2, page["num_pages"]+1):
                url = constants.DICTIONARY_API_URL_PAGINATED.format(excluded_letters, page["length"], i)
                additional_urls.append(url)
    if settings.PRINT_POLLED_WORDS:
        print(words)

    asyncio.run(gather_additional_requests(words, additional_urls))

    print(f"got {len(words)} words!")
    return words



if __name__ == '__main__':
    l = {'K', 'Y', 'V', 'C', 'H', 'J', 'P', 'X', 'U', 'Q', 'B', 'W', 'N', 'F', 'Z'}
    w = get_candidate_words(excluded_letters=''.join(l).lower())
    print(w)