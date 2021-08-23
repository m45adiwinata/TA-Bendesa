# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:50:56 2021

@author: m45ad
"""


import rsa

def file_open(file):
    key_file = open(file, 'rb')
    key_data = key_file.read()
    key_file.close()
    return key_data

pubkey = rsa.PublicKey.load_pkcs1(file_open('publickey.key'))

message = file_open('message.pdf')
signature = file_open('signature_file.txt')

try:
    rsa.verify(message, signature, pubkey)
    print("verified")
    
except:
    print("failed")