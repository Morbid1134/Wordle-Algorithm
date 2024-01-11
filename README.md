# Wordle Algorithm

This Python script implements a simple word guessing algorithm where the program tries to guess the word based on world rules and user feedback. The script is designed for study purposes and serves as a beginner to intermediate level Python project. Feel free to explore the code, understand its structure, and use it as a learning resource.

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Morbid1134/Wordle-Algorithm.git
   cd Wordle-Algorithm
   ```

2. **Run the Script:**
   ```bash
   python wordle_solver.py
   ```

3. **Follow the Instructions:**
   - The program will read a list of words from the file specified in `sanitized_words_1.txt`.
   - It will make educated guesses based on letter frequencies and user feedback.
   - Provide feedback using the pattern 'G' for matched letter, 'Y' for match and incorrectly placed letter, and 'N' for any letter not in the word.
   - Repeat the process until the program guesses the word or runs out of attempts.

4. **Contribute and Learn:**
   - Experiment with the code, make modifications, and observe the effects.
   - Understand how the program calculates letter frequencies and word values.
   - Explore the filtering mechanism based on user feedback.
   - Consider adding new features or improving existing ones. There is a method to add which will make it more accurate; can you find it?

## Functions

### `read_word_list(file_path)`
Reads a list of words from the given file and returns them as a list.

### `calculate_letter_frequency(word_list)`
Calculates the frequency of each letter in the given word list.

### `calculate_word_value(word_list, letter_frequency)`
Calculates the value of each word in the given list based on the letter frequencies.

### `find_highest_valued_word(word_list_values)`
Finds and returns the word with the highest value from the given word-value dictionary.

### `filter_words(pattern, word_list, guessed_word)`
Filters the word list based on the given pattern and guessed word.

### `main()`
The main function orchestrating the word guessing game. It initializes the game, makes guesses, and interacts with the user.
