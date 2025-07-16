import tkinter as tk
from tkinter import messagebox
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
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read().lower()
            tokens = re.findall(r'\b\w+\b', text)
            for i in range(len(tokens) - self.n):
                key = tuple(tokens[i:i + self.n - 1])
                self.model[key].append(tokens[i + self.n - 1])
        except FileNotFoundError:
            messagebox.showerror("Error", f"Corpus file '{filepath}' not found.")

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

# --- GUI Code ---
class PredictiveTextApp:
    def __init__(self, root):
        self.generator = PredictiveTextGenerator(n=2)
        self.generator.load_corpus("corpus.txt")

        root.title("Predictive Text Generator")
        root.geometry("400x300")

        self.label = tk.Label(root, text="Enter your text:")
        self.label.pack(pady=5)

        self.text_input = tk.Entry(root, width=50)
        self.text_input.pack(pady=5)

        self.predict_button = tk.Button(root, text="Predict Next Word", command=self.predict_word)
        self.predict_button.pack(pady=5)

        self.prediction_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.prediction_label.pack(pady=10)

        self.custom_label = tk.Label(root, text="Add a custom word:")
        self.custom_label.pack(pady=5)

        self.custom_input = tk.Entry(root, width=30)
        self.custom_input.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Word", command=self.add_word)
        self.add_button.pack(pady=5)

    def predict_word(self):
        input_text = self.text_input.get()
        prediction = self.generator.predict_next_word(input_text)
        self.prediction_label.config(text=f"Prediction: {prediction}")

    def add_word(self):
        word = self.custom_input.get()
        if word:
            self.generator.add_custom_word(word)
            self.custom_input.delete(0, tk.END)
            messagebox.showinfo("Success", f"'{word}' added to custom dictionary.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictiveTextApp(root)
    root.mainloop()
