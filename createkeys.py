# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:15:15 2021

@author: m45ad
"""


import rsa

(pubkey, privkey) = rsa.newkeys(2048)
with open('publickey.key', 'wb') as key_file:
    key_file.write(pubkey.save_pkcs1('PEM'))
    
with open('privatekey.key', 'wb') as key_file:
    key_file.write(privkey.save_pkcs1('PEM'))