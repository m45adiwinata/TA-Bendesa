# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 22:50:13 2021

@author: m45ad
"""


from tkinter import Frame, Label, Entry, StringVar, Button, Tk, messagebox, filedialog
import mysql.connector
import numpy as np
import math
import rsa
import hashlib
import pickle
from shutil import copyfile

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "ttdpdf"
)
csr = db.cursor(buffered=True)

root = Tk()
root.geometry("600x400")

class Main():
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self.komponen()
        
    #KOMPONEN UTAMA INTERFACE
    def komponen(self):
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        lblUsername = Label(self.mainFrame, text="Username")
        lblUsername.grid(row=0, column=0, sticky="E", padx=5)
        self.username = StringVar(value="")
        entUsername = Entry(self.mainFrame, textvariable=self.username)
        entUsername.grid(row=0, column=1, columnspan=2, pady=5)
        lblPassword = Label(self.mainFrame, text="Password")
        lblPassword.grid(row=1, column=0, sticky="E", padx=5)
        self.password = StringVar(value="")
        entPassword = Entry(self.mainFrame, textvariable=self.password, show="*")
        entPassword.grid(row=1, column=1, columnspan=2, pady=5)
        btnLogin = Button(self.mainFrame, text="Login", width="20", command=self.login)
        btnLogin.grid(row=2, column=0, padx=10, pady=5, columnspan=3)
        btnSignup = Button(self.mainFrame, text="Sign up", width="20", command=self.openSignup)
        btnSignup.grid(row=3, column=0, padx=10, pady=5, columnspan=3)
        
    def login(self):
        sql = "SELECT * FROM authors WHERE username = %s"
        csr.execute(sql, (str(self.username.get()),))
        self.user = csr.fetchone()
        if self.user == None:
            messagebox.showinfo("Message", "Login gagal, user tidak ditemukan.")
        elif self.user[2] == self.password.get():
            self.openTtd()
        else:
            messagebox.showinfo("Message", "Login gagal, username dan password tidak tepat.")
            
    def signup(self):
        sql = "SELECT * FROM authors WHERE username = %s"
        csr.execute(sql, (str(self.username.get()),))
        user = csr.fetchone()
        if user:
            messagebox.showinfo("Message", "Signup gagal, username sudah digunakan user lain.")
        else:
            sql = "INSERT INTO authors (username, password, longname, prime1, prime2) VALUES (%s, %s, %s, %s, %s)"
            csr.execute(sql, (str(self.username.get()), str(self.password.get()), str(self.nama.get()), str(self.prime1.get()), str(self.prime2.get())))
            db.commit()
            sql = "SELECT * FROM authors WHERE username = %s"
            csr.execute(sql, (str(self.username.get()),))
            self.user = csr.fetchone()
            self.openTtd()
            
    def openSignup(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        lblNama = Label(self.mainFrame, text="Nama Lengkap", width="20")
        lblNama.grid(row=0, column=0, padx=10, pady=5)
        self.nama = StringVar(value="")
        entNama = Entry(self.mainFrame, textvariable=self.nama)
        entNama.grid(row=0, column=1, padx=10, pady=5)
        lblUsername = Label(self.mainFrame, text="Username", width="20")
        lblUsername.grid(row=1, column=0, padx=10, pady=5)
        self.username = StringVar(value="")
        entUsername = Entry(self.mainFrame, textvariable=self.username)
        entUsername.grid(row=1, column=1, padx=10, pady=5)
        lblPassword = Label(self.mainFrame, text="Password", width="20")
        lblPassword.grid(row=2, column=0, padx=10, pady=5)
        self.password = StringVar(value="")
        entPassword = Entry(self.mainFrame, textvariable=self.password, show="*")
        entPassword.grid(row=2, column=1, padx=10, pady=5)
        primes = self.generate_primes()
        self.prime1 = StringVar(value=primes[0])
        entPrimNumb1 = Entry(self.mainFrame, textvariable=self.prime1, show="*")
        entPrimNumb1.grid(row=3, column=0, pady=5)
        self.prime2 = StringVar(value=primes[1])
        entPrimNumb2 = Entry(self.mainFrame, textvariable=self.prime2, show="*")
        entPrimNumb2.grid(row=3, column=1, pady=5)
        btnSignup = Button(self.mainFrame, text="Signup", width="20", command=self.signup)
        btnSignup.grid(row=4, column=0, columnspan=2, pady=5)
        btnLogin = Button(self.mainFrame, text="Login", command=self.openLogin, width="20")
        btnLogin.grid(row=5, column=0, columnspan=2, pady=5)
        
    def openLogin(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        lblUsername = Label(self.mainFrame, text="Username")
        lblUsername.grid(row=0, column=0, sticky="E", padx=5)
        self.username = StringVar(value="")
        entUsername = Entry(self.mainFrame, textvariable=self.username)
        entUsername.grid(row=0, column=1, columnspan=2, pady=5)
        lblPassword = Label(self.mainFrame, text="Password")
        lblPassword.grid(row=1, column=0, sticky="E", padx=5)
        self.password = StringVar(value="")
        entPassword = Entry(self.mainFrame, textvariable=self.password, show="*")
        entPassword.grid(row=1, column=1, columnspan=2, pady=5)
        btnLogin = Button(self.mainFrame, text="Login", width="20", command=self.login)
        btnLogin.grid(row=2, column=0, padx=10, pady=5, columnspan=3)
        btnSignup = Button(self.mainFrame, text="Sign up", width="20", command=self.openSignup)
        btnSignup.grid(row=3, column=0, padx=10, pady=5, columnspan=3)
            
    def openTtd(self):
        self.mainFrame.destroy()
        primes = [self.user[3], self.user[4]]
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        btnBrowse = Button(self.mainFrame, text="Browse", command=self.browse)
        btnBrowse.grid(row=0, column=0, pady=10, padx=10)
        self.lblFilename = Label(self.mainFrame, text="")
        self.lblFilename.grid(row=0, column=1, pady=10, sticky="W", columnspan=4)
        self.privateKey = StringVar(value=str(primes[0]))
        self.publicKey = StringVar(value=str(primes[1]))
        btnEncrypt = Button(self.mainFrame, text="Encrypt", command=self.encrypt)
        btnEncrypt.grid(row=3, column=0, columnspan=2)
        btnDecrypt = Button(self.mainFrame, text="Decrypt", command=self.decrypt)
        btnDecrypt.grid(row=3, column=2, columnspan=2)
        
        
    def browse(self):
        self.path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf")], initialdir="../")
        if len(self.path) > 0:
            self.fname = self.path.split('/')[-1].split('.pdf')[0]
            self.lblFilename.config(text=self.fname)
            
    def file_open(self, file):
        key_file = open(file, 'rb')
        key_data = key_file.read()
        key_file.close()
        return key_data
            
    def generate_primes(self):
        primes = []
        count = np.random.randint(low=10, high=99)
        while len(primes) < 2:
            isprime = True
            for x in range(2, int(math.sqrt(count) + 1)):
                if count % x == 0: 
                    isprime = False
                    break
            if isprime:
                if len(primes) > 0:
                    if primes[0] != count:
                        primes.append(count)
                else:
                    primes.append(count)
            count = np.random.randint(low=10, high=99)
        return primes
    
    #FUNGSI ENKRIPSI
    def encrypt(self):
        #if self.privateKey.get() != "" and self.publicKey != "":
        public, private = rsa.generate_keypair(int(self.user[4]), int(self.user[5]))   #GENERATE KEYPAIR
        message = self.file_open(self.path)                             #READ FILE PDF BELUM ENKRIPSI
        md5 = hashlib.md5(message)
        md5hash = md5.hexdigest()
        print(md5hash)
        encrypted_msg = rsa.encrypt(private, md5hash)
        owner_id = self.user[0]
        sql = "INSERT INTO files (filename, md5hash, privkey1, privkey2, pubkey1, pubkey2, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        csr.execute(sql, (str(self.fname), str(md5hash), str(private[0]), str(private[1]), str(public[0]), str(public[1]), str(owner_id)))
        db.commit()
        file = open("hashdata/"+self.fname+".obj", "wb")                     #SIMPAN FILE HASH
        pickle.dump(encrypted_msg, file)
        copyfile(self.path, 'fileupload/'+self.fname+'.pdf')
        messagebox.showinfo("Message", "Authorization Success.")   #MESSAGE SUCCESS
    
    #FUNGSI DEKRIPSI    
    def decrypt(self):
        print(self.path)
        sql = "SELECT * FROM files WHERE filename = %s"
        csr.execute(sql, (str(self.fname),))
        self.file = csr.fetchone()
        message = self.file_open(self.path)                             #READ FILE PDF BELUM ENKRIPSI
        md5 = hashlib.md5(message)
        if self.file:
            public = (int(self.file[5]), int(self.file[6]))
            clip = pickle.load(open("hashdata/"+self.fname+".obj", "rb"))        #READ FILE DATA HASH
            decrypted_msg = rsa.decrypt(public, clip)
            if md5.hexdigest() == decrypted_msg:
                messagebox.showinfo("Message", "Authorization Success.")   #MESSAGE SUCCESS
            else:
                messagebox.showinfo("Message", "Authorization Failed, file content doesn't match.")   #MESSAGE SUCCESS
        else:
            messagebox.showinfo("Message", "Authorization Failed, file not found in database.")   #MESSAGE SUCCESS
        
Main(root, "TTD Digital PDF 1.0")
root.mainloop()
csr.close()
db.close()