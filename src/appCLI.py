import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


from connection import client
from userContext import user



client.connect()

session = PromptSession()



async def updater():
    while True:

        if user.activeChat != "" and user.needsUpdate:

            response = await client.getAllMsgFromChat(user.activeChat)

            length = len(response["data"])
            oldLength = len(user.priorChats)
            lengthDiff = length - oldLength
            for i in range(lengthDiff):
                msg = response["data"][oldLength + i]
                print(f"[{msg['sender']}] {msg['msg']}")

            user.priorChats = response["data"]
            user.needsUpdate = False

        await asyncio.sleep(.1)







async def mainCLI():

    asyncio.create_task(updater())

    with patch_stdout():
        while True:
            try:

                user_input = await session.prompt_async(f"{user.username or '$'}# ")

                parts = user_input.split(" ")
                match parts[0]:
                    case "/login":
                        response = await client.login(parts[1])
                        print("Login Success" if response else "Login Failed")

                    case "/setChat":
                        await setChat(parts[1])

                    case "/chat":

                        if user.activeChat:
                            parts, msg = user_input.split(" ",1)
                            response = await client.Chat(user.activeChat, msg)
                        else:
                            print("Set a chat as active first using /setChat [chat name]")


                    case "/join":
                        response = await client.joinChat(parts[1])
                        print(response["msg"])
                        await setChat(parts[1])

                    case "/create":
                        response = await client.createChat(parts[1])
                        print(response["msg"])
                        await setChat(parts[1])

                    case "/getChats":
                        response = await client.getAllChatNames()
                        print("=============================")
                        print("All Chats")
                        print("=============================")
                        for i in range(len(response["chats"])):
                            print(response["chats"][i])
                        print("=============================")

                    case "/help":
                        print("=============================")
                        print("All Commands")
                        print("Key: [] = user input, -[] = optional input, : = start of description")
                        print("=============================")
                        print("/login [username]: Logs in a user")
                        print("/setChat [chat name]: sets a users active chat to a private user or group chat")
                        print("/chat -[chat name] [msg]:sends a msg to the private chat ot group chat also sets chat to active chat -[chat name] optional if chat is already set")
                        print("/join [chat name]: joins a chat group sets chat to active")
                        print("/create [chat name]: creates a chat group sets chat to active")
                        print("/getChats : prints out a list of all chats or users that active user has joined or chatted with")
                        print("/help : prints out cmds and descriptions")







            except Exception as e:
                print("Error",e)


async def setChat(chat):
    response = await client.getAllMsgFromChat(chat)
    if response["success"]:
        user.activeChat = chat
        user.priorChats = response["data"]
        for i in range(len(user.priorChats)):
            msg = response["data"][i]
            print(f"[{msg['sender']}] {msg['msg']}")


asyncio.run(mainCLI())