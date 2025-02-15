import io
import struct
import argparse

def luaPatch(inputStream: io.BufferedIOBase, outputStream: io.BufferedIOBase) -> None:
    magic = inputStream.read(4)
    if magic != b"\x1BLua":
        raise RuntimeError("invalid lua bytecode")
    content = bytearray(inputStream.read())
    if content[46:50] != b"\x08\x40\x40\x80":
        raise RuntimeError("failed to apply patch, maybe the file is already patched")
    index = content.find(b"g_SetDefaultLangJP\x01\x01")
    if index == -1:
        raise RuntimeError("string missing")
    size = struct.unpack("<I", content[index - 6:index - 2])[0]
    count = 2
    index += 20
    while count < size:
        t = content[index]
        if t == 0x01:
            index += 1
            if content[index] == 0x00:
                count *= 4
                content[47] = (count & 15) << 4
                content[48] += count >> 4
                outputStream.write(magic)
                outputStream.write(content)
                return
        elif t == 0x00:
            pass
        elif t == 0x03 or t == 0x13:
            index += 8
        elif t == 0x04:
            index += content[index + 1]
        else:
            raise RuntimeError(f"unknown bytecode {hex(t)}, at index {hex(index + 4)}, No.{count}")
        index += 1
        count += 1
    raise RuntimeError("cannot find 'false' constant")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("rb"))
    parser.add_argument("outfile", type=argparse.FileType("wb"))
    args = parser.parse_args()
    luaPatch(args.infile, args.outfile)
