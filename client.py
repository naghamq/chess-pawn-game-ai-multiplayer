import pygame
from board import ChessBoard
from UserInterface import UserInterface
from ai_agent import iterative_deepening
import socket
import select

# Global variables
UI = None
Board = None
ai_controlled = False  # True if AI controls White
color = None  # "W" or "B"
time_limit = None  # in seconds

# Helper function for custom setup
def apply_custom_setup(board, setup_str):
    if setup_str.startswith("Setup "):
        setup_str = setup_str[6:]
    board.ChessBoard = [[' ' for _ in range(8)] for _ in range(8)]
    tokens = setup_str.split()
    for token in tokens:
        if len(token) != 3:
            continue
        piece = token[0]
        col = ord(token[1].lower()) - ord('a')
        row = int(token[2]) - 1
        board.ChessBoard[row][col] = piece
    board.boardArray = board.ChessBoard

# Create a socket instance and connect to the server
socketObject = socket.socket()
socketObject.connect(("localhost", 9999))

# Function to drain incoming data (non-blocking)
def drain_incoming():
    global socketObject, UI
    if UI is None:
        return
    socketObject.setblocking(False)
    try:
        while True:
            chunk = socketObject.recv(1024)
            if not chunk:
                break
            data_str = chunk.decode()
            messages = data_str.split('\n')
            for msg in messages:
                msg = msg.strip()
                if not msg:
                    continue
                known_prefixes = ["Time", "Setup", "White", "Black", "exit", "Begin",
                                  "Classic", "Connected to the server", "Your turn",
                                  "White's turn", "Black's turn"]
                if any(msg.startswith(k) for k in known_prefixes) or msg in known_prefixes:
                    continue
                if len(msg) == 4:
                    try:
                        move = f"{8 - int(msg[1])}{ord(msg[0]) - 97}{8 - int(msg[3])}{ord(msg[2]) - 97}"
                        if abs(int(move[1]) - int(move[3])) == 2:
                            UI.chessboard.enpassant = True
                            UI.chessboard.enpassantCol = int(move[1])
                        UI.chessboard.changePerspective()
                        UI.chessboard.computeMove(move, 0)
                        UI.chessboard.changePerspective()
                        UI.drawComponent()
                    except Exception:
                        pass
    except (BlockingIOError, socket.error):
        pass
    finally:
        socketObject.setblocking(True)

# Main loop to read messages from the server
while True:
    data = socketObject.recv(1024).decode()

    if UI and UI.chessboard and UI.chessboard.gameOver:
        if data in ["Your turn", "White's turn", "Black's turn"]:
            continue
    print(data)

    if data.startswith("Time"):
        time_limit = int(data[4:]) * 60

    elif data.startswith("Setup"):
        apply_custom_setup(Board, data)
        UI.drawComponent()

    elif data == "Classic":
        UI.drawComponent()

    elif data == "White":
        color = "W"
        if UI:
            UI.playerColor = color
            UI.chessboard.set_player_color(color)

    elif data == "Black":
        color = "B"
        if UI:
            UI.playerColor = color
            UI.chessboard.set_player_color(color)

    elif data == "exit":
        print("Connection closed")
        break

    elif data == "Your turn":
        if (ai_controlled):
            if(color == "W"):
                ai_move = iterative_deepening(UI.chessboard, max_depth=3, time_limit=5, maximizing_player = True)
            else:
                ai_move = iterative_deepening(UI.chessboard, max_depth=3, time_limit=5, maximizing_player = False)
            if ai_move is None:
                print("AI could not find a valid move!")
                continue
            
            move = f"{chr(97 + ai_move[1])}{8 - ai_move[0]}{chr(97 + ai_move[3])}{8 - ai_move[2]}"
            local_move_str = f"{ai_move[0]}{ai_move[1]}{ai_move[2]}{ai_move[3]}"
            valid = UI.computeMove(local_move_str, 0)
            if not valid:
                drain_incoming()
                continue
            UI.drawComponent()
            msg_to_send = move
        else:
            while True:
                data_tuple, flag = UI.clientMove()
                if flag in [-1, 1]:
                    msg_to_send = "Win" if flag == -1 else "Lost"
                    break
                else:
                    move = f"{chr(97 + int(data_tuple[1]))}{8 - int(data_tuple[0])}{chr(97 + int(data_tuple[3]))}{8 - int(data_tuple[2])}"
                    local_move_str = f"{data_tuple[0]}{data_tuple[1]}{data_tuple[2]}{data_tuple[3]}"
                    valid = UI.computeMove(local_move_str, 0)
                    if not valid:
                        drain_incoming()
                        continue
                    UI.drawComponent()
                    msg_to_send = move
                    break
        socketObject.send(msg_to_send.encode())

    elif data == "Begin":
        pygame.init()
        surface = pygame.display.set_mode([600, 600], 0, 0)
        pygame.display.set_caption('Pawn Game')
        Board = ChessBoard()
        UI = UserInterface(surface, Board)
        UI.time = time_limit
        UI.chessboard.round = int(time_limit / 14)

        print("Select move mode:")
        print("1. AI")
        print("2. Human")
        mode = input("Enter option (1 for AI, 2 for Human): ").strip()
        if mode == "1":
            ai_controlled = True

    elif data in ["White's turn", "Black's turn"]:
        pass

    elif data == "Connected to the server":
        continue

    else:
        move = f"{8 - int(data[1])}{ord(data[0]) - 97}{8 - int(data[3])}{ord(data[2]) - 97}"
        if abs(int(move[1]) - int(move[3])) == 2:
            UI.chessboard.enpassant = True
            UI.chessboard.enpassantCol = int(move[1])
        UI.chessboard.changePerspective()
        UI.chessboard.computeMove(move, 0)
        UI.chessboard.changePerspective()
        UI.drawComponent()

socketObject.close()
