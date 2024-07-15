import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser


def fix_slot_data(data):
    search_bytes = bytearray.fromhex("15000000D81812CE")
    replace_bytes = bytearray.fromhex("FFFFFFFF00000000")

    start_index = int("001A8D44", 16)
    end_index = int("001ACD44", 16)

    for i in range(start_index, end_index - len(search_bytes) + 1):
        if data[i : i + len(search_bytes)] == search_bytes:
            data[end_index:end_index] = replace_bytes
            del data[i : i + len(search_bytes)]
            break

    index = int("001ACE90", 16)
    data[index] &= 0b11111011

    return data


def modify_file(input_file_path, output_file_path, status_var):
    with open(input_file_path, "rb") as file:
        data = bytearray(file.read())

    data = fix_slot_data(data)

    with open(output_file_path, "wb") as file:
        file.write(data)


def open_file_dialog(status_var):
    input_file_path = filedialog.askopenfilename()
    with open(input_file_path, "rb") as file:
        data = bytearray(file.read())

    data = fix_slot_data(data)

    messagebox.showinfo("Processed!", "Please choose where to save fixed data.")

    output_file_path = filedialog.asksaveasfilename(
        defaultextension=".mhwslot", filetypes=[("MHW Slot Data", "*.mhwslot")]
    )
    with open(output_file_path, "wb") as file:
        file.write(data)

    messagebox.showinfo("Fixed file saved ", "Fixed file saved at: " + output_file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", help="source file", nargs="?")
    parser.add_argument("output_file_path", help="fix file", nargs="?")
    args = parser.parse_args()

    if args.input_file_path and args.output_file_path:
        modify_file(args.input_file_path, args.output_file_path)
    else:
        root = tk.Tk()
        root.title("MHW witcher side quest Fixer")

        label = tk.Label(
            root,
            text="This is a .mhwslot data fixing tool for fixing Witcher side quest missing.",
        )
        label.pack()

        button = tk.Button(
            root,
            text="Choose HMW Slot Data",
            command=lambda: open_file_dialog(status_var),
        )
        button.pack()

        link = tk.Label(root, text="GitHub", fg="blue", cursor="hand2")
        link.pack()
        link.bind(
            "<Button-1>",
            lambda e: webbrowser.open_new(
                "https://github.com/DeepTMods/mhw_witcher_fix"
            ),
        )

        status_var = tk.StringVar()
        status_var.set("v0.1.20240715-alpha, by DeepT. @ DeepTMods(DTM)")
        status_bar = tk.Label(
            root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        root.mainloop()


if __name__ == "__main__":
    main()
