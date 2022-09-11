import argparse
import itertools
import random
import typing

from model import Model, deserialize_model


def build_prefix(model: Model) -> tuple[str, str]:
    return random.choice(list(model.data.keys()))


def reformat_prefix(prefix: tuple[str, str], model: Model) -> tuple[str, str]:
    if prefix in model.data:
        return prefix
    new_prefix_list = [key for key in model.data.keys() if key[0] == prefix[-1]]
    if not new_prefix_list:
        return build_prefix(model)
    return random.choice(new_prefix_list)


def generate(model: Model, prefix: typing.Tuple[str, str] | None = None):
    if prefix is None:
        prefix = build_prefix(model)
        yield from prefix
    elif prefix not in model.data:
        yield from prefix[:-1]
        prefix = reformat_prefix(prefix, model)
        yield from prefix
    else:
        yield from prefix

    while True:
        if prefix not in model.data:
            break
        w = model.generate(prefix)
        prefix = (prefix[1], w)
        yield w


def parse_args() -> typing.Tuple[str, typing.Tuple[str, str], int]:
    """
    Parse cmd args
    :return: (model: str, prefix: Tuple[str, str], length: int)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='Path to model dump', dest="model", default="model.pic", type=str)
    parser.add_argument('--prefix', help='Use --prefix word1 word2', dest="prefix", nargs=2, default=None, type=str)
    parser.add_argument('--length', help='Output sequence length', dest="length", default=10, type=int)
    args = parser.parse_args()
    return args.model, tuple(args.prefix) if args.prefix is not None else None, args.length


def main():
    model_path, initial_prefix, seq_length = parse_args()
    m = deserialize_model(model_path)
    c = 0
    for word in itertools.islice(generate(m, initial_prefix), seq_length):
        print(word, end=" ")
        c += 1
    print()


if __name__ == '__main__':
    main()
