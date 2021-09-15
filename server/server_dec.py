import os
import random, string
import sys
import zipfile
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Signature import PKCS1_v1_5

# senders public key
# reciever private key

def sigVerification(f_name,key_pub,f_dec):
    hash_file = SHA256.new()
    print(f_dec)
    hash_file.update(open(f_dec, "rb").read())
    with open(key_pub, "r") as myfile:
        public_key = RSA.importKey(myfile.read())

    keyVerifier = PKCS1_v1_5.new(public_key)

    if keyVerifier.verify(hash_file,open(f_name.split('.')[0] + ".sig","rb").read()):
        print("the signature is authentic")
    else:
        print("failed")
def KeyReader(f_name,key_pri):
    with open(key_pri, "r") as myfile:
        private_Reciever_key = RSA.importKey(myfile.read())
    keyDeCipher = PKCS1_OAEP.new(private_Reciever_key)
    f = open(f_name.split('.')[0] + ".key","rb")
    iv = f.read(16)
    k = keyDeCipher.decrypt(f.read())
    return  iv,k

def decifer(f_name):
    print(f_name)
    if f_name == "fedavg_1.bin":
        key_pri = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/server.pem"
        key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/pub_client1_key.pem"
    else:
        key_pri = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/server.pem"
        key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/pub_client2_key.pem"
    iv,k = KeyReader(f_name,key_pri)
    key_dec = AES.new(k,AES.MODE_CFB,iv)

    bin = open (f_name.split('.')[0] + ".bin" ,"rb").read()
    f= open("fedavg_1.txt","wb")
    f.write(key_dec.decrypt(bin))
    f.close()
    f_dec = "fedavg_1.txt"
    sigVerification(f_name,key_pub,f_dec)
    
	






