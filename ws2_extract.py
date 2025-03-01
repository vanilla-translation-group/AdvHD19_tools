import io
import argparse

def ws2Extract(inputStream: io.BufferedIOBase, textOutputStream: io.TextIOWrapper, nameOutputStream: io.TextIOWrapper) -> None:
    content = inputStream.read()
    length = len(content)
    index = 0
    names = set()
    while index < length:
        if index + 5 < length and content[index:index + 5] == b"char\x00":
            index += 5
            text = content[index:content.find(b"\0", index)].decode("shift_jis")
            index += len(text)
            textOutputStream.write(f"{text}\n")
            continue
        elif index + 2 < length and content[index:index + 2] == b"\x15%":
            index += 1
            name = content[index:content.find(b"\0", index)].decode("shift_jis")
            index += len(name)
            names.add(name)
            continue
        index += 1
    nameOutputStream.seek(0, 0)
    while (name := nameOutputStream.readline()) and (name := name.split()[0]):
        names.discard(name)
    for name in names:
        nameOutputStream.write(f"{name}\t{name}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("rb"))
    parser.add_argument("textoutfile", type=argparse.FileType("w"))
    parser.add_argument("nameoutfile", type=argparse.FileType("a+", encoding="utf-16le"))
    args = parser.parse_args()
    ws2Extract(args.infile, args.textoutfile, args.nameoutfile)
