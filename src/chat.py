from nicegui import ui
from connection import client
from userContext import user
from nicegui.elements.scroll_area import ScrollArea
import time

message_col: ui.column = None
chat_scroll_area: ScrollArea = None

async def handleInput(e):
    
    input_value = e.sender.value
    print(input_value)
    await client.Chat(user.activeChat, input_value)
    e.sender.set_value('')
    e.sender.update()

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

async def chat():
    if user.username == "":
        ui.navigate.to("/")

    with ui.row().classes('w-full h-screen p-0 m-0 gap-0 overflow-hidden'):
        with ui.element('div').classes(
            'flex w-full h-full bg-[radial-gradient(circle_at_bottom_right,_#415A77,_#1B263B,_#0D1B2A)]'
        ):
            
            with ui.element('div').classes('flex flex-row w-full h-7/8'):
    
                # Left column (dropdown + inputs)
                with ui.element('div').classes('flex flex-col gap-4 p-4 w-3/8 h-full'):
                    global chat_dropdown_container
                    chat_dropdown_container = ui.column().classes('p-0 m-0 flex-1 overflow-auto')  # this fills available vertical space
                    
                    await getChats()
                    
                    # Input section stays at bottom
                    with ui.element('div').classes('flex flex-col gap-2'):
                        join_input = ui.input("Join chat").classes('bg-[#778da9] rounded p-2')
                        join_input.on('keydown.enter', handleJoin)
                        create_input = ui.input("Create chat").classes('bg-[#778da9] rounded p-2')
                        create_input.on('keydown.enter', handleCreate)

                # Right column (chat scroll area)
                global chat_scroll_area
                with ui.scroll_area().classes('flex-1 w-5/8 h-full border') as chat_scroll_area:
                    global message_col
                    message_col = ui.column().classes('w-full items-start min-h-[0px]') 

                ui.timer(0.1, update_msg_display)
                        
                   
                    

              

                # Chat input fixed to bottom
                chat_input = ui.input(label='Chat') \
                    .props('input-class="text-white text-2xl"') \
                    .classes('w-full bg-[#778da9] rounded-2xl p-2')
                
                chat_input.on('keydown.enter', handleInput)



chat_dropdown: ui.dropdown_button = None  # global

async def getChats():
    global chat_dropdown_container # Need access to the container
    if chat_dropdown_container is None:
        # This shouldn't happen if chat() runs first, but is a safe guard.
        print("Error: chat_dropdown_container not initialized.")
        return

    chats = await client.getAllChatNames()
    user.updatePrior(chats["chats"])

    # Clear the container instead of deleting the element
    # This removes all elements from the container's slot cleanly.
    chat_dropdown_container.clear()
    
    # 3. Build the new dropdown inside the cleared container
    with chat_dropdown_container:
        with ui.dropdown_button('active chats', auto_close=True) as new_chat_dropdown:
            for chat_id in user.priorChats:
                # The dropdown variable is now local to this function scope
                ui.item(chat_id, on_click=lambda id=chat_id: setChat(id))
                
    chat_dropdown_container.update()

        
        
def setChat(chatId):
    user.setChat(chatId)
    print(user.activeChat)


def userBox(user: str):
    with ui.element('div').classes(

            'flex justify-start items-center w-[130%] h-15 transform -translate-x-3 '
            'transition-all duration-500 group-hover:w-[200%]'
        ):
            with ui.element('div').classes(
          
                'flex flex-row justify-center items-center w-15 h-15 bg-amber-100 rounded-2xl '
                'transition-all group-hover:w-full duration-500 group-hover:justify-start pl-4'
            ):
                ui.label(user[0].upper()).classes(
                    'text-4xl transition-all duration-100 group-hover:opacity-0 absolute'
                )
                ui.label(user).classes(
                    'text-2xl font-semibold opacity-0 transition-all group-hover:opacity-100 ml-10'
                )

def chatBox(sender: str, text: str):
    """
    Creates a single message bubble within the current UI context.
    The message_col context must be active when this is called.
    """
    if sender == 'me':
        alignment_classes = 'self-end bg-[#b8c4d3]'
    else:
        alignment_classes = 'self-start bg-amber-100'
    
    # Building the element inside the active context (which should be message_col)
    with ui.element('div').classes(f'flex flex-col h-fit p-2 rounded-lg m-1 {alignment_classes} max-w-[80%] whitespace-normal break-all'):
        ui.label(text).classes('p-0 m-0')

async def update_msg_display():

    if user.activeChat != "" and user.needsUpdate:
        print("update")
        messages_json = await client.getAllMsgFromChat(user.activeChat)
  
        if messages_json["success"]:
            messages = messages_json["data"]

            # Use a 'with' block to ensure all subsequent elements are built 
            # within the message_col container.
            with message_col:
                # Clear previous messages so we don't duplicate (Issue 2 Fix)
                message_col.clear() 

                # Add each message to the column (Issue 1 Fix)
                for msg in messages:
                    sender = msg['sender']
                    text = msg['msg']

                    if sender == user.username:  # assuming user.username is your current user
                        chatBox('me', text)
                    else:
                        chatBox(sender, text)

            # Important: Update the column itself to reflect the cleared/added messages
            message_col.update()
       
            




