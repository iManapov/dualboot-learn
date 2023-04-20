import socket
import threading
import logging


HOST = '127.0.0.1'
PORT = 12345
ENCODING = 'ascii'

logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d; %(levelname)s; %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

clients: dict = {}


def broadcast(message: bytes) -> None:
    for client in clients:
        client.send(message)


def handle(client: socket.socket, address: str) -> None:
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
                logging.info(f'{address}; {message.decode(ENCODING)}')
        except OSError:
            name = clients.pop(client)
            client.close()
            broadcast(f'{name} left the chat!'.encode(ENCODING))
            break


def receive(connection: socket.socket) -> None:
    while True:
        client, address = connection.accept()

        name = client.recv(1024).decode(ENCODING)
        clients[client] = name

        broadcast(f'{name} joined!'.encode(ENCODING))
        client.send('Connected to server!'.encode(ENCODING))

        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    receive(s)
