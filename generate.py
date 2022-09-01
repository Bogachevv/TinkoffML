from model import Model
import typing
import numpy as np
import random


def generate(model: Model):
    prefix = random.choice(list(model.data.keys()))
    while True:
        if prefix not in model.data:
            break
        w = model.get_next(prefix)
        prefix = (prefix[1], w)
        yield w
