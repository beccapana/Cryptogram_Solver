# Cryptogram Solver

This project provides a method to decrypt a substitution cipher using a genetic algorithm. The genetic algorithm aims to find the best possible decryption mapping based on letter frequencies, bigrams, and trigrams in the English language.

## Features

- **Frequency Analysis**: Calculate frequencies of letters, bigrams, and trigrams in the given text.
- **Genetic Algorithm**: Use a genetic algorithm to optimize the decryption key.
- **Simple Substitution Detection**: Detect simple substitutions based on letter frequency analysis.
- **Multiple Restarts**: Run the genetic algorithm multiple times to improve the chances of finding the optimal decryption.

## Prerequisites

- Python 3.x
- `nltk` library

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/beccapana/Cryptogram_Solver
   ```

2. Navigate to the project directory:

   ```
   cd Cryptogram_Solver
   ```

3. Install the required Python packages:

   ```
   pip install nltk
   ```

## Usage

1. Run the script:

   ```
   python substitution_cipher_decryption.py
   ```

2. Enter the encrypted text when prompted.

3. Enter the number of restarts for the genetic algorithm to run.

4. The script will display the possible decrypted text and several additional decryption variants.

## Functions

- `calculate_frequency(text, n=1)`: Calculates the frequency of n-grams in the text.
- `match_frequencies(cipher_freq, english_freq)`: Matches cipher frequencies to English frequencies and creates a mapping.
- `decrypt(text, mapping)`: Decrypts the text using the provided character mapping.
- `calculate_score(text)`: Scores the decrypted text based on bigrams, trigrams, and valid English words.
- `generate_mapping()`: Generates a random character mapping.
- `mutate(mapping)`: Mutates the mapping by swapping two random characters.
- `detect_simple_substitution(cipher_text, threshold=0.5)`: Detects if the text uses a simple substitution cipher based on letter frequencies.
- `genetic_algorithm(cipher_text, iterations=1000, population_size=100, elite_size=10)`: Applies a genetic algorithm to find the best mapping for decrypting the cipher text.
- `genetic_algorithm_with_restarts(cipher_text, restarts=3, iterations=1000, population_size=100, elite_size=10)`: Runs the genetic algorithm with multiple restarts to find the best mapping.

## Example

```
Enter the encrypted text: 
ZYLHSLHBR LSPJZ
Enter the number of restarts: 
5
```

The output will show the possible decrypted text and several additional decryption variants.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The `nltk` library for providing the English words corpus.
- Genetic algorithm principles for optimizing decryption keys.

Feel free to contribute to this project by creating issues or submitting pull requests.
