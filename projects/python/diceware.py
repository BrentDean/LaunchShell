#!/usr/bin/env python3
"""
Diceware-style passphrase generator.

Files needed in the same folder:

    diceware.py
    eff_diceware.txt

Run:

    python3 diceware.py

The program will ask how many words you want.
Each Diceware word is selected using five dice rolls.
"""

import math
import secrets
from pathlib import Path


DICE_SIDES = "123456"
ROLLS_PER_WORD = 5
DEFAULT_WORD_COUNT = 6
DEFAULT_WORDLIST = "eff_diceware.txt"


def load_wordlist(path: Path) -> dict[str, str]:
    """Load a Diceware word list formatted like: 11111 abacus."""
    wordlist: dict[str, str] = {}

    if not path.exists():
        raise FileNotFoundError(f"Word list not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(maxsplit=1)

            if len(parts) != 2:
                raise ValueError(f"Bad line {line_number}: {raw_line.rstrip()}")

            dice_key, word = parts
            word = word.strip()

            if not is_valid_dice_key(dice_key):
                raise ValueError(f"Bad dice key on line {line_number}: {dice_key}")

            if dice_key in wordlist:
                raise ValueError(f"Duplicate dice key on line {line_number}: {dice_key}")

            wordlist[dice_key] = word

    if not wordlist:
        raise ValueError(f"No words loaded from: {path}")

    return wordlist


def is_valid_dice_key(dice_key: str) -> bool:
    """Return True if the key looks like five dice rolls, such as 12345."""
    return (
        len(dice_key) == ROLLS_PER_WORD
        and all(character in DICE_SIDES for character in dice_key)
    )


def roll_die() -> int:
    """Roll one secure virtual six-sided die."""
    return secrets.randbelow(6) + 1


def roll_for_word() -> str:
    """Roll five dice to create one Diceware lookup key."""
    rolls = []

    for _ in range(ROLLS_PER_WORD):
        rolls.append(str(roll_die()))

    return "".join(rolls)


def generate_passphrase(
    wordlist: dict[str, str],
    word_count: int,
) -> tuple[list[str], list[str]]:
    """Generate dice keys and matching words."""
    dice_keys = []
    words = []

    for _ in range(word_count):
        dice_key = roll_for_word()

        if dice_key not in wordlist:
            raise KeyError(
                f"Dice key {dice_key} was not found in the word list. "
                "The word list may be incomplete."
            )

        dice_keys.append(dice_key)
        words.append(wordlist[dice_key])

    return dice_keys, words


def entropy_bits(word_count: int, wordlist_size: int) -> float:
    """Estimate passphrase entropy in bits."""
    return word_count * math.log2(wordlist_size)


def describe_strength(bits: float) -> str:
    """Return a plain-English strength label."""
    if bits < 50:
        return "weak for important accounts"
    if bits < 65:
        return "okay for low-risk use"
    if bits < 80:
        return "strong"
    if bits < 100:
        return "very strong"
    return "extremely strong"


def ask_word_count() -> int:
    """Ask how many Diceware words to generate."""
    while True:
        answer = input(f"How many words do you want? [{DEFAULT_WORD_COUNT}]: ").strip()

        if not answer:
            return DEFAULT_WORD_COUNT

        try:
            word_count = int(answer)
        except ValueError:
            print("Please enter a number.")
            continue

        if word_count < 1:
            print("Please enter 1 or higher.")
            continue

        return word_count


def ask_separator() -> str:
    """Ask what separator should go between words."""
    print()
    print("Choose a separator:")
    print("1. hyphen: word-word-word")
    print("2. space:  word word word")
    print("3. none:   wordwordword")
    print("4. custom")

    while True:
        answer = input("Separator choice [1]: ").strip()

        if not answer or answer == "1":
            return "-"

        if answer == "2":
            return " "

        if answer == "3":
            return ""

        if answer == "4":
            return input("Enter custom separator: ")

        print("Choose 1, 2, 3, or 4.")


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question."""
    default_label = "Y/n" if default else "y/N"

    while True:
        answer = input(f"{prompt} [{default_label}]: ").strip().lower()

        if not answer:
            return default

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


def print_intro() -> None:
    """Print a short beginner-friendly intro."""
    print()
    print("Diceware Passphrase Generator")
    print("-----------------------------")
    print("Why leave your password up to the luck of the dice?")
    print()
    print("This program uses secure virtual dice rolls to choose random words")
    print("from a Diceware word list.")
    print()
    print("Each word uses 5 dice rolls.")
    print("More words = more possible passphrases = harder to crack.")
    print()


def print_result(
    words: list[str],
    dice_keys: list[str],
    separator: str,
    show_rolls: bool,
    wordlist_size: int,
) -> None:
    """Print the final passphrase and basic stats."""
    passphrase = separator.join(words)
    word_count = len(words)
    total_rolls = word_count * ROLLS_PER_WORD
    bits = entropy_bits(word_count, wordlist_size)
    strength = describe_strength(bits)

    print()
    print("Your passphrase")
    print("---------------")
    print(passphrase)
    print()
    print(f"Words: {word_count}")
    print(f"Virtual dice rolls: {total_rolls}")
    print(f"Word list size: {wordlist_size}")
    print(f"Estimated entropy: {bits:.1f} bits")
    print(f"Strength: {strength}")

    if show_rolls:
        print(f"Dice keys: {' '.join(dice_keys)}")

    print()
    print("Important:")
    print("- Save this in a password manager.")
    print("- Do not reuse it across multiple accounts.")
    print("- Longer passphrases are stronger.")


def main() -> None:
    wordlist_path = Path(DEFAULT_WORDLIST)
    wordlist = load_wordlist(wordlist_path)

    print_intro()

    word_count = ask_word_count()
    total_rolls = word_count * ROLLS_PER_WORD

    print()
    print(f"{word_count} words will use {total_rolls} virtual dice rolls.")

    separator = ask_separator()
    show_rolls = ask_yes_no("Show the dice keys used?", default=False)

    dice_keys, words = generate_passphrase(wordlist, word_count)

    print_result(
        words=words,
        dice_keys=dice_keys,
        separator=separator,
        show_rolls=show_rolls,
        wordlist_size=len(wordlist),
    )


if __name__ == "__main__":
    main()