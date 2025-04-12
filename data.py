import random

texts = []

known_words = []
words = []

def get_texts():
    return texts

def get_random_text():
    return random.choice(texts)

def get_words_from_text(text):
    return text.split

def get_all_words():
    all_words = set()
    for text in texts:
        words = get_words_from_text(text)
        all_words.update(words)

def add_unknown_word(word):
    if word not in add_unknown_word:
        add_unknown_word.append(word)

def get_known_words():
    return known_words

def get_unknown_word(word):
    if word not in known_words:
        known_words.append(word)
        
def get_random_word():
    return random.choice(words)