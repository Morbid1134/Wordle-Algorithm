import random
from tqdm import tqdm


def get_word_list(file_path):
    with open(file_path, "r") as file:
        word_list = file.readlines()
        file.close()
        return word_list


def get_letter_frequency(word_list):
    letter_frequency = {}
    for word in word_list:
        word = word.replace("\n", "")
        for letter in word:
            letter_frequency[letter] = letter_frequency.get(letter, 0) + 1
    return dict(sorted(letter_frequency.items()))


def get_word_value(word_list, letter_frequency):
    word_list_values = {}
    for word in word_list:
        word = word.replace("\n", "")
        word_value = 0
        letter_count = {}
        for letter in word:
            if letter_count.get(letter, 0) == 0:
                word_value += letter_frequency[letter]
            letter_count[letter] = 1
        word_list_values[word] = word_value
    return word_list_values



def get_highest_valued_word(word_list_values):
    return max(word_list_values, key=word_list_values.get)


def make_a_guess(guessed_word, answer, word_list):
    solved = False
    if guessed_word == answer:
        solved = True
        return (solved, None)

    unused_letters = []
    matched_letters = []
    unmatched_letters = []

    for index, letter in enumerate(guessed_word):
        if letter not in answer:
            unmatched_letters.append(None)
            matched_letters.append(None)
            if letter not in unused_letters:
                unused_letters.append(letter)
        elif letter == answer[index]:
            matched_letters.append(letter)
            unmatched_letters.append(None)
        else:
            matched_letters.append(None)
            unmatched_letters.append(letter)

    word_list = remove_words(unused_letters, matched_letters, unmatched_letters, word_list, guessed_word)
    return (solved, word_list)
    

def remove_words(unused_letters, matched_letters, unmatched_letters, word_list, guessed_word):
    # Remove newline characters from the words and store them in a new list
    cleaned_word_list = [word.replace("\n", "") for word in word_list]

    # Filter words that meet the conditions
    new_word_list = [
        word
        for word in cleaned_word_list
        if all(
            letter == matched_letters[index] or matched_letters[index] is None
            for index, letter in enumerate(word)
        )
        and not any(unused_letter in word for unused_letter in unused_letters)
        and word != guessed_word
        and not any(
            unmatched_letters[index] is not None and unmatched_letters[index] == letter
            for index, letter in enumerate(word)
        )
        and all(
            letter is None or (letter in word)
            for letter in unmatched_letters
        )
    ]

    return new_word_list



def main(answer, word_list):
    solved = False
    guesses = []
    static_guesses = []
    while solved == False:
        letter_frequency = get_letter_frequency(word_list)
        word_list_values = get_word_value(word_list, letter_frequency)
        highest_valued_word = get_highest_valued_word(word_list_values)

        guess = None
        if static_guesses:
            guess = static_guesses[0]
            del static_guesses[0]
        else:
            guess = highest_valued_word

        guesses.append(guess)

        result = make_a_guess(guess, answer, word_list)
        solved = result[0]
        word_list = result[1]
    
    return guesses


def read_guesses_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            guesses = [int(line.strip()) for line in file]
            return guesses
    except (FileNotFoundError, ValueError):
        return []


def update_average_in_file(file_path, guesses):
    with open(file_path, "w") as file:
        for guess in guesses:
            file.write(str(guess) + "\n")


def prompt_user_choice():
    print("Choose an option:")
    print("1. Play 'n' times with random words")
    print("2. Let the program guess a word you provide")
    choice = input("Enter your choice (1 or 2): ")
    return choice


def play_n_times_with_random_words(word_list):
    n = int(input("Enter the number of times you want to play: "))
    average_guesses = None

    # Use tqdm to create a progress bar for the for loop
    for i in tqdm(range(n), desc="Playing games", unit="game"):
        answer = random.choice(word_list).replace("\n", "")
        guesses = len(main(answer, word_list))

        stored_guesses = read_guesses_from_file("average_guesses.txt")
        stored_guesses.append(guesses)

        average_guesses = sum(stored_guesses) / len(stored_guesses)
        update_average_in_file("average_guesses.txt", stored_guesses)

    print(f"Average Guesses: {average_guesses}")


def let_program_guess_word(word_list):
    n = int(input("Enter the number of times you want to play: "))
    for i in range(n):
        average_guesses = None
        word = False
        while word == False:
            answer = str(input("Word: ")).replace("\n", "")
            word = True if len(answer) == 5 else False
        if answer not in word_list:
            word_list.append(answer)
        guesses = main(answer, word_list)
        
        for guess in guesses:
            print(guess)

        print(f"Number of guesses: {len(guesses)}")


if __name__ == "__main__":
    file_path = "sanitized_words_1.txt"
    word_list = get_word_list(file_path)

    choice = prompt_user_choice()

    if choice == '1':
        if word_list:  # Check if there are any words in the list
            play_n_times_with_random_words(word_list)
        else:
            print("No words to play. The word list is empty.")
    elif choice == '2':
        let_program_guess_word(word_list)
    else:
        print("Invalid choice. Please choose '1' or '2'.")