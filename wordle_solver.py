def read_word_list(file_path):
    """
    Reads a list of words from the given file and returns them as a list.

    Args:
        file_path (str): The path to the file containing the word list.

    Returns:
        list: A list of words from the file.
    """
    with open(file_path, "r") as file:
        word_list = file.readlines()
    word_list = [word.replace("\n", "") for word in word_list]
    return word_list


def calculate_letter_frequency(word_list):
    """
    Calculates the frequency of each letter in the given word list.

    Args:
        word_list (list): A list of words.

    Returns:
        dict: A dictionary containing letter frequencies.
    """
    letter_frequency = {}
    for word in word_list:
        for letter in word:
            letter_frequency[letter] = letter_frequency.get(letter, 0) + 1
    return dict(sorted(letter_frequency.items()))


def calculate_word_value(word_list, letter_frequency):
    """
    Calculates the value of each word in the given list based on the letter frequencies.

    Args:
        word_list (list): A list of words.
        letter_frequency (dict): A dictionary containing letter frequencies.

    Returns:
        dict: A dictionary containing word values.
    """
    word_list_values = {}
    for word in word_list:
        word_value = 0
        letter_count = {}
        for letter in word:
            if letter_count.get(letter, 0) == 0:
                word_value += letter_frequency[letter]
            letter_count[letter] = 1
        word_list_values[word] = word_value
    return word_list_values


def find_highest_valued_word(word_list_values):
    """
    Finds and returns the word with the highest value from the given word-value dictionary.

    Args:
        word_list_values (dict): A dictionary containing word values.

    Returns:
        str or None: The word with the highest value, or None if the dictionary is empty.
    """
    if not word_list_values:
        return None
    return max(word_list_values, key=word_list_values.get)


def filter_words(pattern, word_list, guessed_word):
    """
    Filters the word list based on the given pattern and guessed word.

    Args:
        pattern (str): A pattern containing 'G' for matched, 'Y' for unmatched, and 'N' for any.
        word_list (list): A list of words to be filtered.
        guessed_word (str): The word guessed so far.

    Returns:
        list: A new filtered word list.
    """
    unused_letters = []
    matched_letters = [None] * len(guessed_word)
    unmatched_letters = [None] * len(guessed_word)

    for pattern_char, guessed_char in zip(pattern, guessed_word):
        index = guessed_word.index(guessed_char)

        if pattern_char == 'N':
            if guessed_char not in guessed_word[:index] + guessed_word[index + 1:]:
                unused_letters.append(guessed_char)
        elif pattern_char == 'G':
            matched_letters[index] = guessed_char
        elif pattern_char == 'Y':
            if guessed_char not in guessed_word[:index] + guessed_word[index + 1:]:
                unmatched_letters[index] = guessed_char

    cleaned_word_list = [word.replace("\n", "") for word in word_list]
    new_word_list = []

    for word in cleaned_word_list:
        condition_1 = all(
            letter == matched_letters[index] or matched_letters[index] is None
            for index, letter in enumerate(word)
        )
        condition_2 = not any(unused_letter in word for unused_letter in unused_letters)
        condition_3 = word != guessed_word
        condition_4 = not any(
            unmatched_letters[index] is not None and unmatched_letters[index] == letter
            for index, letter in enumerate(word)
        )
        condition_5 = all(
            letter is None or (letter in word)
            for letter in unmatched_letters
        )

        if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
            new_word_list.append(word)

    return new_word_list


def main():
    word_list_file = "sanitized_words_1.txt"
    word_list = read_word_list(word_list_file)

    for i in range(6):
        letter_frequency = calculate_letter_frequency(word_list)
        word_value = calculate_word_value(word_list, letter_frequency)
        current_guess = find_highest_valued_word(word_value)

        if current_guess is None:
            print("No more words to guess. What was the Word?")
            word = input(" --> ")
            if word not in word_list:
                word_list.append(word)
                with open(word_list_file, "a") as file:
                    file.write(f"{word}\n")
            print(f"Godamn {word}!")
            return

        current_guess = current_guess.replace("\n", "")
        print(current_guess)

        invalid_response = True
        while invalid_response:
            pattern = str(input("What is correct? (GYN): ")).replace("\n", "")
            if len(pattern) == len(current_guess):
                invalid_response = False

        if all(char == 'G' for char in pattern):
            print("HAHA! I found the Word!")
            return

        word_list = filter_words(pattern, word_list, current_guess)

    print("What was the Word????")
    word = input(" --> ")
    if word not in word_list:
        word_list.append(word)
        with open(word_list_file, "a") as file:
            file.write(f"{word}\n")

    print(f"Bloody {word}!")
    main()


if __name__ == "__main__":
    main()
