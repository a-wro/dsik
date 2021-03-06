#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_STREAM, timeout
from threading import Thread
from sys import exit

BUFFER_SIZE = 2**16 + 1

class ChatServer(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.clientState = {} # socket key

        host = '150.254.78.29'

        port = 4443
        addr = (host, port)

        self.server.bind(addr)
        self.server.listen(5)

        while True:
            client, addr = self.server.accept() # connection(socket), address
            print("Chat server:{} has connected.".format(addr))

            clientThread = Thread(target=self.clientHandler, args=(client,))
            clientThread.start()

    def clientHandler(self, client):  # Takes client socket as argument
        name = client.recv(BUFFER_SIZE).decode("utf8") # from tkinter.simpledialog
        msg = "{} has joined the chat\n".format(name)
        self.broadcast(msg.encode())
        self.clientState[name] = client
        self.broadcast(('!o' + self.userState()).encode()) #broadcast chat state to users
        #with !o header
        #chat logic
        while True:
            msg = client.recv(BUFFER_SIZE)
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

        host = '150.254.78.29'
        port = 4442
        addr = (host, port)

        self.server.bind(addr)
        self.server.listen(5)

        while True:
            client, addr = self.server.accept()
            print("File server:{} has connected.".format(addr))
            name = client.recv(BUFFER_SIZE).decode("utf8") #name
            self.clients[name] = client #map name to socket
            clientThread = Thread(target=self.clientHandler, args=(client,))
            clientThread.start()

    def clientHandler(self, client):
        while True:
<<<<<<< HEAD
=======
            name = client.recv(128).decode("utf8") #who to send to
            print(name)
>>>>>>> f54ff96dfaa404ac6bb76f1668de66121e82669e
            f = open('server_file', 'wb')

            l = client.recv(BUFFER_SIZE) #(name:file)
            name, content = splitBytes(l)

            while (content):
                try:
                    print("Receiving")
                    f.write(content)
                    client.settimeout(3.0)
                    content = client.recv(BUFFER_SIZE)
                except:
                    print('Done receiving')
                    f.close()
                    client.settimeout(None)
                    break

            f = open('server_file', 'rb')
            receivingSocket = self.clients[name.decode()]

            print('Sending a file to ' + str(receivingSocket.getpeername()))
<<<<<<< HEAD
            #receivingSocket.send(frm.encode())
=======
        #    receivingSocket.send(frm.encode())
>>>>>>> f54ff96dfaa404ac6bb76f1668de66121e82669e


            l = f.read(BUFFER_SIZE)
            while l:
                receivingSocket.send(l)
                print('Passing data')
                l = f.read(BUFFER_SIZE)
            f.close()
            print('Done sending')

def splitBytes(bts):
    def findColon():
        i = 0
        for b in bts:
            if b == 58:
                return i
            i += 1
    i = findColon()
    return (bts[:i], bts[i+1:])



chatServer = ChatServer()
print("Chat server running..")
chatServer.start()

fileServer = FileServer()
print("File server running..")
fileServer.start()
