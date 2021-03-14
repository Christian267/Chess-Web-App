from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

HOST = '127.0.0.1'
PORT = 23456
ADDR = (HOST, PORT)
BUFFERSIZE = 1024

class Client:
    def __init(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        sel.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()
    
    def receive_messages(self):