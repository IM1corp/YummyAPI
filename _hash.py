#!/usr/bin/python
import hashlib
import sys


def generate_blake2b_256_hash(file_path):
    # Create a new BLAKE2b hash object with a digest size of 32 bytes (256 bits)
    hasher = hashlib.blake2b(digest_size=32)

    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Read the file in chunks and update the hash object
        chunk_size = 4096  # 4 KB
        while chunk := f.read(chunk_size):
            hasher.update(chunk)

    # Get the hash digest in hexadecimal format
    hash_digest = hasher.hexdigest()
    return hash_digest


# Specify the path to the file
file_path = sys.argv[1]

# Generate and print the BLAKE2b-256 hash
blake2b_256_hash = generate_blake2b_256_hash(file_path)
print(blake2b_256_hash)
