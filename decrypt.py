import os
import hashlib
from Crypto.Cipher import AES

# The path to the text file
file_path = "saved.txt"

# The password used to encrypt the file
password = "YOUR_PASSWORD"

#hash the password
key = hashlib.sha256(password.encode()).digest()[:16]

# Read the initialization vector and ciphertext from the file
with open(file_path, 'rb') as file:
    iv = file.read(16)
    ciphertext = file.read()

# Create a new AES cipher
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt the ciphertext
plaintext = cipher.decrypt(ciphertext)

# Remove the padding
pad_length = plaintext[-1]
plaintext = plaintext[:-pad_length]

# convert plaintext to utf-8
plaintext = plaintext.decode("utf-8")

# Write the plaintext to a new file
with open(file_path, 'w') as file:
    file.write(plaintext)
