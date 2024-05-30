import aiohttp
import asyncio
import json
import keyboard
import requests
import time

try:
    import constants
    import settings
except ModuleNotFoundError:
    from utils import constants
    from utils import settings


WORDLIST_ASYNC_LOCK = asyncio.Lock()


def enter_word_with_keyboard(word: str):
    """
    Enters the word with methods from the "keyboard" library.

    Args:
        word: word found on the square consisting only of lower-case English letters
    """
    keyboard.write(word, delay=settings.TYPING_DELAY_BETWEEN_CHARACTERS)
    time.sleep(settings.TYPING_DELAY_AFTER_LAST_CHARACTER)
    keyboard.press_and_release("enter")
    time.sleep(settings.TYPING_DELAY_AFTER_WORD)


def get_candidate_words(excluded_letters: str | list[str] | set[str]) -> list[str]:
    """
    Calls dictionary API to get words containing only letters present on the Squardle square.
    The response is paginated, limited to 50 words per word length, so additional calls
    might be needed (handled within this function).
    Note that this API has a max word length of 15, whereas Squardle accepts longer words too.

    Args:
        excluded_letters: iterable of letters that should be excluded from returned words
    Returns:
        all words received from the dictionary
    """
    if isinstance(excluded_letters, (list, set)):
        excluded_letters = "".join(excluded_letters)
    excluded_letters= excluded_letters.lower()

    print(f"polling for words with excluded letters '{excluded_letters}'...")
    res = requests.get(constants.DICTIONARY_API_URL.format(excluded_letters.lower()))
    response_dict = json.loads(res.text)
    words: list[str] = []
    additional_urls = []

    for page in response_dict["word_pages"]:
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


async def gather_additional_requests(word_list: list[str], urls: list[str]):
    """
    Triggers asynchronous get requests for additional paginated API calls.

    Args:
        word_list: word list instance to add the words to
        urls: paginated URLs to request for additional calls
    """
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        await asyncio.gather(*(get_additional_words(word_list, url, session) for url in urls))


async def get_additional_words(word_list: list[str], url: str, session: aiohttp.ClientSession):
    """
    Gets words from page 2 onwards of paginated API requests.

    Args:
        word_list: word list instance to add the words to
        url: one paginated URL to request
        session:
    """
    async with session.get(url=url) as response:
        res = await response.read()
        response_dict = json.loads(res)
        words: list[str] = []
        for page in response_dict["word_pages"]:
            if page["length"] < constants.MIN_WORD_LENGTH:
                continue
            for word_dict in page["word_list"]:
                words.append(word_dict["word"])
        async with WORDLIST_ASYNC_LOCK:
            word_list += words
        if settings.PRINT_POLLED_WORDS:
            print(words)


if __name__ == "__main__":
    l = "jqxdletgbs"
    settings.PRINT_POLLED_WORDS = True
    w = get_candidate_words(excluded_letters=l)
    print(w)
    with open("jqw2.txt", "w") as f:
        f.write(' '.join(w))