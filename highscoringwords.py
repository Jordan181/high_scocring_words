__author__ = 'codesse'
# Developed using Python 3.11.6

import bisect

from attr import dataclass

@dataclass(frozen=True)
class ScoredWord:
    word: str
    value: int

    def __str__(self) -> str:
        return f"{self.word}: {self.value}"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, ScoredWord) 
                and self.word == other.word
                and self.value == other.value)
    
class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values: dict[str, int]
    valid_words: set[str]

    def __init__(self, valid_words: set[str], letter_values: dict[str, int]):
        """
        Initialise the class with complete set of valid words and letter values
        :param word_list: a list of words
        :param letter_values: a dictionary mapping each letter to a value
        :return:
        """
        if not valid_words:
            raise ValueError("word_list is None or empty")
        if not letter_values:
            raise ValueError("letter_values is None or empty")

        if len(letter_values) != 26:
            raise ValueError("Letter values not provided for all letters")
        
        self.valid_words = valid_words
        self.letter_values = letter_values


    @staticmethod
    def from_files(valid_words='wordlist.txt', letter_values='letterValues.txt') -> "HighScoringWords":
        """
        Create the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        words = set()
        with open(valid_words) as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    words.add(word)

        values = {}
        with open(letter_values) as f:
            for line in f:
                (key, val) = line.split(':')
                values[str(key).strip().lower()] = int(val)

        return HighScoringWords(words, values)

    def build_leaderboard_for_word_list(self) -> list[ScoredWord]:
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """
        leaderboard = []

        for word in self.valid_words:
            self._add_to_leaderboard(leaderboard, word)

        return leaderboard

    def build_leaderboard_for_letters(self, starting_letters: str) -> list[ScoredWord]:
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """
        leaderboard = []
        letter_counts = self._count_letters(starting_letters)

        for word in self.valid_words:
            if self._can_word_be_built_from_letters(word, letter_counts):
                self._add_to_leaderboard(leaderboard, word)

        return leaderboard
  
    def _add_to_leaderboard(self, leaderboard: list[ScoredWord], word: str) -> None:
        if len(word) < self.MIN_WORD_LENGTH:
            return

        score = self._calculate_score(word)

        if (
            len(leaderboard) == self.MAX_LEADERBOARD_LENGTH and
            score < leaderboard[-1].value
        ):
            return

        scored_word = ScoredWord(word, score)

        # Get insertion index based on value
        index = bisect.bisect_right(leaderboard, -scored_word.value, key=lambda x: -x.value)

        # Ensure alphabetical ordering
        while (
            index > 0 and
            leaderboard[index - 1].value == scored_word.value and
            leaderboard[index - 1].word > scored_word.word
        ):
            index -= 1

        leaderboard.insert(index, scored_word)

        if len(leaderboard) > self.MAX_LEADERBOARD_LENGTH:
            leaderboard.pop()

    def _calculate_score(self, word: str) -> int:
        score = 0
        for c in word:
            score += self.letter_values[c]

        return score
    
    @staticmethod
    def _can_word_be_built_from_letters(word: str, letter_counts: dict[str, int]) -> bool:
        word_letters = {}
        for c in word:
            if c not in letter_counts:
                return False
            
            if c not in word_letters:
                word_letters[c] = 0
            word_letters[c] += 1

            if word_letters[c] > letter_counts[c]:
                return False
        
        return True
    
    @staticmethod
    def _count_letters(letters: str) -> dict[str, int]:
        counts = {}
        for c in letters:
            if c not in counts:
                counts[c] = 0
            counts[c] += 1
        
        return counts
