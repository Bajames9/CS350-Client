import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


from connection import client
from userContext import user



client.connect()

session = PromptSession()


# used to updates msgs from server
async def updater():
    while True:

        # makes sure there is an active chat and that it needs to be updated
        if user.activeChat != "" and user.needsUpdate:

            #gets the chat history
            response = await client.getAllMsgFromChat(user.activeChat)

            # used to determine how many new msgs need to be printed
            length = len(response["data"])
            oldLength = len(user.priorChats)
            lengthDiff = length - oldLength
            # prints all new msgs
            for i in range(lengthDiff):
                msg = response["data"][oldLength + i]
                print(f"[{msg['sender']}] {msg['msg']}")

            # updates stored msgs to include new msgs
            user.priorChats = response["data"]
            user.needsUpdate = False

        # sleeps to avoid freezing up client code
        await asyncio.sleep(.1)






# main starting point of CLI
async def mainCLI():

    # starts the updater thread
    asyncio.create_task(updater())

    # lets me use prompt_toolkit to handle output cleanly
    with patch_stdout():
        # runs tell user quits or connection error
        while True:
            try:

                # used to get user commands
                user_input = await session.prompt_async(f"{user.username or '$'}# ")

                # splits command into components
                parts = user_input.split(" ")
                # tests first component
                match parts[0]:
                    # runs login logic if user doesn't exist it will create that user
                    case "/login":
                        response = await client.login(parts[1])
                        print("Login Success" if response else "Login Failed")

                    # sets the active chat
                    case "/setChat":
                        if user.username != "":
                            await setChat(parts[1])
                        else:
                            print("Login first use /login [username]")
                    # sends a msg
                    case "/chat":
                        if user.username != "":
                            await sendChatMsg(user_input)
                        else:
                            print("Login first use /login [username]")
                    # used to join a chat group
                    case "/join":
                        if user.username != "":
                            response = await client.joinChat(parts[1])
                            print(response["msg"])
                            await setChat(parts[1])
                        else:
                            print("Login first use /login [username]")
                    # used to create a chat group
                    case "/create":
                        if user.username != "":
                            response = await client.createChat(parts[1])
                            print(response["msg"])
                            await setChat(parts[1])
                        else:
                            print("Login first use /login [username]")
                    # used to get all chats
                    case "/getChats":
                        if user.username != "":
                            response = await client.getAllChatNames()
                            print("=============================")
                            print("All Chats")
                            print("=============================")
                            for i in range(len(response["chats"])):
                                print(response["chats"][i])
                            print("=============================")
                        else:
                            print("Login first use /login [username]")
                    # quits program
                    case "/quit":
                        if user.username != "":
                            await client.Quit()
                        break

                    # helps users with commands
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
                        print("/quit : quits the program")
                        print("/help : prints out cmds and descriptions")







            except Exception as e:
                print("Error",e)




# used to set teh active chat and send Join and Leave msgs to chats
async def setChat(chat):
    #gets msgs for chat being joined
    response = await client.getAllMsgFromChat(chat)
    #if successful
    if response["success"]:
        # sends leave msg
        if user.activeChat:
            #sends a msg to leave chat
            leaveMsg = f"/chat ### Has Left The Chat ###"
            await sendChatMsg(leaveMsg)

        #sets active chat
        user.activeChat = chat
        user.priorChats = response["data"]
        #displays msgs from chat
        for i in range(len(user.priorChats)):
            msg = response["data"][i]
            print(f"[{msg['sender']}] {msg['msg']}")

        # sends join msg
        joinMsg = f"/chat ### Has Joined The Chat ###"
        await sendChatMsg(joinMsg)



# sends a chat msg
async def sendChatMsg(user_input):
    if user.activeChat:
        parts, msg = user_input.split(" ", 1)
        response = await client.Chat(user.activeChat, msg)
    else:
        print("Set a chat as active first using /setChat [chat name]")

asyncio.run(mainCLI())