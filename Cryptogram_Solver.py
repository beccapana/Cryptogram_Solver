import random
import string
from collections import Counter
import concurrent.futures
import nltk

# Download English words if they are not already downloaded
nltk.download('words')
english_words = set(nltk.corpus.words.words())

# Typical frequencies of letters, bigrams, and trigrams in English
english_letter_freq = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31,
    'N': 6.95, 'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32,
    'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.30,
    'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49,
    'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.10,
    'Z': 0.07
}

english_bigrams = {
    'TH': 1.52, 'HE': 1.28, 'IN': 0.94, 'ER': 0.94, 'AN': 0.82,
    'RE': 0.68, 'ND': 0.63, 'AT': 0.59, 'ON': 0.57, 'NT': 0.56,
    'HA': 0.56, 'ES': 0.56, 'ST': 0.55, 'EN': 0.55, 'ED': 0.53,
    'TO': 0.52, 'IT': 0.50, 'OU': 0.50, 'EA': 0.47, 'HI': 0.46,
    'IS': 0.46, 'OR': 0.43, 'TI': 0.34, 'AS': 0.33, 'TE': 0.27,
    'ET': 0.19, 'NG': 0.18, 'OF': 0.16, 'AL': 0.09, 'DE': 0.09,
    'SE': 0.08, 'LE': 0.08, 'SA': 0.06, 'SI': 0.05, 'AR': 0.04
}

english_trigrams = {
    'THE': 1.81, 'AND': 0.73, 'ING': 0.72, 'ENT': 0.42, 'ION': 0.42,
    'HER': 0.36, 'FOR': 0.34, 'THA': 0.33, 'NTH': 0.33, 'INT': 0.32,
    'ERE': 0.31, 'TIO': 0.31, 'TER': 0.30, 'EST': 0.28, 'ERS': 0.28,
    'ATI': 0.26, 'HAT': 0.26, 'ATE': 0.25, 'ALL': 0.24, 'ETH': 0.22,
    'HES': 0.21, 'VER': 0.21, 'HIS': 0.20, 'OFT': 0.20, 'ITH': 0.20,
    'FTH': 0.18, 'STH': 0.18, 'OTH': 0.18, 'RES': 0.18, 'ONT': 0.17
}

def calculate_frequency(text, n=1):
    """Calculate the frequency of n-grams in the given text."""
    text = text.upper()
    ngrams = [text[i:i+n] for i in range(len(text)-n+1) if all(c in string.ascii_uppercase for c in text[i:i+n])]
    counter = Counter(ngrams)
    total = sum(counter.values())
    frequency = {ngram: count / total * 100 for ngram, count in counter.items()}
    return frequency

def match_frequencies(cipher_freq, english_freq):
    """Match cipher frequencies to English frequencies and create a mapping."""
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True)
    sorted_english_freq = sorted(english_freq.items(), key=lambda item: item[1], reverse=True)
    
    mapping = {}
    for i in range(min(len(sorted_cipher_freq), len(sorted_english_freq))):
        cipher_char, _ = sorted_cipher_freq[i]
        english_char, _ = sorted_english_freq[i]
        mapping[cipher_char] = english_char
    
    return mapping

