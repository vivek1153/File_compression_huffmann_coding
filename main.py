
from file_handler import compress_file, decompress_file

print("================================")
print(" HUFFMAN FILE COMPRESSION SYSTEM")
print("================================")

while True:

    print("\n1. Compress File")
    print("2. Decompress File")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    try:

        if choice == "1":

            compress_file(
                "input.txt",
                "compressed.huff"
            )

        elif choice == "2":

            decompress_file(
                "compressed.huff",
                "decompressed.txt"
            )

        elif choice == "3":

            print("Thank you for using the system!")
            break

        else:

            print("Invalid choice! Try again.")

    except Exception as error:

        print("Error:", error)
