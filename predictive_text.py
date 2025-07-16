import random
import re
from collections import defaultdict

class PredictiveTextGenerator:
    def __init__(self, n=2):
        self.n = n
        self.model = defaultdict(list)
        self.custom_words = set()
        self.load_custom_words("custom_dict.txt")

    def load_corpus(self, filepath="corpus.txt"):
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read().lower()
        tokens = re.findall(r'\b\w+\b', text)
        for i in range(len(tokens) - self.n):
            key = tuple(tokens[i:i + self.n - 1])
            self.model[key].append(tokens[i + self.n - 1])

    def load_custom_words(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                self.custom_words = set(word.strip() for word in file.readlines())
        except FileNotFoundError:
            self.custom_words = set()

    def add_custom_word(self, word, filepath="custom_dict.txt"):
        word = word.lower().strip()
        if word not in self.custom_words:
            self.custom_words.add(word)
            with open(filepath, "a", encoding="utf-8") as file:
                file.write(word + "\n")

    def predict_next_word(self, prev_words):
        prev_words = prev_words.lower().split()
        if len(prev_words) < self.n - 1:
            return "Not enough context"
        key = tuple(prev_words[-(self.n - 1):])
        predictions = self.model.get(key, [])
        predictions += list(self.custom_words)
        return random.choice(predictions) if predictions else "No prediction"

# --- Example usage ---
if __name__ == "__main__":
    ptg = PredictiveTextGenerator(n=2)
    ptg.load_corpus("corpus.txt")

    while True:
        print("\n--- Predictive Text Generator ---")
        print("1. Predict next word")
        print("2. Add custom word")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            input_text = input("Enter your text: ")
            prediction = ptg.predict_next_word(input_text)
            print("Predicted next word:", prediction)

        elif choice == "2":
            new_word = input("Enter word to add: ")
            ptg.add_custom_word(new_word)
            print(f"'{new_word}' added to custom dictionary.")

        elif choice == "3":
            break
