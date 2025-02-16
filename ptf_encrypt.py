import io
import struct
import argparse

def ptfEncrypt(inputStream: io.BufferedIOBase, outputStream: io.BufferedIOBase, key: int) -> None:
    buffer = bytearray()
    size = 0
    # TODO: compress data
    while True:
        binary = bytes(map(lambda x: x ^ key, inputStream.read(8)))
        length = len(binary)
        size += length
        if length == 8:
            buffer.append(0xff)
            buffer.extend(binary)
        else:
            buffer.append((1 << length) - 1)
            buffer.extend(binary)
            buffer.extend(b"\0\0")
            break
    outputStream.write(struct.pack("<I", size))
    outputStream.write(buffer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("rb"))
    parser.add_argument("outfile", type=argparse.FileType("wb"))
    parser.add_argument("key", type=lambda x: int(x, 16) % 256)
    args = parser.parse_args()
    ptfEncrypt(args.infile, args.outfile, args.key)
