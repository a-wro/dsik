#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from sys import exit

class ChatServer(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.clientState = {} # socket key

        host = '127.0.0.1'
        port = 8888
        addr = (host, port)

        self.server.bind(addr)
        self.server.listen(5)

        while True:
            client, addr = self.server.accept() # connection(socket), address
            print("Chat server:{} has connected.".format(addr))

            clientThread = Thread(target=self.clientHandler, args=(client,))
            clientThread.start()

    def clientHandler(self, client):  # Takes client socket as argument
        name = client.recv(1024).decode("utf8") # from tkinter.simpledialog
        msg = "{} has joined the chat\n".format(name)
        self.broadcast(msg.encode())
        self.clientState[name] = client
        self.broadcast(('!o' + self.userState()).encode()) #broadcast chat state to users
        #with !o header
        #chat logic
        while True:
            msg = client.recv(1024)
            decoded = msg.decode("utf8")
            print(decoded)
            if (decoded != '!quit'):
                sender = name + ': '
                self.broadcast(sender.encode() + msg)
            else: #!quit
                client.close()
                del self.clientState[name]
                print("{} has left the chat.".format(name))
                self.broadcast("{} has left the chat.".format(name).encode())
                exit()

    def broadcast(self, msg):  # takes in encoded msg
        #send to every client
        for socket in self.clientState.values():
            socket.send(msg)

    def userState(self):
        users = []
        for user in self.clientState.keys():
            users.append(user)
        return str(users)

'''
protocol:
    name:file content
'''
class FileServer(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.clients = {} #internal state - name to socket mapping

        host = '127.0.0.1'
        port = 8887
        addr = (host, port)

        self.server.bind(addr)
        self.server.listen(5)

        while True:
            client, addr = self.server.accept()
            print("File server:{} has connected.".format(addr))
            name = client.recv(1024).decode("utf8") #name
            self.clients[name] = client #map name to socket
            clientThread = Thread(target=self.clientHandler, args=(client, name))
            clientThread.start()

    def clientHandler(self, client, frm):
        while True:
            name = client.recv(1024).decode("utf8") #who to send to
            file = client.recv(1024)
            receivingSocket = self.clients[name]
            print('Sending a file to ' + str(receivingSocket.getpeername()))
            receivingSocket.send(frm.encode())
            receivingSocket.send(file)

chatServer = ChatServer()
print("Chat server running..")
chatServer.start()

fileServer = FileServer()
print("File server running..")
fileServer.start()
