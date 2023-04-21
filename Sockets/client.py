import socket
import threading


HOST = '127.0.0.1'
PORT = 12345
ENCODING = 'ascii'


def receive(conn: socket.socket) -> None:
    while True:
        try:
            message = conn.recv(1024).decode(ENCODING)
            print(message)
        except OSError as e:
            print("Error!", e)
            conn.close()
            break


def write(conn: socket.socket, client_name: str) -> None:
    while True:
        message = input()
        try:
            conn.send(f'{client_name}: {message}'.encode(ENCODING))
        except OSError as e:
            print("Error!", e)
            conn.close()
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    name = input("Write your name: ")
    s.send(name.encode(ENCODING))

    receive_thread = threading.Thread(target=receive, args=(s, ))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(s, name))
    write_thread.start()

    receive_thread.join()
    write_thread.join()
