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


# File name to encrypt



def sigGenerator(f_name,key_pri):
    # Opening and reading file to encrypt
    f = open(f_name, "rb")
    buffer = f.read()
    print(buffer)
    f.close()

    #enocding beacuse of error
    buffer1 = buffer

    # Creating hash of the file. Using SHA-256 (SHA-512 rose problems)
    hash_file = SHA256.new(buffer1)
    # Reading private key of sender to sign file with
    private_key = False
    with open (key_pri , "r") as myfile:
        private_Sender_key = RSA.importKey(myfile.read())
    keySigner = PKCS1_v1_5.new(private_Sender_key)
    f = open(f_name.split('.')[0] + ".sig","wb")
    f.write(keySigner.sign(hash_file))
    f.close()

def keyGenerator(f_name, iv,key_pub):
    # Generating 1024 random bits, and creating SHA-256 (for 32 bits compatibility with AES)
    key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +string.digits) for x in range(32))
    #iv = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    key = key.encode()
    hash_key = SHA256.new(key)

    # Reading public key to encrypt AES key with
    with open (key_pub , "r") as myfile:
        Public_key_Reciever = RSA.importKey(myfile.read())

    keyCipher = PKCS1_OAEP.new(Public_key_Reciever)
    # Saving encrypted key to *.key file
    f = open(f_name.split('.')[0] + ".key", "wb")
    f.write(iv + keyCipher.encrypt(hash_key.digest()))
    f.close()
    # Returning generated key to encrypt file with
    return hash_key.digest()

def encipher(f_name):
    # Opening file to encrypt in binary reading mode

    f = open(f_name, "rb")
    buffer = f.read()
    f.close()
    if f_name == "fedavg_1.txt":
        key_pri = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management/client1_pri_key.pem"
        key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management/pub_server.pem"
    else:
        key_pri = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management/client2_pri_key.pem"
        key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management/pub_server.pem"
    # Generating file's signature (and saving it)

    sigGenerator(f_name,key_pri)

    iv = Random.new().read(AES.block_size)
    key = keyGenerator(f_name,iv,key_pub)
    key_enc = AES.new(key, AES.MODE_CFB, iv)
    f = open(f_name.split('.')[0] + ".bin", "wb")
    f.write(key_enc.encrypt(buffer))
    f.close()
    return(key_enc.encrypt(buffer))





