# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 18:20:31 2021

@author: m45ad
"""


from tkinter import Frame, Label, Entry, StringVar, Button, Tk, messagebox, filedialog
import mysql.connector
import numpy as np
import math
import rsa
import hashlib
import pickle

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
        sql = "SELECT * FROM commons WHERE username = %s"
        csr.execute(sql, (str(self.username.get()),))
        self.user = csr.fetchone()
        if self.user == None:
            messagebox.showinfo("Message", "Login gagal, user tidak ditemukan.")
        elif self.user[2] == self.password.get():
            self.openAuth()
        else:
            messagebox.showinfo("Message", "Login gagal, username dan password tidak tepat.")
            
    def signup(self):
        sql = "SELECT * FROM commons WHERE username = %s"
        csr.execute(sql, (str(self.username.get()),))
        user = csr.fetchone()
        if user:
            messagebox.showinfo("Message", "Signup gagal, username sudah digunakan user lain.")
        else:
            sql = "INSERT INTO commons (username, password, name, tgl_lahir) VALUES (%s, %s, %s, %s)"
            csr.execute(sql, (str(self.username.get()), str(self.password.get()), str(self.nama.get()), str(self.tglLahir.get())))
            db.commit()
            sql = "SELECT * FROM commons WHERE username = %s"
            csr.execute(sql, (str(self.username.get()),))
            self.user = csr.fetchone()
            self.openAuth()
            
    def openSignup(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        lblNama = Label(self.mainFrame, text="Nama Lengkap")
        lblNama.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        self.nama = StringVar(value="")
        entNama = Entry(self.mainFrame, textvariable=self.nama)
        entNama.grid(row=0, column=1, padx=10, pady=5)
        lblTglLahir = Label(self.mainFrame, text="Tanggal Lahir")
        lblTglLahir.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        self.tglLahir = StringVar(value="")
        entTglLahir = Entry(self.mainFrame, textvariable=self.tglLahir)
        entTglLahir.grid(row=1, column=1, padx=10, pady=5)  
        lblUsername = Label(self.mainFrame, text="Username")
        lblUsername.grid(row=2, column=0, padx=10, pady=5, sticky="W")
        self.username = StringVar(value="")
        entUsername = Entry(self.mainFrame, textvariable=self.username)
        entUsername.grid(row=2, column=1, padx=10, pady=5)
        lblPassword = Label(self.mainFrame, text="Password")
        lblPassword.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        self.password = StringVar(value="")
        entPassword = Entry(self.mainFrame, textvariable=self.password, show="*")
        entPassword.grid(row=3, column=1, padx=10, pady=5)
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
            
    def openAuth(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        btnBrowse = Button(self.mainFrame, text="Browse", command=self.browse)
        btnBrowse.grid(row=0, column=0, pady=10, padx=10)
        self.lblFilename = Label(self.mainFrame, text="")
        self.lblFilename.grid(row=0, column=1, pady=10, sticky="W", columnspan=4)
        lblPubKey = Label(self.mainFrame, text="Public Key")
        lblPubKey.grid(row=1, column=0, padx=5, pady=10)
        self.publicKey = StringVar(value="")
        entPubKey = Entry(self.mainFrame, textvariable=self.publicKey, show="*")
        entPubKey.grid(row=1, column=1)
        lblPubKey2 = Label(self.mainFrame, text="Public Key2")
        lblPubKey2.grid(row=2, column=0, padx=5, pady=10)
        self.publicKey2 = StringVar(value="")
        entPubKey2 = Entry(self.mainFrame, textvariable=self.publicKey2, show="*")
        entPubKey2.grid(row=2, column=1)
        btnDecrypt = Button(self.mainFrame, text="Decrypt", command=self.decrypt)
        btnDecrypt.grid(row=3, column=0, columnspan=2)
        
    def browse(self):
        self.path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf")], initialdir="fileupload/")
        if len(self.path) > 0:
            self.fname = self.path.split('/')[-1].split('.pdf')[0]
            self.lblFilename.config(text=self.fname)
            sql = "SELECT * FROM files WHERE filename = %s"
            csr.execute(sql, (str(self.fname),))
            self.file = csr.fetchone()
            self.publicKey.set(self.file[5])
            self.publicKey2.set(self.file[6])
            
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
    
    def decrypt(self):
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