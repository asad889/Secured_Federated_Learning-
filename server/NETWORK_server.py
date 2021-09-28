import os
import socket
import threading
import tqdm
from server_dec import *
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 4096
SEPERATOR = "<SEPERATOR>"
SERVER_DATA_PATH = "/home/asadnaveed/PycharmProjects/Secured_Federated_Learning-/server"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    received = conn.recv(SIZE).decode()
    received = received.split(SEPERATOR)
    cmd = received[0]
    if cmd == "DOWNLOAD":
        with open("Global_model.pt", "rb") as f:
            while True:
                bytes_read = f.read(SIZE)

                if not bytes_read:
                    break

                conn.sendall(bytes_read)
                #progress.update(len(bytes_read))
    elif cmd == "UPLOAD":
        received_1 = conn.recv(SIZE).decode()
        filename, filesize, cmd_2 = received_1.split(SEPERATOR)
        print(filename)
        if cmd_2 == "ON":
            filename = os.path.basename(filename.split('.')[0] + ".all")
            filesize = int(filesize)

            filepath = os.path.join(SERVER_DATA_PATH, filename)

            with open(filename.split('.')[0] + ".all","wb") as f:
                while True:
                    bytes_read = conn.recv(SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    break
            dec = Decryption(filename)
            dec.Unzip()
            iv, k = dec.KeyReader()
            key_dec = AES.new(k, AES.MODE_CFB, iv)
            bin = open(filename.split('.')[0] + ".bin", "rb").read()
            f = open(filename.split('.')[0] + ".tmp", "wb")
            f.write(key_dec.decrypt(bin))
            f.close()
            key_pub = dec.Keymanagement()
            verify = dec.sigVerification(key_pub)
            dec.fileWriting(verify)
            dec.delete()
            status = f"OK{SEPERATOR}Server has already RECIEVED a file {filename} from client"
            conn.send(status.encode())
        else:
            filename = os.path.basename(filename.split('.')[0] + ".txt")
            filesize = int(filesize)

            progress = tqdm.tqdm(range(filesize), f"Recieving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            filepath = os.path.join(SERVER_DATA_PATH, filename)

            with open(filename.split('.')[0] + ".txt", "wb") as f:
                while True:
                    bytes_read = conn.recv(SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
                    break



    elif cmd == "HELP":
        data = f"OK{SEPERATOR}"
        data += "___________________________________\n"
        data += "UPLOAD: Upload a file to the server.\n"
        data += "First line : write UPLOAD.\n"
        data += "Second line : write <filename>.\n"
        data += "__________________________________\n"
        data += "DOWNLOAD: Upload a file to the server.\n"
        data += "First line : write DOWNLOAD.\n"
        data += "Second line : write <filename>.\n"
        data += "___________________________________\n"
        data += "LOGOUT: Disconnect from the server.\n"
        data += "___________________________________\n"
        data += "HELP: List all the commands.\n"
        data += "___________________________________\n"
        conn.send(data.encode())


def main():
    print("[STARTING] Server is starting")
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()


