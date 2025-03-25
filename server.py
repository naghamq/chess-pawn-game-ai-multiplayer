import socket
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pygame
global time
global boardArray

clients = []
# Create a server socket
serverSocket = socket.socket()

print("Server socket created")

# Associate the server socket with the IP and Port
ip = "127.0.0.1"
port = 9999
serverSocket.bind((ip, port))
print("Server socket bound with with ip {} port {}".format(ip, port))

# Make the server listen for incoming connections
serverSocket.listen()

# Server incoming connections "one by one"
count = 0
while True:
    # wait for the two agents to connect
    (clientConnection, clientAddress) = serverSocket.accept()
    count += 1
    clients.append(clientConnection)

    (clientConnection, clientAddress) = serverSocket.accept()
    count += 1
    clients.append(clientConnection)

    print("Accepted {} connections".format(count))

    msg = str.encode("Connected to the server")
    clients[0].send(msg)
    clients[1].send(msg)

    # Send time to clients
    time_input = input("Enter time (in minutes): ")
    time_msg = str.encode(time_input)
    clients[0].send(time_msg)
    clients[1].send(time_msg)

    # Send Begin to clients
    begin_msg = input("Type 'Begin' to start: ")
    begin_msg = str.encode(begin_msg)
    clients[0].send(begin_msg)
    clients[1].send(begin_msg)

    # Assign colors to clients
    msg = str.encode("White")
    clients[0].send(msg)
    msg = str.encode("Black")
    clients[1].send(msg)

    # Board setup: choose between Classic or Setup.
    setup_option = input("Enter board setup option (Classic or Setup): ").strip()
    if setup_option.lower() == "classic":
        setup_msg = "Classic"
    else:
        setup_msg = input("Enter custom setup string (e.g. 'Setup Wb4 Wa3 Wc2 Bg7'): ").strip()
    setup_msg_bytes = setup_msg.encode()
    clients[0].send(setup_msg_bytes)
    clients[1].send(setup_msg_bytes)

    # Determine which player begins based on setup string ending (if applicable)
    if setup_msg.endswith("BLACK"):
        player_index = 1
    elif setup_msg.endswith("WHITE"):
        player_index = 0
    else:
        player_index = 0

    # Read moves from client connection and relay them
    while True:
       if player_index == 0:
           turn_msg = str.encode("White's turn")
           clients[1].send(turn_msg)
       else:
           turn_msg = str.encode("Black's turn") 
           clients[0].send(turn_msg)

       your_turn_msg = str.encode("Your turn")
       clients[player_index].send(your_turn_msg)
       data = clients[player_index].recv(1024)
       if data != b'':
            data_decoded = data.decode()
            if data_decoded == "exit":
                exit_msg = str.encode("exit")
                clients[0].send(exit_msg)
                clients[1].send(exit_msg)
                print("Agent wants to end the game.")
                print("Connection closed")
                break

            if data_decoded == "Win":
                if player_index:
                    print("Black player won")
                else:
                    print("White player won")
                exit_msg = str.encode("exit")
                clients[0].send(exit_msg)
                clients[1].send(exit_msg)
                break

            data = data  # already in bytes
            msg = data
            # Alternate turn
            player_index = not player_index
            clients[player_index].send(msg)
    break
