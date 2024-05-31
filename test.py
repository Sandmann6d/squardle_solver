# import pytest

from utils.squardle_square import SquardleSquarePathFinder
from utils import settings


settings.DEBUG = True

print('\nthis is amazing unit testing\n')

arbor_day_puzzle_letters = "SPRWALNUCHWMNUCHAZTENOLEACIENSDLMIRMKALUTAWBEAPOTMEROECDLPRRGVAHUOEYWEONMAGOWNHSROCYWDOIACEFSRESRPEF"

path_finder = SquardleSquarePathFinder(list(arbor_day_puzzle_letters))

present_words = ["acai", "archaeans", "acacia"]
absent_words = ["accountant", "army", "almanac"]
difficult_to_find_words = ["aloe", "acclaimed", "antelope"]  # words the algorithm has struggled with finding
mistakenly_found_words = ["aahed", "acclaimes", "acacias"]  # words the algorithm has hallucinated
non_existent_starting_letter_words = ["q", "jail", "xernias"]


def test_find_present_words():
    for word in present_words:
        assert path_finder.find_path(word) is True
        print(f"found {word.upper()} successfully!")


def test_do_not_find_absent_words():
    for word in absent_words:
        assert path_finder.find_path(word) is False
        print(f"did not find {word.upper()}, successfully!")


def test_find_difficult_words():
    for word in difficult_to_find_words:
        assert path_finder.find_path(word) is True
        print(f"found {word.upper()} successfully!")


def test_do_not_find_hallucinated_words():
    for word in mistakenly_found_words:
        assert path_finder.find_path(word) is False
        print(f"did not find {word.upper()}, successfully!")


def test_do_not_find_non_existent_starting_letter_words():
    for word in non_existent_starting_letter_words:
        assert path_finder.find_path(word) is False
        print(f"did not find {word.upper()}, successfully!")


def test_path_finder():
    test_find_present_words()
    test_do_not_find_absent_words()
    test_find_difficult_words()
    test_do_not_find_hallucinated_words()
    test_do_not_find_non_existent_starting_letter_words()
    print("tests passed!")


if __name__ == "__main__":
    test_path_finder()