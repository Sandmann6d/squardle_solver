from utils import constants
from utils.word_utils import get_candidate_words


class SquardleSquarePathFinder:
    def __init__(self, letters: list[str]):
        self.letters: list[str] = letters
        # currently assumes that every squaredle is square, so len(row)==len(column)
        self.square_size = int(len(letters) ** 0.5)
        if self.square_size ** 2 != len(self.letters):
            raise ValueError(f"Squardle with {len(self.letters)} is not a square!")
        
        self.letter_square: list[list[str]] = [letters[i*self.square_size : (i+1)*self.square_size] for i in range(self.square_size)]
        self.print_word_square()
        
        self.all_grid_coordinates = [(i, j)
                                     for i in range(self.square_size)
                                     for j in range(self.square_size)]

        self.letters_contained = set(self.letters)
        self.letters_to_exclude = sorted(list(set(constants.LETTERS) - self.letters_contained))
        self.candidate_words = get_candidate_words(excluded_letters=''.join(self.letters_to_exclude).lower())
        self.candidate_words.sort()
        print("finished sortng")
        
    def print_word_square(self):
        print(*[' '.join(row) for row in self.letter_square], sep='\n')


    def is_letter_at_coordinate(self, letter, coordinate) -> bool:
        return self.letter_square[coordinate[0]][coordinate[1]] == letter

    def find_first_letter_coords(self, first_letter: str) -> list[tuple[int]]:
        possible_coords = []
        for coord in self.all_grid_coordinates:
            if self.is_letter_at_coordinate(first_letter, coord):
                possible_coords.append(coord)
        return possible_coords
        

    def coords_next_to(self, passed_cords: list[tuple[int]], coords: tuple[int]):
        x, y = coords
        possible = [(i, j)
                    for i in range(max(0, x-1), min(self.square_size, x+2))
                    for j in range(max(0, y-1), min(self.square_size, y+2))]
        return [c for c in possible if c not in passed_cords]


    def letter_in_coords_next_to(self, passed_coords: list[tuple[int]], current_coord: tuple[int], letter: str) -> list[tuple[int]]:
        candidate_coords = self.coords_next_to(passed_coords, current_coord)
        return [c for c in candidate_coords if self.is_letter_at_coordinate(letter, c)]


    def find_next_letter(self, word, word_index, current_letter_coords, passed_coords) -> bool:
        word_index += 1
        current_letter = word[word_index]
        for coord in current_letter_coords:
            passed_coords.append(coord)
            next_letter_coords = self.letter_in_coords_next_to(passed_coords, passed_coords[-1], current_letter)
            if word_index == len(word) - 1:
                return bool(next_letter_coords)
            if not next_letter_coords:
                passed_coords.pop()
                continue
            found_path = self.find_next_letter(word, word_index, next_letter_coords, passed_coords)
            if found_path:
                return True
        return False

    def find_path(self, word: str) -> bool:
        word = word.upper()
        first_letter_coords = self.find_first_letter_coords(word[0])
        word_available = self.find_next_letter(word, 0, first_letter_coords, [])
        return word_available

    
    