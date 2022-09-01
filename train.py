import os
import sys
import string
import numpy as np
import argparse
import typing
import model
from generate import generate

def parse_args() -> typing.Tuple[str, str]:
    """
    Parse cmd args
    :return: (inp_dir: str, model: str)
    """
    parser = argparse.ArgumentParser()
    # TODO:
    #   Write help
    parser.add_argument('--input-dir', help='inp help here', dest="inp_dir", default=None, type=str)
    parser.add_argument('--model', help='model help here', dest="model", default="model.pic", type=str)
    args = parser.parse_args()
    print(f"{args=}")
    print(f"{args.inp_dir=}")
    print(f"{args.model=}")
    return args.inp_dir, args.model


def get_files(path: str | None) -> str | None:
    if path is None:
        yield None
    else:
        yield from (file for file in os.listdir(path) if '.txt' in file)


def get_fd(path: str | None) -> typing.TextIO:
    return sys.stdin if path is None else open(path, "r", encoding="utf-8")


def main():
    inp_dir, model_path = parse_args()
    print()
    m = model.Model()
    with open("texts\\text3.txt", "r", encoding="utf-8") as f:
        m.train(f.readlines())
    prefix = ("Помню", "будучи")
    for w in generate(m):
        print(w, end=' ')


if __name__ == '__main__':
    main()
