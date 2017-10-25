import random
from messages.generators.generator import Generator


class Markov(Generator):
    def __init__(self, text=None, filename=None):
        self.cache = {}
        self.words = []
        if filename:
            self.words.append(self.file_to_words(filename))
        if text:
            self.words += text.split()

    def append_words(self, text):
        self.words += text.split()

    def file_to_words(self, filename):
        with open(filename, 'r') as f:
            f.seek(0)
            data = f.read()
        words = data.split()
        return words

    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def analyze_text(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate(self, size=None):
        if not size:
            size = random.randint(0, 50)
        seed = random.randint(0, len(self.words) - 3)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)
