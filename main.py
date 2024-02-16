import time
import argparse

from highscoringwords import HighScoringWords

def main(args: argparse.Namespace):
    words = HighScoringWords.from_files(
        valid_words=args.words,
        letter_values=args.values,
    )

    if args.number:
        words.MAX_LEADERBOARD_LENGTH = args.number
    if args.min_length:
        words.MIN_WORD_LENGTH = args.min_length

    start = time.time()

    if args.mode == "list":
        leaderboard = words.build_leaderboard_for_word_list()
    else:
        leaderboard = words.build_leaderboard_for_letters(args.string)

    end = time.time()
    
    for word in leaderboard:
        print(word)

    print()
    print(f"Execution time: {end - start:.3f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="HighScoringWords",
        description="Generates leaderboard of the n highest scoring words from a word list and letter values.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "mode",
        choices=["list", "letters"],
        help="Generate from the entire word list (list) or a subset of words built from a supplied string of characters (letters, requires --string arg).",
    )
    parser.add_argument(
        "-s",
        "--string",
        help="A string of letters from which to build words."
    )
    parser.add_argument(
        "-w",
        "--words",
        default="wordlist.txt",
        help="A text file containing the complete set of valid words, one word per line.",
    )
    parser.add_argument(
        "-v",
        "--values",
        default="letterValues.txt",
        help="A text file containing the score for each letter in the format letter:score one per line.",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="The maximum number of items that can appear in the leaderboard.",
        type=int
    )
    parser.add_argument(
        "-l",
        "--min_length",
        help="Words must be at least this many characters long.",
        type=int
    )

    args = parser.parse_args()

    if args.mode == "letters" and args.string is None:
        parser.error("letters mode requires --string")

    main(args)
