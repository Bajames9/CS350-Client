from nicegui import ui
from connection import client
from userContext import user
from nicegui.elements.scroll_area import ScrollArea
import time

message_col: ui.column = None
chat_scroll_area: ScrollArea = None

#Main Chat page



# used to send chat msgs
async def handleInput(e):
    
    input_value = e.sender.value
    print(input_value)
    await client.Chat(user.activeChat, input_value)
    e.sender.set_value('')
    e.sender.update()


# used to join Chat groups
async def handleJoin(e):
    
    input_value = e.sender.value
    print(input_value)
    data = await client.joinChat(input_value)
    if data["success"] == False:
        n = ui.notification(timeout=10)
        n.message = data["msg"]

    user.setChat(input_value)
    await update_msg_display()
    e.sender.set_value('')
    e.sender.update()


#used To create Chat groups
async def handleCreate(e):
    
    input_value = e.sender.value
    print(input_value)
    data = await client.createChat(input_value)
    if data["success"] == False:
        n = ui.notification(timeout=10)
        n.message = data["msg"]
    else:

        user.setChat(input_value)
        await update_msg_display()
    e.sender.set_value('')
    e.sender.update()


#main display code for chat page
async def chat():
    # makes sure user is logged in
    if user.username == "":
        ui.navigate.to("/")

    # outer divs
    with ui.row().classes('w-full h-screen p-0 m-0 gap-0 overflow-hidden'):
        with ui.element('div').classes(
            'flex w-full h-full bg-[radial-gradient(circle_at_bottom_right,_#415A77,_#1B263B,_#0D1B2A)]'
        ):
            
            with ui.element('div').classes('flex flex-row w-full h-7/8'):
    
                # Left column
                with ui.element('div').classes('flex flex-col gap-4 p-4 w-3/8 h-full'):
                    global chat_dropdown_container
                    chat_dropdown_container = ui.column().classes('p-0 m-0 flex-1 overflow-auto')  # this fills available vertical space
                    
                    await getChats()
                    
                    # Input section
                    with ui.element('div').classes('flex flex-col gap-2'):
                        join_input = ui.input("Join chat").classes('bg-[#778da9] rounded p-2')
                        join_input.on('keydown.enter', handleJoin)
                        create_input = ui.input("Create chat").classes('bg-[#778da9] rounded p-2')
                        create_input.on('keydown.enter', handleCreate)

                # Right column
                global chat_scroll_area
                with ui.scroll_area().classes('flex-1 w-5/8 h-full border') as chat_scroll_area:
                    global message_col
                    message_col = ui.column().classes('w-full items-start min-h-[0px]') 

                ui.timer(0.1, update_msg_display)
                        
                   
                    

              

                # Chat input
                chat_input = ui.input(label='Chat') \
                    .props('input-class="text-white text-2xl"') \
                    .classes('w-full bg-[#778da9] rounded-2xl p-2')
                
                chat_input.on('keydown.enter', handleInput)



chat_dropdown: ui.dropdown_button = None  # global


# used to getActive Chats for dropdown
async def getChats():
    global chat_dropdown_container
    if chat_dropdown_container is None:
        print("Error: chat_dropdown_container not initialized.")
        return

    chats = await client.getAllChatNames()
    user.updatePrior(chats["chats"])


    chat_dropdown_container.clear()
    

    # sets chat dropdown with data
    with chat_dropdown_container:
        with ui.dropdown_button('active chats', auto_close=True) as new_chat_dropdown:
            for chat_id in user.priorChats:
                ui.item(chat_id, on_click=lambda id=chat_id: setChat(id))
                
    chat_dropdown_container.update()

        

# sets the active chat
async def setChat(chatId):


    if user.activeChat:
        leaveMsg = f"/chat ### Has Left The Chat ###"
        await sendChatMsg(leaveMsg)

    user.setChat(chatId)
    print(user.activeChat)


    joinMsg = f"/chat ### Has Joined The Chat ###"
    await sendChatMsg(joinMsg)


# sends a chat msg used for server leave and join
async def sendChatMsg(user_input):
    if user.activeChat:
        parts, msg = user_input.split(" ", 1)
        response = await client.Chat(user.activeChat, msg)




# used to display msgs
def chatBox(sender: str, text: str):


    fromUser = sender
    if sender == 'me':
        alignment_classes = 'self-end bg-[#b8c4d3]'
        fromUser = user.username


    else:
        alignment_classes = 'self-start bg-amber-100'

    with ui.element('div').classes(f'flex flex-col h-fit p-2 rounded-lg m-1 {alignment_classes} max-w-[80%] whitespace-normal break-all'):
        ui.label(f"{fromUser}# {text}").classes('p-0 m-0')


# used to update msgs
async def update_msg_display():

    if user.activeChat != "" and user.needsUpdate:
        print("update")
        messages_json = await client.getAllMsgFromChat(user.activeChat)
  
        if messages_json["success"]:
            messages = messages_json["data"]


            with message_col:
                message_col.clear()

                for msg in messages:
                    sender = msg['sender']
                    text = msg['msg']

                    if sender == user.username:
                        chatBox('me', text)
                    else:
                        chatBox(sender, text)

            message_col.update()
       
            




