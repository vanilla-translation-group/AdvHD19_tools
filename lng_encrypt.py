import io
import struct
import argparse

def lngEncrypt(inputStream: io.TextIOWrapper, outputStream: io.BufferedIOBase, key: int) -> None:
    data = []
    while line := inputStream.readline():
        data.append(bytes(map(lambda x: x ^ key, (line[:-1] + "\0").encode("utf-16le"))))
    outputStream.write(struct.pack("<I", len(data)))
    for d in data:
        outputStream.write(struct.pack("<H", len(d)))
    for d in data:
        outputStream.write(d)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))
    parser.add_argument("outfile", type=argparse.FileType("wb"))
    parser.add_argument("key", type=lambda x: int(x, 16) % 256)
    args = parser.parse_args()
    lngEncrypt(args.infile, args.outfile, args.key)
