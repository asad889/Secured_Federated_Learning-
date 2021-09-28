import socket
from tqdm import tqdm
import os
import argparse
import time
from client_enc import *


IP = socket.gethostbyname(socket.gethostname())  # to get the IPaddress
PORT = 4456  # to get the port number
ADDR = (IP, PORT)  # adress is tuple of ipaddress and port number
SIZE = 4096
SEPERATOR = "<SEPERATOR>"
CLIENT_DATA_PATH = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client"
start = time.process_time_ns()

def main():
    print("********************************")
    print("********************************")
    print("To see the guideline write HELP")
    print("********************************")
    print("********************************")

    data = input("> ")
    data = data.split(" ")
    cmd = data[0]
    client = socket.socket()      # creating a socket for client
    print("SOCKET HAS BEEN CREATED")
    print("********************************")
    client.connect(ADDR)  # client socket is connected with server socket
    print(f"SOCKET HAS BEEN CONNECTED TO {IP}:{PORT}")
    print("********************************")
    c = f"{cmd}{SEPERATOR}".encode()
    client.send(c)
    # s.send(f"{filename}{SEPARATOR}{filesize}".encode())



    if cmd == "HELP":
        received = client.recv(SIZE).decode()

        received = received.split(SEPERATOR)

        print(received[1])

    elif cmd == "DOWNLOAD":
        data_2 = input("> ")
        data_2 = data_2.split(" ")
        filename = data_2[0]
        #filesize = os.path.getsize(filename)

        filename = os.path.join(CLIENT_DATA_PATH, filename)

        with open(filename, "wb") as f:
            while True:
                bytes_read = client.recv(SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                break





    elif cmd == "LOGOUT":
        while True:
            client.send(cmd.encode())
            break

    elif cmd == "UPLOAD":
        print("write file name you want to transfer")
        data_1 = input("> ")
        data_1 = data_1.split(" ")
        filename = data_1[0]
        filesize = os.path.getsize(filename)
        print("write ON if you want to turn encryption ON else OFF" )
        data_2 = input("> ")
        cmd_2 = data_2
        d = f"{filename}{SEPERATOR}{filesize}{SEPERATOR}{cmd_2}".encode()
        client.send(d)




        if cmd_2 == "OFF":
            with open(filename.split('.')[0] + ".txt", "rb") as f:
                while True:
                    bytes_read = f.read(SIZE)

                    if not bytes_read:
                        break
                    client.sendall(bytes_read)

        elif cmd_2 == "ON":

            print("enter client private key")
            data = input("> ")
            data = data.split(" ")
            key = data[0]
            key_pub = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client/keys_management/pub_server.pem"
            enc = Encryption(filename,key)
            sign = enc.sigGenerator()
            iv = Random.new().read(AES.block_size)
            key = enc.keyGenerator(key_pub)
            enc.encipher(key)
            enc.merger()
            enc.delete()

            with open(filename.split('.')[0] + ".all","rb") as f:
                while True:
                    bytes_read = f.read(SIZE)

                    if not bytes_read:

                        break
                    client.sendall(bytes_read)




            received = client.recv(SIZE).decode()

            received = received.split(SEPERATOR)

            #print(received[1])

    else:
        print("********************************")
        print("Wrong Command, To see the guideline write HELP")
        print("********************************")

    print("Disconnected from the server.")
    client.close()
    print("-----------------------------")
    #print(time.process_time_ns() - start)
if __name__ == "__main__":
    main()
