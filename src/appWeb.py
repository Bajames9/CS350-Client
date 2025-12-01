import multiprocessing

multiprocessing.set_start_method('spawn', force=True)

from nicegui import ui, Client
from login import login
from chat import chat
from connection import client
import socket


# connects to server
client.connect()



# route for login page of ui
@ui.page('/')
async def index_page(client: Client):
    await client.connected()
    client.layout.classes(remove='q-pa-lg').classes('p-0 m-0') 
    client.content.classes(remove='q-pa-md').classes('p-0 m-0')
    ui.add_head_html('<style>body, html { margin: 0 !important; padding: 0 !important; }</style>')

    login()


# route for main chat page of ui
@ui.page('/home')
async def home_page(client: Client):
    await client.connected()
    client.layout.classes(remove='q-pa-lg').classes('p-0 m-0') 
    client.content.classes(remove='q-pa-md').classes('p-0 m-0')
    ui.add_head_html('<style>body, html { margin: 0 !important; padding: 0 !important; }</style>')

    await chat()





# insures client uses a new port if one is already being used for ui display
def find_free_port(start=8000, end=8100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found")

port = find_free_port()  # finds the first available port
ui.run(port=port)