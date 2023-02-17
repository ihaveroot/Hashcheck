# Hashcheck.py
#
#   This program will get the hash of a specified file
#    and compares it to the hash stored in the clipboard.
#    This uses the most common file hashing algorithms when
#    verifying files.
#
#   This program assumes you've copied the hash of a file
#    before running.
#
#   If you'd like to add alternative hashing algorithms
#    you can do so by adding the library and use the template
#    in the `compute_file_hash` function.
#
#   If you have added a new hashing algorithm in the 
#    `compute_file_hash` function you must add it in order
#    in the `hash_types` array in the `assign` function.
#    I'm sure you can figure it out. If you're calculating
#    the `foobar` hash before the `blake2b` hash in the
#    `compute_file_hash` function then the `foobar` string 
#    must come before the `blake2b` string in the assign function.
#
#   If the `foobar` hash you're adding is a different length.
#    you must modify the mapping variable in the
#    `display_confidence_hashes` pertaining to the position
#    of the `foobar` hash in the `list` variable in `assign`.
#
#   The last point in the program is the check between the
#    generated hash as well as the hash stored in your
#    clipboard. You will need to add the check if you had 
#    added a library into this program.
#
#
import re
import os
import sys
import zlib
import tqdm
import hashlib
import pyperclip
from termcolor import colored
from colorama import just_fix_windows_console



def banner():
    print(colored("\n\t    __  __           __         __              __  \n", "magenta") +
          colored("\t   / / / /_created__/ /_  _by__/ /_  ihaveroot_/ /__\n", "magenta") +
          colored("\t  / /_/ / __ `/ ___/ __ \/ ___/ __ \/ _ \/ ___/ //_/\n", "magenta") +
          colored("\t / __  / /_/ (__  ) / / / /__/ / / /  __/ /__/ ,<   \n", "cyan") +
          colored("\t/_/ /_/\__,_/____/_/ /_/\___/_/ /_/\___/\___/_/|_|  \n", "cyan") +
          "{:>55}\n".format("ver 1.0"),
          "\tSupported hashes: MD5, SHA-1, SHA256, SHA512, BLAKE2s, BLAKE2b\n\n")


# Function to compute the hash of a file
def compute_file_hash(file_name, hash_type):
    with open(file_name, 'rb') as file:
        if hash_type == 'MD5':
            hash_func = hashlib.md5()
        elif hash_type == 'SHA-1':
            hash_func = hashlib.sha1()
        elif hash_type == 'SHA256':
            hash_func = hashlib.sha256()
        elif hash_type == 'SHA512':
            hash_func = hashlib.sha512()
        elif hash_type == 'BLAKE2s':
            hash_func = hashlib.blake2s()
        #elif hash_type == 'foobar':
        #    hash_func = library.hashing_algorithm()
        elif hash_type == 'BLAKE2b':
            hash_func = hashlib.blake2b()
        else:
            # Check speeling of hash_type being called
            raise ValueError(f"Unsupported hash type: {hash_type}")
        buffer_size = 65536
        buffer = file.read(buffer_size)
        # tqdm progress bar, Flair
        pbar = tqdm.tqdm(total = round(os.path.getsize(file_name) / buffer_size) + 1, desc = f"Calculating {hash_type.upper()} hash", leave = False, ncols=100)
        while len(buffer) > 0:
            hash_func.update(buffer)
            buffer = file.read(buffer_size)
            pbar.update(1)
        return hash_func.hexdigest()


# Function to compute the CRC32 checksum
def compute_crc32_checksum(file_name):
    # Open the file in binary mode
    with open(file_name, 'rb') as f:
        # Read the contents of the file
        data = f.read()
        zlib.crc32(data)
        # Calculate the CRC32 checksum of the file's contents
        crc = zlib.crc32(data)
        # Return the CRC32 checksum
        return crc


# Compare Strings 
#  Compares both string hashes and checks 
#   whether both characters are the same. If 
#   they are then output it in green, if not 
#   then output it in red
def compare_strings(clipboard_hash, hash_string):
    # Print the hash from the clipboard
    print("{:>5} Hash from clipboard: ".format(""), end = "")

    # Compare each character from the clipboard_hash
    #  and the hash in the list. If it matches,
    #  color it green, if not then red
    for y, w in zip(clipboard_hash, hash_string):
        if y == w:
            print(colored(y, 'green'), end = "")
        else:
            print(colored(y, 'red'), end = "")
    print("\n")


# Confidence Level
#  Compares both string hashes and checks
#   whether both characters are the same. If
#   they are then increase confidence level
def confidence_level(clipboard_hash, list):
    confidence = 0
    for x, w in zip(clipboard_hash, list):
        if x == w:
            confidence += 1
    return round(confidence / len(clipboard_hash) * 100)


