#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
protocol:
    !o - python object from server
'''

from socket import socket, SOCK_STREAM, AF_INET
from threading import Thread, Timer
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import sys

class ChatThread(Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket


    def run(self):
        while True:
            message = self.socket.recv(1024)
            decoded = message.decode("utf-8")
            if decoded.startswith('!o'): #python objects
                state = eval(message[2:])
                mapStateToListBox(state)

            else: #normal message
                messages.insert(tk.END, decoded)


class FileThread(Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        while True:
            name = self.socket.recv(1024).decode("utf8")

            file = self.socket.recv(65536)

            with open('received_file', 'wb') as f:
                f.write(file)
                print('Received a file')
                messages.insert(tk.END, 'You received a file from {}.\n'.format(name))
                f.close()

    def selectFile(self, e=None):
        filename =  tk.filedialog.askopenfilename(initialdir = "/Users/Aleksy/Desktop/dsik",
        title = "Select file", filetypes = (("All files","*.*"),))
        self.sendFile(filename)

    def sendFile(self, file):
        with open(file, 'rb') as f:
            name = self.getSelectedUser()
            self.socket.send(name.encode())
            content = f.read(65536)
            print('Sending a file to {}'.format(name))
            messages.insert(tk.END, 'You sent a file to {}\n'.format(name))
            self.socket.send(content)

    def getSelectedUser(self):
        return list.get(tk.ACTIVE)


def enterHandler(e=None):
    input = entry.get('1.0', tk.END)
    client_chat_socket.send(input.encode()) #send to server
    entry.delete('1.0', tk.END)

def mapStateToListBox(state):
    list.delete(0, tk.END)
    for name in state:
        list.insert(tk.END, name)


#socket and threads configuration

#chat server
chatHost = 'localhost'
chatPort = 8888
chatAddr = (chatHost, chatPort)

#file server
fileHost = 'localhost'
filePort = 8887
fileAddr = (fileHost, filePort)

client_chat_socket = socket(AF_INET, SOCK_STREAM)
client_chat_socket.connect(chatAddr)

print('Connected to chat server as: {}'.format(client_chat_socket.getsockname()))


client_file_socket = socket(AF_INET, SOCK_STREAM)
client_file_socket.connect(fileAddr)

print('Connected to file server as: {}'.format(client_file_socket.getsockname()))

chatThread = ChatThread(client_chat_socket)
fileThread = FileThread(client_file_socket)

#GUI
root = tk.Tk()
namePrompt = tk.simpledialog.askstring('Hello', 'Enter your name')
while not namePrompt: #name not entered
    namePrompt = tk.simpledialog.askstring('Hello', 'Enter your name')

#send names to servers os they can map it to the socket
client_chat_socket.send(namePrompt.encode())
client_file_socket.send(namePrompt.encode())

nameLabel = tk.Label(root, text='Connected as {}.'.format(namePrompt)).grid(row=2)

#userInput = tk.StringVar()
entry = tk.Text(root, height=8)
entry.grid(row=1, column=0)
entry.bind('important', '<Return>', enterHandler) # enter

messages = tk.Text(root)
messages.grid(row=0, column=0)


buttons = tk.Frame(root)
sendBtn = tk.Button(buttons, text='Send', bg="steel blue", width=10, height=2, command=enterHandler).pack()
fileBtn = tk.Button(buttons, text='Send File', width=10, height=2, command=fileThread.selectFile, bg="steel blue").pack()
exitBtn = tk.Button(buttons, text='Exit', bg="steel blue",width=10, height=2).pack()
buttons.grid(row=1, column=1)

list = tk.Listbox(root, height=18)
list.grid(row=0, column=1)
list.bind('<Button-1>')
#list.pack(side=tk.RIGHT)

chatThread.start()
fileThread.start()

root.mainloop()
