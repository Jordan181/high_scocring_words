import string
from unittest import TestCase

from highscoringwords import HighScoringWords, ScoredWord


class TestHighScoringWords(TestCase):
    # Sets value of letter to its position in alphabet
    DEFAULT_LETTER_VALUES = {
        c: ind + 1 for ind, c in enumerate(string.ascii_lowercase)
    }

    def test_raises_value_error_for_none_args(self):
        with self.assertRaises(ValueError):
            HighScoringWords(valid_words=None, letter_values=self.DEFAULT_LETTER_VALUES)

        with self.assertRaises(ValueError):
            HighScoringWords(valid_words=["aaa"], letter_values=None)

    def test_raises_value_error_if_no_valid_words(self):
        with self.assertRaises(ValueError):
            HighScoringWords(valid_words=[], letter_values=self.DEFAULT_LETTER_VALUES)

    def test_raises_value_error_if_missing_letter_values(self):
        with self.assertRaises(ValueError):
            HighScoringWords(valid_words=["aaa"], letter_values={"A": 1, "B": 2})

    def test_leaderboard_created_for_word_list(self):
        test_words = [
            "confuse",
            "silent",
            "second",
            "awake",
            "dusty",
            "spiritual",
            "listen",
            "dull",
            "applaud",
            "tease",
        ]

        expected = [
            ScoredWord("spiritual", 125),
            ScoredWord("dusty", 89),
            ScoredWord("confuse", 83),
            ScoredWord("listen", 79),
            ScoredWord("silent", 79),
        ]

        words = HighScoringWords(test_words, self.DEFAULT_LETTER_VALUES)
        words.MAX_LEADERBOARD_LENGTH = 5

        leaderboard = words.build_leaderboard_for_word_list()

        self.assertListEqual(expected, leaderboard)

    def test_leaderboard_excludes_words_shorter_than_min_length(self):
        test_words = [
            "silent",
            "dusty",
            "spiritual",
            "listen",
            "confuse",
            "aa",
            "a"
        ]

        expected = [
            ScoredWord("spiritual", 125),
            ScoredWord("dusty", 89),
            ScoredWord("confuse", 83),
            ScoredWord("listen", 79),
            ScoredWord("silent", 79),
        ]

        words = HighScoringWords(test_words, self.DEFAULT_LETTER_VALUES)
        words.MAX_LEADERBOARD_LENGTH = 10
        words.MIN_WORD_LENGTH = 3

        leaderboard = words.build_leaderboard_for_word_list()

        self.assertListEqual(expected, leaderboard)
    
    def test_leaderboard_created_for_letters(self):
        test_words = [
            "applaud",
            "tease",
            "road",
            "read",
            "adore",
        ]

        expected = [
            ScoredWord("adore", 43),
            ScoredWord("road", 38),
            ScoredWord("read", 28),
        ]

        words = HighScoringWords(test_words, self.DEFAULT_LETTER_VALUES)

        leaderboard = words.build_leaderboard_for_letters("deora")

        self.assertListEqual(expected, leaderboard)

    def test_leaderboard_created_for_letters_respects_letter_occurences(self):
        test_words = [
            "bul",
            "bulx",
            "bukll"
        ]

        expected = [
            ScoredWord("bulx", 59),
            ScoredWord("bul", 35),
        ]

        words = HighScoringWords(test_words, self.DEFAULT_LETTER_VALUES)

        leaderboard = words.build_leaderboard_for_letters("bulx")

        self.assertListEqual(expected, leaderboard)
