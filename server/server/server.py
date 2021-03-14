from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
from user import user

HOST = '127.0.0.1'
PORT = 23456
ADDR = (HOST, PORT)
BUFFERSIZE = 1024

users = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(HOST, PORT)

def client_communication(client):


    while True:
        msg = client.recv(BUFFERSIZE)
        if msg == bytes('{quit}', 'utf8'):
            client.send(bytes('{quit}', 'utf8'))
            client.close()
            del clients[client]
            broadcast(bytes(f'{name} has left the game.', 'utf8'))
        else:
            broadcast(msg, name + ': ')


def accept_incoming_connections():
""" Waits for connection from new clients, sets up handling once connected."""
    While True:
        client, client_address = SERVER.accept()
        print(f'{client_address} has connected to the server: {time.time()}')

        Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    SERVER.listen()
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()