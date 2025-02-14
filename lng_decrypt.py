import io
import struct
import argparse

def lngDecrypt(inputStream: io.BufferedIOBase, outputStream: io.TextIOWrapper) -> None:
    inputStream.seek(-1, 2)
    key = inputStream.read(1)[0]
    inputStream.seek(0, 0)
    length = struct.unpack("<I", inputStream.read(4))[0]
    lengths = []
    for _ in range(length):
        lengths.append(struct.unpack("<H", inputStream.read(2))[0])
    for length in lengths:
        data = bytes(map(lambda x: x ^ key, inputStream.read(length)))
        if data[-2:] != b"\0\0":
            raise RuntimeError("invalid string")
        outputStream.write(data.decode("utf-16le")[:-1] + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("rb"))
    parser.add_argument("outfile", type=argparse.FileType("w"))
    args = parser.parse_args()
    lngDecrypt(args.infile, args.outfile)
