"""Generate page names consisting of three random words."""

from random_word import RandomWords

word_generator = RandomWords()

words = []
for _ in range(3):
    word = word_generator.get_random_word(
        hasDictionaryDef=True, minDictionaryCount=30
    ).capitalize()
    words.append(word)

print("-".join(words))
