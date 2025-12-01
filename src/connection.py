import asyncio
import socket
import threading
import json
from collections import deque
from queue import Queue

from userContext import user

#Main Client Code handles Server Connection

class _TCPClient:

    # stores info for later use sets up connection
    def __init__(self, host='localhost', port=2317):
        if not hasattr(self, "initialized"):
            self.host = host
            self.port = port
            self.socket = None
            self.connected = False
            self.initialized = True
            self.commandQueue = deque()

    # connects to server if server is not up just loops tell connection is made
    def connect(self):

        while not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.connected = True
                threading.Thread(target=self.listen, daemon=True).start()



            except ConnectionRefusedError:
                pass
            except Exception as e:

                  print("Connection failed:", e)

    # used to listen for msgs from server adds them to queue
    def listen(self):

        # buffer stores msgs from server so dont rn into length limits
        buffer = ""

        while self.connected:
            try:

                # gets chunk of data from server
                chunk = self.socket.recv(4096)

                #breaks connection if not getting data
                if not chunk:
                    self.connected = False
                    break

                # adds chunk to buffer
                buffer += chunk.decode()

                # splits buffer by escape character to identify individual commands
                while "\x1e" in buffer:
                    msg, buffer = buffer.split("\x1e",1)

                    if msg.strip() == "":
                        continue

                    try:
                        json_obj = json.loads(msg)
                        # adds command to queue
                        self.commandQueue.append(json_obj)
                    except json.JSONDecodeError:
                        print("BAD JSON:", msg)

                # checks if command is update msgs
                if self.commandQueue:  # non-empty
                    nextCMD = self.commandQueue[0]

                    if nextCMD["command"] == "update" and nextCMD["chat"] == user.activeChat:
                        user.needsUpdate = True
                        self.commandQueue.popleft()




            except Exception as e:
                print("Listen error:", e)
                self.connected = False
                break





    # runs login cmd
    async def login(self, username):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "login",
                "username": username
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "login":
                        if data["status"]:
                            user.setUsername(data["user"])
                            self.commandQueue.popleft()
                            return True

                await asyncio.sleep(0.01)
        except Exception as e:
            print("Send Error:", e)
            return False


    # runs get all msg command
    async def getAllMsgFromChat(self, username):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "getChat",
                "name": username,
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "getChat":
                        user.needsUpdate = False
                        self.commandQueue.popleft()
                        return data

        except Exception as e:
            print("Send Error:", e)
            return False


    async def createChat(self, name):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "createChat",
                "name": name,
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "createChat":
                        self.commandQueue.popleft()
                    return data

        except Exception as e:
            print("Send Error:", e)
            return False


    async def joinChat(self, chatName):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "joinChat",
                "name": chatName,
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "joinChat":
                        self.commandQueue.popleft()
                        return data

        except Exception as e:
            print("Send Error:", e)
            return False


    async def getAllChatNames(self):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "getChatNames"
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "getChatNames":
                        self.commandQueue.popleft()
                        return data

        except Exception as e:
            print("Send Error:", e)
            return False

    async def Quit(self):
        if not self.connected:
            return

        try:
            json_obj = {
                "command": "quit"
            }
            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "quit":
                        print("Disconnected from server.")
                    return data


        except Exception as e:
            print("Error quitting:", e)


    async def Chat(self, recipient, msg):


        if not self.connected:
            return False
        try:
            json_obj = {
                "command": "chat",
                "name": recipient,
                "msg": msg
            }

            self.socket.sendall(f"{json.dumps(json_obj)}\x1e".encode())

            while True:
                if self.commandQueue:  # non-empty
                    data = self.commandQueue[0]
                    if data["command"] == "chat":
                        user.needsUpdate = True
                        self.commandQueue.popleft()
                    return data

        except Exception as e:
            print("Send Error:", e)
            return False


client = _TCPClient()