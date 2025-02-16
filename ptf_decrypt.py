import io
import struct
import argparse

def ptfDecrypt(inputStream: io.BufferedIOBase, outputStream: io.BufferedIOBase, key: int) -> None:
    size = struct.unpack("<I", inputStream.read(4))[0]
    content = inputStream.read()
    buffer = bytearray()
    dictionary = bytearray(0x1000)
    indexI = 0
    indexD = 1
    while True:
        bit = content[indexI]
        indexI += 1
        for _ in range(8):
            if bit & 1 == 0:
                offset = (content[indexI + 1] >> 4) + content[indexI] * 0x10
                indexI += 2
                if offset != 0:
                    for _ in range((content[indexI - 1] & 0xf) + 2):
                        dictionary[indexD] = dictionary[offset & 0xfff]
                        buffer.append(dictionary[indexD] ^ key)
                        indexD = (indexD + 1) & 0xfff
                        offset += 1
                    bit >>= 1
                    continue
                if len(buffer) == size:
                    outputStream.write(buffer)
                else:
                    raise RuntimeError(f"file size mismatch, expected {hex(size)}, got {hex(len(buffer))}")
                return
            dictionary[indexD] = content[indexI]
            buffer.append(dictionary[indexD] ^ key)
            indexD = (indexD + 1) & 0xfff
            indexI += 1
            bit >>= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("rb"))
    parser.add_argument("outfile", type=argparse.FileType("wb"))
    parser.add_argument("key", type=lambda x: int(x, 16) % 256)
    args = parser.parse_args()
    ptfDecrypt(args.infile, args.outfile, args.key)
