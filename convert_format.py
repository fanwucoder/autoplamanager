import tkinter as tk
from tkinter import simpledialog

test = """(0x54d22e, "", 90, 397, 260, 421, 279)"""


def onBtClick():
    try:
        data = input.get()
        ret = convert_colors(data)

        output.delete(0, tk.END)
        output.insert(0, ret)
    except:
        output.delete(0, tk.END)
        output.insert(0, "error")


def convert_colors(data):
    data = data[1: -1].split(",")
    data = [x.strip() for x in data]
    ret = "%.02f,%s,%s,%s,%s,\"%s\",%s" % (
        int(data[2]) / 100.0, data[3], data[4], data[5], data[6], data[0], data[1])
    return ret

print(test)
print(convert_colors(test))
root = tk.Tk()
root.geometry("400x100")
input = tk.Entry(root)
input.pack()
output = tk.Entry(root)
output.pack()
bt = tk.Button(root, text="转换", command=onBtClick)

bt.pack()

root.mainloop()