# Hash Confidence
#  Output the hash that has the most character similarities
#  Just some fun flair
def display_confidence_hashes(clipboard_hash, list):
    # Map the lengths of clipboard_hash to the corresponding elements in list and their confidence levels
    hash_length_map = {
        128: [list[3][1], list[5][1]],
         64: [list[2][1], list[4][1]],
         40: [list[1][1], list[1][1]],
         32: [list[0][1], list[0][1]],
        # foobar hash length of 16
        # foobar hash is in the 5th
        #  position, and the hash is
        #  in the first array.
        #16: [list[5][1], list[5][1]]
    }

    # Get the element in list and confidence level for the length of clipboard_hash
    hash_string, hash_string2 = hash_length_map.get(len(clipboard_hash), [None, None])

    # Break out from display if there is no hash, or value in clipboard is invalid
    if hash_string is None:
        print(colored('Warning', 'yellow') + ": The value in the clipboard is not a hash that this program identifies. Check your clipboard\n"
                "\tSupported hashes: MD5, SHA-1, SHA256, SHA512, BLAKE2s, BLAKE2b\n")
        return

    # Calculate the confidence level for the element in list
    confidence = confidence_level(clipboard_hash, hash_string)
    if confidence <= 50:
        confidence = confidence_level(clipboard_hash, hash_string2)
        hash_string = hash_string2

    # Find the index of the element in list that is the same as hash_string
    index = -1
    for a, b in enumerate(list):
        if b[1] == hash_string:
            index = a
            break

    # Print the confidence level and the relevant hash in list
    print(f"Confidence: {confidence}%")
    print("{0[0]:>12} hash of file: {0[1]}".format(list[index], list[index]))
    compare_strings(clipboard_hash, hash_string)


# Display match, if not then display that 
#  there is no match or if what user has 
#  in their clipboard isn't a hash type
#  display what they currently have copied
def display(nohash, list, clipboard_hash):
    match = False

    for name, hash in list:
        if hash == clipboard_hash:
            print("[", colored('O', 'green'), "] The hash matches the", colored(name, 'blue', 'on_white'), "hash of the file.\n")
            match = True
            return
    if not match:
        if nohash == 0:
            print("[", colored('X', 'red'), "] The hash does not match any of the calculated file hashes.\n")
        elif nohash == 1:
            print(colored('Info', 'yellow') + ": Current clipboard contents (128 chars shown): {:.128}\n".format(clipboard_hash))


# Assign the calculated hashes to
#  the corresponding hash_type in list
def assign(file_name):
    hash_types = ['MD5', 
                  'SHA-1', 
                  'SHA256', 
                  'SHA512', 
                  'BLAKE2s', 
                  #'FOOBAR',
                  'BLAKE2b']
    list = []

    for hash_type in hash_types:
        hash_value = compute_file_hash(file_name, hash_type)
        list.append([hash_type, hash_value])
        print(f"\t[{colored('O', 'green')}] {hash_type} hash calculation finished.")
    
    print("\t[" + colored('-', 'yellow') + f"] Calculating CRC32 checksum", end = "\r")
    crc32_hash   = compute_crc32_checksum(file_name)
    print("\t[" + colored('O', 'green') + f"] CRC32   checksum finished.{'':5s}")

    return list, crc32_hash


def main():
    # Throw error if no file is supplied
    if len(sys.argv) < 2:
        print("\nError: incorrect number of arguments. Usage: Hashcheck.py <file_name/path to file>")
        os.system('pause')
        return 1

    # Get the file to be checked
    file_name = sys.argv[1]

    # Use Colorama to make Termcolor work on Windows
    just_fix_windows_console()

    # Flair
    banner()

    try:
        # Get the hash from the clipboard
        clipboard_hash = pyperclip.paste().replace(" ", "")

        # If clipboard hash doesn't match the hash algorithm type
        #  continue anyway to generate hash types for the file
        if re.match(r"^[a-fA-F0-9]{32,64}$|^[a-fA-F0-9]{128}$", clipboard_hash) or re.match(r"^[0-9A-Fa-f]{8}$", clipboard_hash):
            nohash = 0
        else:
            nohash = 1

        # Assign calculated hash to hash type
        list, crc32_hash = assign(file_name)

        # print out file being checked and properties
        print("\n\n\tFile got: " + colored(os.path.basename(file_name), 'blue', 'on_white'), end = "\n\n")

        # Linebreak, Flair
        print("\t{:=^75s}\n\n".format(""))

        # Output and format for hash values
        for i in range(len(list)):
            print("{0[0]:>12} hash: {0[1]}".format(list[i], list[i]))

        # Print out CRC checksum
        print("\n{:>3}CRC32 checksum: {}\n".format("", colored(crc32_hash, 'yellow')))

        # Linebreak, Flair
        print("\t{:-^75s}\n".format(""))

        # Since BLAKE2b/SHA512, and BLAKE2s/SHA256
        #  have the same bit length, I like to compare the two
        #  hashes and look at if there is any differences.
        # Just some fun flair, it's fun to see.
        display_confidence_hashes(clipboard_hash, list)

        # display output of match/nomatch
        display(nohash, list, clipboard_hash)

        # Linebreak, Flair
        print("\t{:=^75s}\n\n\n".format(""))

        # Allow user to see results,
        #  if you're using this program on the command line then you can omit this
        os.system('pause')

    # Throw error if something fails
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