def decrypt(text, mapping):
    """Decrypt the text using the provided character mapping."""
    decrypted_text = []
    for char in text:
        if char.upper() in mapping:
            new_char = mapping[char.upper()]
            if char.islower():
                new_char = new_char.lower()
            decrypted_text.append(new_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

def calculate_score(text):
    """Calculate the score of the decrypted text based on bigrams, trigrams, and valid words."""
    bigrams = calculate_frequency(text, n=2)
    trigrams = calculate_frequency(text, n=3)
    
    score = 0
    for bigram in bigrams:
        if bigram in english_bigrams:
            score += english_bigrams[bigram] * bigrams[bigram]
    for trigram in trigrams:
        if trigram in english_trigrams:
            score += english_trigrams[trigram] * trigrams[trigram]
    
    words = text.split()
    valid_words = [word for word in words if word.lower() in english_words]
    score += len(valid_words) * 10
    
    return score

def generate_mapping():
    """Generate a random character mapping."""
    letters = list(string.ascii_uppercase)
    random.shuffle(letters)
    return dict(zip(string.ascii_uppercase, letters))

def mutate(mapping):
    """Mutate the mapping by swapping two random characters."""
    keys = list(mapping.keys())
    a, b = random.sample(keys, 2)
    mapping[a], mapping[b] = mapping[b], mapping[a]

def detect_simple_substitution(cipher_text, threshold=0.5):
    """Detect if the text uses a simple substitution cipher based on letter frequencies."""
    letter_freq = calculate_frequency(cipher_text, n=1)
    sorted_cipher_freq = sorted(letter_freq.items(), key=lambda item: item[1], reverse=True)
    
    # Check if the frequencies match those of English letters
    if len(sorted_cipher_freq) < len(english_letter_freq):
        return None

    # Assume the most frequent letter in the cipher is the most frequent in English
    cipher_top = sorted_cipher_freq[0][0]
    english_top = sorted(english_letter_freq.items(), key=lambda item: item[1], reverse=True)[0][0]

    if sorted_cipher_freq[0][1] / sum(freq for _, freq in sorted_cipher_freq) > threshold:
        return {cipher_top: english_top}
    
    return None

def genetic_algorithm(cipher_text, iterations=1000, population_size=100, elite_size=10):
    """Apply a genetic algorithm to find the best mapping for decrypting the cipher text."""
    def evaluate_mapping(mapping):
        decrypted_text = decrypt(cipher_text, mapping)
        return calculate_score(decrypted_text), mapping
    
    population = [generate_mapping() for _ in range(population_size)]
    
    best_mapping = None
    best_score = float('-inf')
    
    for iteration in range(1, iterations + 1):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(evaluate_mapping, mapping) for mapping in population]
            scores_mappings = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        sorted_population = sorted(scores_mappings, key=lambda item: item[0], reverse=True)
        best_mapping = sorted_population[0][1]
        best_score = sorted_population[0][0]
        
        # Log current iteration and best result
        if iteration % 100 == 0 or iteration == iterations:
            print(f"Iteration {iteration}/{iterations}, current best score: {best_score}")
            print("Current best decrypted text:")
            print(decrypt(cipher_text, best_mapping))
        
        # Check for simple substitution
        simple_substitution = detect_simple_substitution(cipher_text)
        if simple_substitution:
            print("Simple substitution detected:")
            print(simple_substitution)
            best_mapping.update(simple_substitution)
        
        new_population = [mapping for score, mapping in sorted_population[:elite_size]]
        
        for _ in range(population_size - elite_size):
            parent_mapping = random.choice(new_population)
            new_mapping = parent_mapping.copy()
            mutate(new_mapping)
            new_population.append(new_mapping)
        
        population = new_population
    
    return best_mapping

def genetic_algorithm_with_restarts(cipher_text, restarts=3, iterations=1000, population_size=100, elite_size=10):
    """Run the genetic algorithm with multiple restarts to find the best mapping."""
    best_mapping = None
    best_score = float('-inf')
    
    for restart in range(1, restarts + 1):
        print(f"Restart {restart}/{restarts}...")
        current_mapping = genetic_algorithm(cipher_text, iterations, population_size, elite_size)
        decrypted_text = decrypt(cipher_text, current_mapping)
        current_score = calculate_score(decrypted_text)
        
        print(f"Best result in restart {restart}: {current_score}")
        print("Best decrypted text in this restart:")
        print(decrypted_text)
        
        if current_score > best_score:
            best_score = current_score
            best_mapping = current_mapping
    
    return best_mapping

def main():
    encrypted_text = input("Enter the encrypted text: ")

    # Ask the user for the number of additional restarts
    restarts = int(input("Enter the number of restarts: "))

    # Run the algorithm with the specified number of restarts
    best_mapping = genetic_algorithm_with_restarts(encrypted_text, restarts=restarts)
    
    decrypted_text = decrypt(encrypted_text, best_mapping)
    
    print("\nPossible decrypted text:")
    print(decrypted_text)

    print("\nAdditional decryption variants:")
    for i in range(1, 4):
        mutated_mapping = best_mapping.copy()
        for _ in range(3):  # Apply several mutations for stability
            mutate(mutated_mapping)
        alt_decryption = decrypt(encrypted_text, mutated_mapping)
        print(f"Variant {i}: {alt_decryption}")

if __name__ == "__main__":
    main()