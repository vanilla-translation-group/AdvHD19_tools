import tkinter as tk
from tkinter import font, messagebox, filedialog

from lng_encrypt import lngEncrypt
from lng_decrypt import lngDecrypt
from ws2_extract import ws2Extract
from ptf_decrypt import ptfDecrypt
from lua_patch import luaPatch

root = tk.Tk()
root.title("AdvHD 1.9 Tools GUI")
root.geometry("720x405")
root.resizable(False, False)

font.nametofont("TkDefaultFont").configure(size=18)

def getFont(*config):
    return ("TkDefaultFont", ) + config

button = tk.Button(root, text="Run", height=2, width=2, font=getFont(14))

def doAction(function, *args):
    try:
        function(*args)
    except Exception as e:
        messagebox.showerror(message=f"Operation failed: {e}")
    else:
        messagebox.showinfo(message="Operation successful")

def selectFile(var):
    var.set(filedialog.askopenfilename())

def validHex(string, char):
    if char:
        char = ord(char)
    else:
        char = 0
    return len(string) < 3 and (48 <= char <= 57 or 65 <= char <= 70 or 97 <= char <= 102)

vcmd = root.register(validHex)

components = []

def lngEncryptComponents():
    infile = tk.StringVar()
    outfile = tk.StringVar()
    key = tk.StringVar()

    def run():
        def _run(inputFile, outputFile, key):
            with open(inputFile, "r") as inputStream, open(outputFile, "wb") as outputStream:
                lngEncrypt(inputStream, outputStream, int(key, 16))
        doAction(_run, infile.get(), outfile.get(), key.get())

    components.append(tk.Frame(root))
    components.append(tk.Frame(root))
    components.append(tk.Frame(root))

    components.append(tk.Label(root, text="Input file (.txt):"))
    components.append(tk.Entry(components[0], textvariable=infile))
    components.append(tk.Button(components[0], text="...", command=lambda: selectFile(infile)))

    components.append(tk.Label(root, text="Output file (.lng):"))
    components.append(tk.Entry(components[1], textvariable=outfile))
    components.append(tk.Button(components[1], text="...", command=lambda: selectFile(outfile)))

    components.append(tk.Label(components[2], text="Key:"))
    components.append(tk.Entry(components[2], textvariable=key, width=2, validate="key", validatecommand=(vcmd, "%P", "%S")))

    components[3].pack(anchor="w")
    components[0].pack(fill="x")
    components[4].pack(side="left", fill="x", expand=True)
    components[5].pack(side="right")

    components[6].pack(anchor="w")
    components[1].pack(fill="x")
    components[7].pack(side="left", fill="x", expand=True)
    components[8].pack(side="right")

    components[2].pack(fill="x")
    components[9].pack(side="left")
    components[10].pack(side="left")

    button.configure(command=run)

def lngDecryptComponents():
    infile = tk.StringVar()
    outfile = tk.StringVar()

    def run():
        def _run(inputFile, outputFile):
            with open(inputFile, "rb") as inputStream, open(outputFile, "w") as outputStream:
                lngDecrypt(inputStream, outputStream)
        doAction(_run, infile.get(), outfile.get())

    components.append(tk.Frame(root))
    components.append(tk.Frame(root))

    components.append(tk.Label(root, text="Input file (.lng):"))
    components.append(tk.Entry(components[0], textvariable=infile))
    components.append(tk.Button(components[0], text="...", command=lambda: selectFile(infile)))

    components.append(tk.Label(root, text="Output file (.txt):"))
    components.append(tk.Entry(components[1], textvariable=outfile))
    components.append(tk.Button(components[1], text="...", command=lambda: selectFile(outfile)))

    components[2].pack(anchor="w")
    components[0].pack(fill="x")
    components[3].pack(side="left", fill="x", expand=True)
    components[4].pack(side="right")

    components[5].pack(anchor="w")
    components[1].pack(fill="x")
    components[6].pack(side="left", fill="x", expand=True)
    components[7].pack(side="right")

    button.configure(command=run)

