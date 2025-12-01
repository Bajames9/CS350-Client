from collections import deque



#user context stores info about user
class _user:

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.username = ""
            self.activeChat = ""
            self.needsUpdate = True
            self.priorChats = []
            self.currentTyping = ""


    def setUpdate(self, value:bool):
        self.needsUpdate = value

    def setChat(self,id : str):
        self.activeChat = id
        self.needsUpdate = True

    def setUsername(self,username: str):
        self.username = username

    def updatePrior(self ,msg:dict):
        self.priorChats = msg

user = _user()