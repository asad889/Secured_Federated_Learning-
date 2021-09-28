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
KEYS_DATA_PATH = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management"


class Encryption:
    def __init__(self,f_name,key):
        self.f_name = f_name
        self.key = key


    def sigGenerator(self):
        f = open(self.f_name, "rb")
        buffer = f.read()
        f.close()
        hash_file = SHA256.new(buffer)
        private_key = False
        data = os.path.basename(self.key)
        KEYS_DATA_PATH ="/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management"
        key_path = os.path.join(KEYS_DATA_PATH,data)
        key_pri = key_path
        with open(key_pri, "r") as myfile:
            private_Sender_key = RSA.importKey(myfile.read())
        keySigner = PKCS1_v1_5.new(private_Sender_key)
        f = open(self.f_name.split('.')[0] + ".sig", "wb")
        f.write(keySigner.sign(hash_file))
        f.close()



    def keyGenerator(self,key_pub):

        key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +string.digits) for x in range(32))
        key = key.encode()
        hash_key = SHA256.new(key)
        with open (key_pub , "r") as myfile:
            Public_key_Reciever = RSA.importKey(myfile.read())
        keyCipher = PKCS1_OAEP.new(Public_key_Reciever)
        # Saving encrypted key to *.key file
        f = open(self.f_name.split('.')[0] + ".key", "wb")

        f.write(iv + keyCipher.encrypt(hash_key.digest()))
        f.close()
        ret = hash_key.digest()
        return ret


    def merger(self):
        f = zipfile.ZipFile(self.f_name.split('.')[0]+".all","w")
        f.write(self.f_name.split('.')[0]+".sig")
        f.write(self.f_name.split('.')[0]+".bin")
        f.write(self.f_name.split('.')[0]+".key")
        f.close()
    def delete(self):
        os.remove(self.f_name.split('.')[0]+".sig")
        os.remove(self.f_name.split('.')[0]+".bin")
        os.remove(self.f_name.split('.')[0]+".key")
    

   
    def encipher(self, key):
        f = open(self.f_name, "rb")
        buffer = f.read()
        f.close()

        key_enc = AES.new(key, AES.MODE_CFB, iv)
        f = open(self.f_name.split('.')[0] + ".bin", "wb")
        f.write(key_enc.encrypt(buffer))
        f.close()

        return(key_enc.encrypt(buffer))
iv = Random.new().read(AES.block_size)






