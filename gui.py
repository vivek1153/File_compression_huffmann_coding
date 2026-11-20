
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from file_handler import compress_file, decompress_file


selected_file = None


def browse_file():

    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Text File",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if selected_file:
        file_label.config(
            text=os.path.basename(selected_file)
        )


def compress():

    if not selected_file:
        messagebox.showerror(
            "Error", "Please select a file first."
        )
        return

    output_file = selected_file + ".huff"

    try:

        result = compress_file(selected_file, output_file)

        original_label.config(
            text=f"Original Size: {result['original_size']} bytes"
        )

        compressed_label.config(
            text=f"Compressed Size: {result['compressed_size']} bytes"
        )

        saved_label.config(
            text=f"Space Saved: {result['space_saved']:.2f}%"
        )

        # Display frequency and codes
        table.delete("1.0", tk.END)

        table.insert(tk.END, "CHARACTER | FREQUENCY | HUFFMAN CODE\n")
        table.insert(tk.END, "-" * 48 + "\n")

        for char, freq in result["frequencies"].items():

            display_char = repr(char)

            code = result["codes"][char]

            table.insert(
                tk.END,
                f"{display_char:10} | {freq:9} | {code}\n"
            )

        status_label.config(
            text="Compression successful!",
            fg="#16A34A"
        )

    except Exception as error:

        messagebox.showerror("Error", str(error))


def decompress():

    compressed_file = filedialog.askopenfilename(
        title="Select Compressed File",
        filetypes=[("Huffman Files", "*.huff")]
    )

    if not compressed_file:
        return

    output_file = compressed_file + "_restored.txt"

    try:

        decompress_file(compressed_file, output_file)

        status_label.config(
            text="Decompression successful!",
            fg="#16A34A"
        )

        messagebox.showinfo(
            "Success",
            f"File restored successfully!\n\n{output_file}"
        )

    except Exception as error:

        messagebox.showerror("Error", str(error))


# Main application window

root = tk.Tk()

root.title("Huffman File Compression System")
root.geometry("750x650")
root.configure(bg="#172554")


# Heading

heading = tk.Label(
    root,
    text="HUFFMAN FILE COMPRESSION SYSTEM",
    font=("Arial", 19, "bold"),
    bg="#172554",
    fg="white"
)

heading.pack(pady=20)


# Browse button

browse_button = tk.Button(
    root,
    text="Browse Text File",
    command=browse_file,
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=22
)

browse_button.pack(pady=8)


file_label = tk.Label(
    root,
    text="No file selected",
    bg="#172554",
    fg="white"
)

file_label.pack(pady=5)


# Compress button

compress_button = tk.Button(
    root,
    text="COMPRESS FILE",
    command=compress,
    font=("Arial", 11, "bold"),
    bg="#16A34A",
    fg="white",
    width=22
)

compress_button.pack(pady=10)


# Decompress button

decompress_button = tk.Button(
    root,
    text="DECOMPRESS FILE",
    command=decompress,
    font=("Arial", 11, "bold"),
    bg="#EA580C",
    fg="white",
    width=22
)

decompress_button.pack(pady=5)


# File statistics

original_label = tk.Label(
    root,
    text="Original Size: --",
    bg="#172554",
    fg="white",
    font=("Arial", 11)
)

original_label.pack(pady=8)


compressed_label = tk.Label(
    root,
    text="Compressed Size: --",
    bg="#172554",
    fg="white",
    font=("Arial", 11)
)

compressed_label.pack(pady=5)


saved_label = tk.Label(
    root,
    text="Space Saved: --",
    bg="#172554",
    fg="#4ADE80",
    font=("Arial", 12, "bold")
)

saved_label.pack(pady=8)


# Character frequency and code table

table_heading = tk.Label(
    root,
    text="CHARACTER FREQUENCY AND HUFFMAN CODES",
    bg="#172554",
    fg="white",
    font=("Arial", 11, "bold")
)

table_heading.pack(pady=8)


table = tk.Text(
    root,
    height=12,
    width=75,
    font=("Consolas", 10)
)

table.pack(padx=15, pady=5)


# Status

status_label = tk.Label(
    root,
    text="Ready",
    bg="#172554",
    fg="white",
    font=("Arial", 11, "bold")
)

status_label.pack(pady=10)


root.mainloop()