def ws2ExtractComponents():
    infile = tk.StringVar()
    textoutfile = tk.StringVar()
    nameoutfile = tk.StringVar()

    def run():
        def _run(inputFile, textOutputFile, nameOutputFile):
            with open(inputFile, "rb") as inputStream, open(textOutputFile, "w") as textOutputStream, open(nameOutputFile, "w", encoding="utf-16le") as nameOutputStream:
                ws2Extract(inputStream, textOutputStream, nameOutputStream)
        doAction(_run, infile.get(), textoutfile.get(), nameoutfile.get())

    components.append(tk.Frame(root))
    components.append(tk.Frame(root))
    components.append(tk.Frame(root))

    components.append(tk.Label(root, text="Input file (.ws2):"))
    components.append(tk.Entry(components[0], textvariable=infile))
    components.append(tk.Button(components[0], text="...", command=lambda: selectFile(infile)))

    components.append(tk.Label(root, text="Output file (.txt):"))
    components.append(tk.Entry(components[1], textvariable=textoutfile))
    components.append(tk.Button(components[1], text="...", command=lambda: selectFile(textoutfile)))

    components.append(tk.Label(root, text="Output file (NameTable.txt):"))
    components.append(tk.Entry(components[2], textvariable=nameoutfile))
    components.append(tk.Button(components[2], text="...", command=lambda: selectFile(nameoutfile)))

    components[3].pack(anchor="w")
    components[0].pack(fill="x")
    components[4].pack(side="left", fill="x", expand=True)
    components[5].pack(side="right")

    components[6].pack(anchor="w")
    components[1].pack(fill="x")
    components[7].pack(side="left", fill="x", expand=True)
    components[8].pack(side="right")

    components[9].pack(anchor="w")
    components[2].pack(fill="x")
    components[10].pack(side="left", fill="x", expand=True)
    components[11].pack(side="right")

    button.configure(command=run)

def ptfDecryptComponents():
    infile = tk.StringVar()
    outfile = tk.StringVar()
    key = tk.StringVar()

    def run():
        def _run(inputFile, outputFile, key):
            with open(inputFile, "rb") as inputStream, open(outputFile, "wb") as outputStream:
                ptfDecrypt(inputStream, outputStream, int(key, 16))
        doAction(_run, infile.get(), outfile.get(), key.get())

    components.append(tk.Frame(root))
    components.append(tk.Frame(root))
    components.append(tk.Frame(root))

    components.append(tk.Label(root, text="Input file (.ptf):"))
    components.append(tk.Entry(components[0], textvariable=infile))
    components.append(tk.Button(components[0], text="...", command=lambda: selectFile(infile)))

    components.append(tk.Label(root, text="Output file (.ttf):"))
    components.append(tk.Entry(components[1], textvariable=outfile))
    components.append(tk.Button(components[1], text="...", command=lambda: selectFile(outfile)))

    components.append(tk.Label(components[2], text="Key:"))
    components.append(tk.Entry(components[2], textvariable=key, width=2, validate="key", validatecommand=(vcmd, "%P", "%S")))

    components[3].pack(anchor="w")
    components[0].pack(fill="x")
    components[4].pack(side="left", fill="x", expand=True)
    components[5].pack(side="right")

    components[6].pack(anchor="w")
    components[1].pack(fill="x")
    components[7].pack(side="left", fill="x", expand=True)
    components[8].pack(side="right")

    components[2].pack(fill="x")
    components[9].pack(side="left")
    components[10].pack(side="left")

    button.configure(command=run)

def luaPatchComponents():
    infile = tk.StringVar()
    outfile = tk.StringVar()

    def run():
        def _run(inputFile, outputFile):
            with open(inputFile, "rb") as inputStream, open(outputFile, "wb") as outputStream:
                luaPatch(inputStream, outputStream)
        doAction(_run, infile.get(), outfile.get())

    components.append(tk.Frame(root))
    components.append(tk.Frame(root))

    components.append(tk.Label(root, text="Input file (LegacyGame.lua):"))
    components.append(tk.Entry(components[0], textvariable=infile))
    components.append(tk.Button(components[0], text="...", command=lambda: selectFile(infile)))

    components.append(tk.Label(root, text="Output file (.lua):"))
    components.append(tk.Entry(components[1], textvariable=outfile))
    components.append(tk.Button(components[1], text="...", command=lambda: selectFile(outfile)))

    components[2].pack(anchor="w")
    components[0].pack(fill="x")
    components[3].pack(side="left", fill="x", expand=True)
    components[4].pack(side="right")

    components[5].pack(anchor="w")
    components[1].pack(fill="x")
    components[6].pack(side="left", fill="x", expand=True)
    components[7].pack(side="right")

    button.configure(command=run)

label = tk.Label(root, justify="center", font=getFont(16, "bold"))

def itemSelected(event):
    selection = event.widget.curselection()
    if selection:
        selection = selection[0]
    else:
        return
    label.configure(text=event.widget.get(selection))
    label.pack(side="top", fill="x", anchor="n")
    while components:
        components.pop().destroy()
    match selection:
        case 0:
            lngEncryptComponents()
        case 1:
            lngDecryptComponents()
        case 2:
            ws2ExtractComponents()
        case 3:
            ptfDecryptComponents()
        case 4:
            luaPatchComponents()
    button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

listbox = tk.Listbox(root, bd=0, font=getFont(15), width=15)
listbox.insert(0, "encrypt lng", "decrypt lng", "extract from ws2", "decrypt PTF", "patch lua")
listbox.bind("<<ListboxSelect>>", itemSelected)
listbox.pack(side="left", fill="y")

root.mainloop()
