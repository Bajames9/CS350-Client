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


        buffer = ""

        while self.connected:
            try:


                chunk = self.socket.recv(4096)

                if not chunk:
                    self.connected = False
                    break

                buffer += chunk.decode()


                while "\x1e" in buffer:
                    msg, buffer = buffer.split("\x1e",1)

                    if msg.strip() == "":
                        continue

                    try:
                        json_obj = json.loads(msg)
                        self.commandQueue.append(json_obj)
                    except json.JSONDecodeError:
                        print("BAD JSON:", msg)


                if self.commandQueue:  # non-empty
                    nextCMD = self.commandQueue[0]

                    if nextCMD["command"] == "update" and nextCMD["chat"] == user.activeChat:
                        user.needsUpdate = True
                        self.commandQueue.popleft()




            except Exception as e:
                print("Listen error:", e)
                self.connected = False
                break





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