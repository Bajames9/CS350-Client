from nicegui import ui
from connection import client
from userContext import user
import json

async def handle_login(username: str):
    response  = await client.login(username)

    if response:
          ui.navigate.to("/test")


def login():
    with ui.row().classes('w-full h-screen p-0 m-0 gap-0'):
        with ui.element('div').classes(
            'flex flex-row justify-center items-center w-full h-full ' \
            'bg-[radial-gradient(circle_at_bottom_right,_#415A77,_#1B263B,_#0D1B2A)]'
            ):
            with ui.element('div').classes('flex flex-col justify-center items-center h-100 w-150 bg-[#415a77] rounded-2xl shadow-2xl gap-4'):
                with ui.element('div').classes('w-3/4 rounded-2xl overflow-hidden text-2xl'):
                    username_input = ui.input(label='Username', placeholder='Enter Username') \
                        .props(' input-class="text-white text-2xl"') \
                        .classes('w-full bg-[#778da9] rounded-2xl p-2')
                with ui.element('button').classes('bg-[#778da9] w-3/4 h-15 rounded-2xl hover:bg-[#9ab4c9] transition-colors duration-300'
                    ) as login_btn:
                    ui.label('Login').classes('text-2xl text-white font-bold')

                async def on_click(e):
                    await handle_login(username_input.value)
                login_btn.on('click', on_click)



    
