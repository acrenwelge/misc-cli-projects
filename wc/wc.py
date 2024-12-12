from sys import argv


def wc(file):
    with open(file, "rb") as f:
        lines = f.readlines()
        words = sum(len(line.split()) for line in lines)
        chars = sum(len(line) for line in lines)
    return len(lines), words, chars


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: wc.py <file>")
    else:
        print(wc(argv[1]))
