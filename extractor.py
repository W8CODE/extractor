import time
from tqdm import tqdm
import subprocess

import os
import hashlib
from Crypto.Cipher import AES
import os
import hashlib
from Crypto.Cipher import AES

# The path to the text file
file_path = "saved.txt"

# The password used to encrypt the file
password = "YOUR_PASSWORD"

#hash the password
key = hashlib.sha256(password.encode()).digest()[:16]

# The initialization vector used for encryption
iv = os.urandom(16)

# Create a new AES cipher
cipher = AES.new(key, AES.MODE_CBC, iv)

# getting the wifi passwords
txt = ""

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in tqdm(profiles):
    time.sleep(1)
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            txt += "{:<30}|  {:<}\n".format(i, results[0])
        except IndexError:
            txt += "{:<30}|  {:<}\n".format(i, "")
    except subprocess.CalledProcessError:
        txt += "{:<30}|  {:<}\n".format(i, "ENCODING ERROR")

# save passwords to a text file
with open('./saved.txt', 'w') as f:
    f.write(txt)


# Read the contents of the text file
with open(file_path, 'r') as file:
    plaintext = file.read()

# convert plaintext to bytes
plaintext = plaintext.encode("utf-8")

# Pad the plaintext to a multiple of 16 bytes
pad_length = 16 - (len(plaintext) % 16)
padding = bytes([pad_length]) * pad_length
plaintext += padding

# Encrypt the plaintext
ciphertext = cipher.encrypt(plaintext)

# Write the encrypted ciphertext to a new file
with open(file_path, 'wb') as file:
    file.write(iv + ciphertext)
