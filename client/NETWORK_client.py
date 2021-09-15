import socket
import tqdm
import os
import argparse
from sender_enc import *

IP = socket.gethostbyname(socket.gethostname())  # to get the IPaddress
PORT = 4456  # to get the port number
ADDR = (IP, PORT)  # adress is tuple of ipaddress and port number
SIZE = 4096
SEPERATOR = "<SEPERATOR>"
CLIENT_DATA_PATH = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/client"


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
        #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "wb") as f:
            while True:
                bytes_read = client.recv(SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                #progress.update(len(bytes_read))
                break





    elif cmd == "LOGOUT":
        while True:
            client.send(cmd.encode())
            break

    elif cmd == "UPLOAD":
        data_1 = input("> ")
        data_1 = data_1.split(" ")
        filename = data_1[0]
        filesize = os.path.getsize(filename)
        d = f"{filename}{SEPERATOR}{filesize}".encode()
        client.send(d)
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        enc = encipher(filename)
        with open(filename.split('.')[0] + ".bin","rb") as f:
            while True:
                bytes_read = f.read(SIZE)

                if not bytes_read:

                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        with open(filename.split('.')[0] + ".sig","rb") as f:
            while True:
                bytes_read = f.read(SIZE)

                if not bytes_read:

                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        with open(filename.split('.')[0] + ".key","rb") as f:
            while True:
                bytes_read = f.read(SIZE)

                if not bytes_read:

                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        received = client.recv(SIZE).decode()

        received = received.split(SEPERATOR)

        print(received[1])

    else:
        print("********************************")
        print("Wrong Command, To see the guideline write HELP")
        print("********************************")

    print("Disconnected from the server.")
    client.close()
if __name__ == "__main__":
    main()
