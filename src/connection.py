import asyncio
import socket
import threading
import json
from collections import deque
from queue import Queue

from userContext import user



class _TCPClient:

    def __init__(self, host='localhost', port=2317):
        if not hasattr(self, "initialized"):
            self.host = host
            self.port = port
            self.socket = None
            self.connected = False
            self.initialized = True
            self.commandQueue = deque()

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


    def listen(self):
        """Continuously wait for messages from the server."""
        while self.connected:
            try:
                data = self.socket.recv(1024)

                if data != "":
                    text = data.decode().strip("\x1e")
                    json_obj = json.loads(text)
                    self.commandQueue.append(json_obj)

                if self.commandQueue:  # non-empty
                    nextCMD = self.commandQueue[0]

                    if nextCMD["command"] == "update" and nextCMD["chat"] == user.activeChat:
                        print("update")
                        user.needsUpdate = True
                        self.commandQueue.popleft()




            except Exception as e:
                print("Listen error:", e)
                self.connected = False
                break





    async def login(self, username):

        print("login")

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


    async def getAllMsgFromChat(self, username):

        print("getAllMsg")

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

        print("createChat")

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

        print("joinChat")

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

        print("getAllChatNames")

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

    async def Chat(self, recipient, msg):

        print("Chat")

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