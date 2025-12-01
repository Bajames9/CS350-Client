# CS350-Client
client Code for CS350 Chat app


## Running the Client

### Command-Line Version

To run the command-line interface (CLI) version:

### Windows
    run/click the runCLI.bat file in root
### linux /macOS
    open terminal to root 
    type 
    ./runCLI.sh

### commands

    /login [username]	Logs in a user with the specified username.
    /setChat [chat name]	Sets the active chat to a private user or group chat.
    /chat -[chat name] [msg]	Sends a message to the private or group chat. Optionally specify the chat name; otherwise, the current active chat is used.
    /join [chat name]	Joins a chat group and sets it as active.
    /create [chat name]	Creates a chat group and sets it as active.
    /getChats	Displays a list of all chats or users the active user has joined or chatted with.
    /quit	Quits the program and notifies other users in the chat that you left.
    /help	Displays this list of commands and descriptions.

### UI Interface Version

### Windows
    run the runWeb.bat file in root
### linux /macOS
    open terminal to root 
    type 
    ./runWeb.sh


### Errors
    if issues running .bat or .sh files
    src/appCLI.py is the starting point for Command Line
    src/appWeb.py is the starting point for Command Line
    