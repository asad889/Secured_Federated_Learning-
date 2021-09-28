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
key_pri = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/server.pem"
class Decryption:
    def __init__(self,f_name):
        self.f_name = f_name

    def delete(self):
        os.remove(self.f_name.split('.')[0]+".sig")
        os.remove(self.f_name.split('.')[0]+".bin")
        os.remove(self.f_name.split('.')[0]+".key")
        os.remove(self.f_name.split('.')[0] + ".all")
        os.remove(self.f_name.split('.')[0] + ".tmp")
    def Keymanagement(self):
        if self.f_name == "fedavg_1.all":
            key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/pub_client1_key.pem"
        elif self.f_name == "fedavg_2.all":
            key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server/keys_management/pub_client2_key.pem"

        return key_pub

    def sigVerification(self,key_pub):
        hash_file = SHA256.new()

        hash_file.update(open(self.f_name.split('.')[0] + ".tmp", "rb").read())

        with open(key_pub, "r") as myfile:
            public_key = RSA.importKey(myfile.read())

        keyVerifier = PKCS1_v1_5.new(public_key)
        verify = keyVerifier.verify(hash_file,open(self.f_name.split('.')[0] + ".sig","rb").read())

        if keyVerifier.verify(hash_file,open(self.f_name.split('.')[0] + ".sig","rb").read()):
            print("the signature is authentic and the file can be used by server")

            return(verify)
        else:
            print("Signature authentication failed , it means  either file has been comprised, corrupted or send by milicious client")
            return(verify)
    def Unzip(self):

        f = zipfile.ZipFile(self.f_name,"r")


        f.extractall()




    def KeyReader(self):
        with open(key_pri, "r") as myfile:
            private_Reciever_key = RSA.importKey(myfile.read())
        keyDeCipher = PKCS1_OAEP.new(private_Reciever_key)
        f = open(self.f_name.split('.')[0] + ".key","rb")
        iv = f.read(16)
        k = keyDeCipher.decrypt(f.read())
        return  iv,k

    def fileWriting(self,verify):
        print(verify)
        if verify == True:

            tmp = open(self.f_name.split('.')[0] + ".tmp", "rb").read()

            f = open(self.f_name.split('.')[0] + ".txt", "wb")
            f.write(tmp)

            f.close()

        elif verify == False:
            print("execution failed")




    
	






