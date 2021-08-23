# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:45:11 2021

@author: m45ad
"""


import rsa

def file_open(file):
    key_file = open(file, 'rb')
    key_data = key_file.read()
    key_file.close()
    return key_data

privkey = rsa.PrivateKey.load_pkcs1(file_open('privatekey.key'))

message = file_open('message.pdf')
hash_value = rsa.compute_hash(message, 'SHA-512')

signature = rsa.sign(message, privkey, 'SHA-512')
s = open('signature_file.txt', 'wb')
s.write(signature)

print(signature)
print(len(signature))
print(len(hash_value) * 8) #to verify size of hash/output