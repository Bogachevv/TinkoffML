from model import Model, deserialize_model
import typing
import random
import argparse
import itertools


def generate(model: Model, prefix: typing.Tuple[str, str] | None = None):
    prefix = random.choice(list(model.data.keys())) if prefix is None else prefix
    while True:
        if prefix not in model.data:
            break
        w = model.get_next(prefix)
        prefix = (prefix[1], w)
        yield w

# TODO: user interface


def parse_args() -> typing.Tuple[str, typing.Tuple[str, str], int]:
    """
    Parse cmd args
    :return: (inp_dir: str, model: str)
    """
    parser = argparse.ArgumentParser()
    # TODO:
    #   Write help
    parser.add_argument('--model', help='model help here', dest="model", default="model.pic", type=str)
    parser.add_argument('--prefix', help='prefix help here', dest="prefix", nargs=2, default=None, type=str)
    parser.add_argument('--length', help='length help here', dest="length", default=10, type=int)
    args = parser.parse_args()
    print(f"{args=}")
    return args.model, tuple(args.prefix) if args is not None else None, args.length


def main():
    model_path, initial_prefix, seq_length = parse_args()
    print(f"{initial_prefix=}")
    m = deserialize_model(model_path)
    c = 0
    for word in itertools.islice(generate(m, initial_prefix), seq_length):
        print(word, end=" ")
        c += 1
    print()
    print(f"{c=}")


if __name__ == '__main__':
    main()
