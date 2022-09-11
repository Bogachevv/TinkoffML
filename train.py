import argparse
import os
import typing

import model


def parse_args() -> typing.Tuple[str, str]:
    """
    Parse cmd args
    :return: (inp_dir: str, model: str)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', help='Path to folder with .txt files', dest="inp_dir", default=None, type=str)
    parser.add_argument('--model', help='Path to model dump', dest="model", default="model.pic", type=str)
    args = parser.parse_args()
    return args.inp_dir, args.model


def get_files(path: str):
    yield from (f"{path}\\{file}" for file in os.listdir(path) if '.txt' in file)


def get_lines(path: str | None = None):
    if path is None:
        line = input("Input text: ")
        while line:
            yield line
            line = input()
    else:
        for fp in get_files(path):
            with open(fp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            yield from lines


def main():
    inp_dir, model_path = parse_args()
    m = model.Model()
    m.fit(get_lines(inp_dir))
    model.serialize_model(m, model_path)


if __name__ == '__main__':
    main()
