from typing import Tuple

from utils import constants

Coordinates = Tuple[int, int]


class SquardleSquarePathFinder:
    def __init__(self, letters_in_square: list[str]):
        """
        Args:
            letters_in_square: one-dimensional list of letters on the square
        """
        self.letters: list[str] = letters_in_square

        # currently assumes that every Squaredle is square, so len(row)==len(column)
        self.square_size = int(len(letters_in_square) ** 0.5)
        assert self.square_size ** 2 == len(self.letters), f"Squardle with {len(self.letters)} is not a square!"
        
        # convert one-dimensional list to nested lists to represent a square
        self.letter_square: list[list[str]] = [letters_in_square[i*self.square_size : (i+1)*self.square_size] for i in range(self.square_size)]
        self.print_word_square()
        
        self.all_grid_coordinates: list[Coordinates] = [(i, j)
                                                        for i in range(self.square_size)
                                                        for j in range(self.square_size)]

        self.letters_contained = set(self.letters)
        self.letters_to_exclude = sorted(list(set(constants.LETTERS) - self.letters_contained))
        self.candidate_words: list[str]  # to be filled from outside
        
    def print_word_square(self):
        print(*[" ".join(row) for row in self.letter_square], sep="\n")

    def is_letter_at_coordinate(self, letter: str, coordinate: Coordinates) -> bool:
        """
        Checks if a letter is on a given coordinate.

        Args:
            letter:
        Returns:
            (bool)
        """
        return self.letter_square[coordinate[0]][coordinate[1]] == letter

    def find_first_letter_coords(self, first_letter: str) -> list[Coordinates]:
        """
        Finds all coordinates that a given letter (first letter of a word) is on.

        Args:
            first_letter:
        Returns:
            all coordinates on the square with given letter
        """
        possible_coords = []
        for coord in self.all_grid_coordinates:
            if self.is_letter_at_coordinate(first_letter, coord):
                possible_coords.append(coord)
        return possible_coords

    def get_adjacent_letter_coords(self, current_coord: Coordinates, passed_coords: list[Coordinates]) -> list[Coordinates]:
        """
        Gets adjacent coordinates within the boundaries of the square, excluding those that have been passed.

        Args:
            current_coord:
            passed_coords:
        Returns:
            possible coordinates for the next letter
        """
        x, y = current_coord
        adjacent_coords = [(i, j)
                           for i in range(max(0, x-1), min(self.square_size, x+2))
                           for j in range(max(0, y-1), min(self.square_size, y+2))]
        return [c for c in adjacent_coords if c not in passed_coords]

    def get_adjacent_coords_with_letter(self, current_coord: Coordinates, letter: str, passed_coords: list[Coordinates]) -> list[Coordinates]:
        """
        Gets adjacent coordinates that contain and are valid for the letter in question.

        Args:
            current_coord:
            letter:
            passed_coords:
        Returns:
            valid coordinates for the next letter (could be empty list)
        """
        candidate_coords = self.get_adjacent_letter_coords(current_coord, passed_coords)
        return [c for c in candidate_coords if self.is_letter_at_coordinate(letter, c)]

    def find_next_letter(self, word: str, word_index: int, current_letter_coords: list[Coordinates], passed_coords: list[Coordinates]) -> bool:
        """
        Starting from coordinates for the first letter, recursively goes through the rest of the word
        to find a path for the entire word.

        Args:
            word:
            word_index: index in the word of current letter
            current_letter_coords: all valid coordinates that contain the current letter
            passed_coords: list of coordinates with the path travelled so far
        Returns:
            (bool) whether a path exists spanning to the last letter 
        """
        word_index += 1
        current_letter = word[word_index]

        if word_index == len(word) - 1:  # at the last letter, if it has candidate coordinates, word mst have a path
            return bool(current_letter_coords)
        
        for i, coord in enumerate(current_letter_coords):
            passed_coords.append(coord)
            next_letter_coords = self.get_adjacent_coords_with_letter(passed_coords[-1], current_letter, passed_coords)
            #print(word_index, word[:word_index], current_letter_coords, "curr:", coord, "so far:", passed_coords)

            if not next_letter_coords:
                p = passed_coords.pop()
                #print("popped and continue:", p, self.letter_square[p[0]][p[1]])
                continue
            found_path = self.find_next_letter(word, word_index, next_letter_coords, passed_coords)
            if found_path:  # if path is found, abort the search immediately and return positive result
                return True
            else:
                p = passed_coords.pop()
                #print("popped in else:", p, self.letter_square[p[0]][p[1]])
        return False

    def find_path(self, word: str) -> bool:
        """
        Tries to find a path for a word on the qiven square.

        Args:
            word: word to be found
        Returns:
            (bool) whether a path exists for the given word
        """
        word = word.upper()
        first_letter_coords = self.find_first_letter_coords(word[0])
        word_available = self.find_next_letter(word, 0, first_letter_coords, [])
        return word_available
