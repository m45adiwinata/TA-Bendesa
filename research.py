# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 20:06:31 2021

@author: m45ad
"""


import rsa
import hashlib

def file_open(file):
    key_file = open(file, 'rb')
    key_data = key_file.read()
    key_file.close()
    return key_data



p = 17
q = 71
public, private = rsa.generate_keypair(p, q)

message = file_open('message1.pdf')
md5 = hashlib.md5(message)
encrypted_msg = rsa.encrypt(private, md5.hexdigest())

print("Your encrypted message is: ")
print(''.join(map(lambda x: str(x), encrypted_msg)))
enc = ''.join(map(lambda x: str(x), encrypted_msg))

print("Decrypting message with public key ", public ," . . .")
print("Your message is:")
print(rsa.decrypt(public, encrypted_msg))
dec = rsa.decrypt(public, encrypted_msg)

print(enc[:12])
print(dec[:12])
temp= 0
for i in range(12):
    temp += (ord(enc[i]) - ord(dec[i]))

