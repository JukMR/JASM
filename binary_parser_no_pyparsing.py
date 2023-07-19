import re


def load_binary():
    with open('ls_short.s', 'r', encoding='utf-8') as f:
        binary = f.read()

    binary = binary.replace('\t', '')
    binary = binary.replace('\n', '|')
    binary = re.sub(r'#[^|]+', "", binary)

    return binary


def main():
    loaded_binary = load_binary()
    print(loaded_binary)


if __name__ == "__main__":
    main()
