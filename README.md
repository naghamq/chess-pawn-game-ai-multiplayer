# Chess Pawn Game with AI and Network Multiplayer (WIP)

## Description
An in-progress Python project simulating a chess-inspired pawn game with an AI opponent (using minimax with iterative deepening and alpha–beta pruning), a Pygame GUI, and socket-based multiplayer via a client–server model. Future work includes refining the AI and expanding features.

## Features
- **AI Opponent:** Implements a minimax algorithm with iterative deepening and alpha–beta pruning.
- **Graphical Interface:** Built using Pygame for a dynamic game board.
- **Networking:** Utilizes a socket-based client–server architecture for real-time multiplayer gameplay.
- **Custom Board Setup:** Supports both classic and customizable board configurations.

## Prerequisites
- Python 3.x
- Pygame (Install via `pip install pygame`)
- Standard libraries: `socket`, `copy`, `math`, etc.
- (Tkinter is used in the server for some UI elements and typically comes pre-installed with Python.)

## Installation

### 1. Clone the Repository:
```bash
git clone https://github.com/yourusername/chess-pawn-game-ai-multiplayer.git
```

### 2. Navigate to the Project Directory:
```bash
cd chess-pawn-game-ai-multiplayer
```

### 3. (Optional) Create and Activate a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies:
```bash
pip install pygame
```

## Running the Project

### Server Setup
1. Open a terminal and navigate to the project directory.
2. Run the server script:
```bash
python server.py
```
3. Follow the on-screen prompts:
   - **Enter the game time (in minutes):**
     Example: Type `Time 10` if you want a 10-minute game.
   - **Type "Begin" to start the game:**
     Example: Type `Begin` (case sensitive) when prompted.
   - **Choose a board setup option:**
     - For a standard board, type: `Classic`
     - For a custom board setup, type: `Setup` and then when prompted, provide a custom setup string.
     Example: Type `Setup Wb4 Wa3 Wc2 Bg7` to place a White pawn at b4, a White pawn at a3, a White pawn at c2, and a Black pawn at g7.

### Client Setup
1. Open a new terminal window (or use a separate machine).
2. Run the client script:
```bash
python client.py
```
3. The client will connect to the server automatically.
4. When the game begins, a Pygame window will open.
5. Select the move mode when prompted:
   - **AI Mode:** The computer will play moves.
   - **Human Mode:** You can make moves by clicking the game board.

**Note:** To test multiplayer functionality on a single machine, run two instances of the client.

## How to Play
- **Human Mode:** Click on your pawn to select the source square, then click on the destination square to make a move.
- **AI Mode:** The AI will compute and perform its move automatically when it's its turn.

The server handles the turn order and relays messages between clients.

## Future Work
- Enhance AI decision-making and performance.
- Improve error handling and user input validation.
- Expand game functionalities with additional chess rules and features.


