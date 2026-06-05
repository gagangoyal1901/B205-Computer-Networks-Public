import socket
import threading
import os

PORT = 5000

# receiving messages
def receive(client):
    while True:
        try:
            data = client.recv(1024)

            if not data:
                break

            # handling file receiving
            if data.startswith(b"FILE|"):
                _, filename = data.decode().split("|")

                size = int(client.recv(1024).decode())

                with open("received_" + filename, "wb") as f:
                    received = 0
                    while received < size:
                        chunk = client.recv(min(1024, size - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                print(f"\nfile received: {filename}")

            else:
                print(data.decode(), end="")

        except:
            break

    print("closing connection")
    client.close()

# sending messages
def send(client):
    while True:
        msg = input()

        # handling file sending
        if msg.startswith("sendfile"):
            try:
                _, filepath = msg.split()

                if os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    size = os.path.getsize(filepath)

                    client.sendall(f"FILE|{filename}".encode())
                    client.sendall(str(size).encode())

                    with open(filepath, "rb") as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            client.sendall(chunk)

                    print("sending file")

                else:
                    print("file not found")

            except:
                print("usage: sendfile filename")

        else:
            client.sendall(msg.encode())
