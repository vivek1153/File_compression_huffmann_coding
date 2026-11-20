
import pickle
import os
from collections import Counter

from huffman import build_huffman_tree, generate_codes


def compress_file(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        raise ValueError("Cannot compress an empty file.")

    # Step 1: Calculate character frequencies
    frequencies = Counter(text)

    # Step 2: Build Huffman Tree
    root = build_huffman_tree(text)

    # Step 3: Generate Huffman codes
    codes = generate_codes(root)

    # Step 4: Encode original text
    encoded_text = "".join(codes[ch] for ch in text)

    # Step 5: Add padding to complete 8-bit bytes
    padding = (8 - len(encoded_text) % 8) % 8
    encoded_text += "0" * padding

    # Step 6: Convert binary string into bytes
    byte_array = bytearray()

    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        byte_array.append(int(byte, 2))

    # Step 7: Save codes, padding and compressed data
    compressed_data = {
        "codes": codes,
        "padding": padding,
        "data": bytes(byte_array)
    }

    with open(output_file, "wb") as file:
        pickle.dump(compressed_data, file)

    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)

    space_saved = (
        (original_size - compressed_size) / original_size
    ) * 100

    return {
        "frequencies": frequencies,
        "codes": codes,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "space_saved": space_saved
    }


def decompress_file(input_file, output_file):

    # Read compressed data
    with open(input_file, "rb") as file:
        compressed_data = pickle.load(file)

    codes = compressed_data["codes"]
    padding = compressed_data["padding"]
    data = compressed_data["data"]

    # Reverse the Huffman code dictionary
    reverse_codes = {
        code: char for char, code in codes.items()
    }

    # Convert bytes back into binary
    binary_data = "".join(
        format(byte, "08b") for byte in data
    )

    # Remove padding
    if padding:
        binary_data = binary_data[:-padding]

    # Decode binary data
    decoded_text = ""
    current_code = ""

    for bit in binary_data:

        current_code += bit

        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""

    if current_code:
        raise ValueError("Invalid compressed data.")

    # Restore original text
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(decoded_text)

    return output_file
