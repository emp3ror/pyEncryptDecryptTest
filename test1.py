import os, random, struct
from Crypto.Cipher import AES
import sys
import hashlib

print("trying")

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    iv = 16 * '\x00'
    print(iv)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            # outfile.write(iv)
            outfile.write(bytes(iv, 'UTF-8'))

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
                # outfile.write(bytes(encryptor.encrypt(chunk), 'UTF-8'))


def main():
    filename = sys.argv[-1]
    key = '0123456789abcdef'

    # password = 'kitty'
    # key = hashlib.sha256(password.encode('utf-8')).digest()
    # IV = 16 * '\x00'           # Initialization vector: discussed later
    # mode = AES.MODE_CBC
    # encryptor = AES.new(key, mode, IV=IV)

    # text = 'j' * 64 + 'i' * 128
    # ciphertext = encryptor.encrypt(text)
    encrypt_file(key, filename)
    print("done")


if __name__ == '__main__':
    main()
