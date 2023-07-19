import yaml
import argparse
from typing import Any


def read_yaml(file) -> Any:
    with open(file, 'r', encoding='utf-8') as f:
        loaded_yaml = yaml.load(stream=f.read(), Loader=yaml.Loader)
    return loaded_yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-yaml', required=True)
    args = parser.parse_args()

    loaded_yaml = read_yaml(args.input_yaml)

    print(loaded_yaml)


if __name__ == "__main__":
    main()
