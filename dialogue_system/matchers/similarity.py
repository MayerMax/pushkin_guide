import string

from pymorphy2 import MorphAnalyzer
from pymorphy2.tokenizers import simple_word_tokenize


morph = MorphAnalyzer()


def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form


def is_matching(first, second, similarity_func: callable, normalize_tokens=True, threshold=0.75) -> bool:
    first_tokens = [normalize(token) if normalize_tokens else token
                    for token in simple_word_tokenize(first) if token not in string.punctuation]
    second_tokens = [normalize(token) if normalize_tokens else token
                     for token in simple_word_tokenize(second) if token not in string.punctuation]
    return similarity_func(''.join(first_tokens), ''.join(second_tokens)) > threshold
