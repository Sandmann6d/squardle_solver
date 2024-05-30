# Selenium Squardle Solver

This script automatically solves Squardle puzzles. Running `main.py` will:
1) start a Selenium webbrowser and open a specified Squardle puzzle;
2) send get requests to a US Scrabble dictionary API for all words that exclude letters absent on the puzzle (like [word.tips](https://word.tips/words-with-letters/));
3) then, for each word, check whether it is playable on the puzzle and, if it is, enter it by typing and hitting the enter key.

https://github.com/Sandmann6d/squardle_solver/assets/97108287/36f964fe-28f7-4917-bfa5-152f048bdafc

### Installation
- Requires Python >= 3.10
- Create [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements, e.g.
`pip install -r requirements.txt`
- Have either Firefox or Chrome installed
  - (in case of Firefox, you may have to [install geckodriver](https://www.browserstack.com/guide/geckodriver-selenium-python#toc2))

### Usage
Either run `main.py` in the IDE and pass a Squardle URL to the `main()` function, or run it on the command line and pass a URL as an argument, suche as `python3 main.py "https://squaredle.app/?puzzle=poetry"`. If no argument is passed, the script will open the daily puzzle.

- Some customisation (such as typing delays) can be set in `utils/settings.py`.
- Automatic login is not implemented, and I am not planning to. No need to mess with the leaderboard.
- That means, only freely available puzzles can be solved.
- Reliance on the US Scrabble dictionary entails that
  - words longer than 15 characters are not considered.
  - puzzles created prior to Squardle's switch to this dictionary might not get solved perfectly.
