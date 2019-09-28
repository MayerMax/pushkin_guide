import string

from pymorphy2 import MorphAnalyzer
from pymorphy2.tokenizers import simple_word_tokenize


morph = MorphAnalyzer()


def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form


def tokenize(line):
    return [token for token in simple_word_tokenize(line) if token not in string.punctuation]


def is_matching(first, second, similarity_func: callable, normalize_tokens=True, threshold=0.75) -> bool:
    first_tokens = [normalize(token) if normalize_tokens else token
                    for token in tokenize(first)]
    second_tokens = [normalize(token) if normalize_tokens else token
                     for token in tokenize(second)]
    return similarity_func(''.join(first_tokens), ''.join(second_tokens)) > threshold
