class ChessBoard:
    def __init__(self):
        #8x8 board with:
        #  - row 0 at bottom, row 7 at top
        #  - White pawns on row 1, Black pawns on row 6
        self.ChessBoard = [[' ' for _ in range(8)] for _ in range(8)]
        for col in range(8):
            self.ChessBoard[1][col] = 'W'
            self.ChessBoard[6][col] = 'B'

        self.boardArray = self.ChessBoard
        self.round = 0
        self.en_passant_target = None
        self.is_black = False

        # Tracks if the game is over and who won
        self.gameOver = False
        self.winner = None
        self.game_over_printed = False  # New flag to prevent repeated printing

    def set_player_color(self, color):
        self.is_black = (color == 'B')

    def changePerspective(self):
        # No internal flipping; the UI handles orientation
        pass

    def computeMove(self, move, flag):
        #move is a 4-char string: 'src_row src_col dst_row dst_col' (0..7).
        if len(move) != 4:
            return False
        try:
            src_row = int(move[0])
            src_col = int(move[1])
            dst_row = int(move[2])
            dst_col = int(move[3])
        except ValueError:
            print("Error parsing move.")
            return False
        return self.apply_move((src_row, src_col, dst_row, dst_col))

    def generate_moves_for_pawn(self, row, col):
        #Returns valid moves for the pawn at (row,col).
        #Follows standard chess-pawn rules (1-step, 2-step from start, diagonal capture, en passant).
        moves = []
        piece = self.ChessBoard[row][col]
        if piece not in ['W', 'B']:
            return moves

        if piece == 'W':
            direction = 1
            start_row = 1
            opponent = 'B'
        else:
            direction = -1
            start_row = 6
            opponent = 'W'

        new_row = row + direction
        # One-step forward
        if 0 <= new_row < 8 and self.ChessBoard[new_row][col] == ' ':
            moves.append((row, col, new_row, col))
            # Two-step if at starting row
            if row == start_row:
                new_row2 = row + 2 * direction
                if 0 <= new_row2 < 8 and self.ChessBoard[new_row2][col] == ' ':
                    moves.append((row, col, new_row2, col))

        # Diagonal captures & en passant
        for d_col in [-1, 1]:
            new_col = col + d_col
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                # Normal capture
                if self.ChessBoard[new_row][new_col] == opponent:
                    moves.append((row, col, new_row, new_col))
                # En passant
                if self.en_passant_target == (new_row, new_col):
                    moves.append((row, col, new_row, new_col))

        return moves

    def is_valid_move(self, move):
        return move in self.generate_moves_for_pawn(move[0], move[1])

    def apply_move(self, move):
        #Applies the move if valid, sets en passant target if needed,
        #then checks if game is over. Does NOT exit or send 'exit'.
        
        # If already over, print game over message only once
        if self.gameOver:
            if not self.game_over_printed:
                print(f"Game Over! Winner: {self.winner}")
                self.game_over_printed = True
            return False

        if not self.is_valid_move(move):
            print("Invalid move!")
            return False

        src_row, src_col, dst_row, dst_col = move
        piece = self.ChessBoard[src_row][src_col]

        # Move the pawn
        self.ChessBoard[dst_row][dst_col] = piece
        self.ChessBoard[src_row][src_col] = ' '

        # Two-step => en passant target
        if piece == 'W' and src_row == 1 and dst_row == 3:
            self.en_passant_target = (2, src_col)
        elif piece == 'B' and src_row == 6 and dst_row == 4:
            self.en_passant_target = (5, src_col)
        else:
            self.en_passant_target = None

        self.boardArray = self.ChessBoard

        # Check if game is over
        over, winner = self.check_game_over()
        if over:
            self.gameOver = True
            self.winner = winner
            if not self.game_over_printed:
                print(f"Game Over! Winner: {winner}")
                self.game_over_printed = True

        return True

    def check_game_over(self):
        # Pawn reaches last row = immediate win
        # All opponent pawns captured = immediate win
        # Opponent has no moves = immediate win
        white_exists = False
        black_exists = False
        for r in range(8):
            for c in range(8):
                p = self.ChessBoard[r][c]
                if p == 'W':
                    white_exists = True
                    if r == 7:  # White reached last row
                        return (True, 'W')
                elif p == 'B':
                    black_exists = True
                    if r == 0:  # Black reached last row (first row)
                        return (True, 'B')

        if not white_exists:
            return (True, 'B')
        if not black_exists:
            return (True, 'W')

        white_moves = []
        black_moves = []
        for r in range(8):
            for c in range(8):
                p = self.ChessBoard[r][c]
                if p == 'W':
                    white_moves += self.generate_moves_for_pawn(r, c)
                elif p == 'B':
                    black_moves += self.generate_moves_for_pawn(r, c)

        if not white_moves:
            return (True, 'B')
        if not black_moves:
            return (True, 'W')

        return (False, None)
