import itertools
import pickle
import string
import typing
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np


def del_punctuation(s: str) -> str:
    punctuation = string.punctuation + "«»–…"
    return s.translate(str.maketrans({key: None for key in punctuation}))


def get_words(line: str) -> list[str]:
    line = del_punctuation(line)
    return line.strip().lower().split()


def calc_probs(ls: list[str]) -> np.ndarray:
    """
    :return: np.array([...,[elm_i, p_i],...])
    """
    unique_elms = set(ls)
    return np.array([[elm, ls.count(elm)/len(ls)] for elm in unique_elms])


@dataclass(init=True, slots=True)
class Model:
    data: defaultdict = field(default_factory=lambda: defaultdict(list))

    def fit(self, lines: typing.Iterable):
        words_gen = itertools.chain(*(get_words(line) for line in lines))
        prefix = (next(words_gen), next(words_gen))
        for word in words_gen:
            self.data[prefix].append(word)
            prefix = (prefix[1], word)

        for key in self.data:
            self.data[key] = calc_probs(self.data[key])

    def generate(self, prefix: typing.Tuple[str, str]) -> str:
        prefix = tuple(s.lower() for s in prefix)
        if prefix not in self.data:
            raise RuntimeError(f"Prefix not found\n{self.data.keys()=}\n{prefix=}")
        return np.random.choice(self.data[prefix][:, 0], 1, p=[float(p) for p in self.data[prefix][:, 1]])[0]


def serialize_model(m: Model, path: str):
    with open(path, "wb") as f:
        pickle.dump(m, file=f)


def deserialize_model(path: str) -> Model:
    with open(path, "rb") as f:
        return pickle.load(file=f)
