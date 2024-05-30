# Selenium Squardle solver

This script automatically solves Squardle puzzles. Running `main.py` will:
1) start a selenium webbrowser and open a specified Squardle puzzle
2) send get requests to a US Scrabble dictionary API for all words that exclude letters absent on the puzzle
3) then, for each word, check whether it is playable on the puzzle and, if it is, enter it by typing and hitting the enter key

### Installation
- Install Python >= 3.10
- Create [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements, e.g.
`pip install -r requirements.txt`
- Have either Firefox or Chrome installed
  - in case of Firefox, [install geckodriver](https://www.browserstack.com/guide/geckodriver-selenium-python#toc2)

### Usage
Either run `main.py` in the IDE and pass a Squardle URL to the `main()` function, or run it on the command line and pass a URL as an argument, suche as `python3 main.py https://squaredle.app/?puzzle=poetry`. If no argument is passed, the script will open the daily puzzle.

