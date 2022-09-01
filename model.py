import sys
import typing
import string
import numpy as np
from collections import defaultdict


def del_punctuation(s: str) -> str:
    return s.translate(str.maketrans({key: None for key in string.punctuation}))


def get_words(line: str) -> list[str]:
    line = del_punctuation(line)
    return [s for s in line.strip().lower().split()]


# TODO: change signature
def convert_list(ls: list[str]) -> np.ndarray:
    """
    :return: np.array([...,[elm_i, p_i],...])
    """
    unique_elms = set(ls)
    return np.array([[elm, ls.count(elm)/len(ls)] for elm in unique_elms])


def get_words_from_lines(lines: typing.Iterable):
    for line in lines:
        yield from get_words(line)


class Model:
    __slots__ = ['data']

    def __init__(self):
        self.data = defaultdict(list)

    def train(self, lines: typing.Iterable):
        words_gen = get_words_from_lines(lines)
        prefix = (next(words_gen), next(words_gen))
        for word in words_gen:
            if prefix not in self.data:
                self.data[prefix] = list()
            self.data[prefix].append(word)
            prefix = (prefix[1], word)

        for key in self.data:
            self.data[key] = convert_list(self.data[key])

    def get_next(self, prefix: typing.Tuple[str, str]) -> str:
        prefix = tuple(s.lower() for s in prefix)
        if prefix not in self.data:
            raise RuntimeError(f"Prefix not found\n{self.data.keys()=}\n{prefix=}")
        # print(f"DEBUG: {self.data[prefix][:, 0]=}\n{self.data[prefix][:, 1]=}")
        return np.random.choice(self.data[prefix][:, 0], 1, p=[float(p) for p in self.data[prefix][:, 1]])[0]
