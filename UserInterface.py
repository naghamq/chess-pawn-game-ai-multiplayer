import pygame
from board import ChessBoard

class UserInterface:
    def __init__(self, surface, board):
        #Displays the board so that: - White sees row 0 at bottom, - Black sees row 0 at top
        self.surface = surface
        self.board = board
        self.chessboard = board
        self.playerColor = None
        self.time = None
        self.firstgame = True
        self.square_size = self.surface.get_width() // 8
        self.selected_square = None

    def drawComponent(self):
        self.surface.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 36)

        # Draw squares
        for draw_row in range(8):
            for col in range(8):
                color = (240, 217, 181) if ((draw_row + col) % 2 == 0) else (181, 136, 99)
                rect = (col * self.square_size, draw_row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.surface, color, rect)

        # Draw pieces
        for draw_row in range(8):
            for col in range(8):
                if self.playerColor == 'W':
                    board_row = 7 - draw_row
                else:
                    board_row = draw_row
                piece = self.board.boardArray[board_row][col]
                if piece != ' ':
                    text = font.render(piece, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(
                        col * self.square_size + self.square_size // 2,
                        draw_row * self.square_size + self.square_size // 2
                    ))
                    self.surface.blit(text, text_rect)
        pygame.display.flip()

    def clientMove(self):
        #Lets the user pick source & dest squares by clicking, If the board is over, returns a special signal ("game_over"),
        # instead of reprinting "Game Over! Winner: X".
        # Check before processing any clicks.
        if self.chessboard.gameOver:
            return "game_over", None

        source = None
        destination = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit", None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Re-check inside the loop.
                    if self.chessboard.gameOver:
                        return "game_over", None

                    x, y = event.pos
                    col = x // self.square_size
                    draw_row = y // self.square_size
                    if self.playerColor == 'W':
                        row_internal = 7 - draw_row
                    else:
                        row_internal = draw_row

                    piece = self.board.boardArray[row_internal][col]
                    if source is None:
                        if piece != self.playerColor:
                            print("Invalid selection. Pick your own pawn.")
                            continue
                        source = (row_internal, col)
                        print(f"Source selected: {source}")
                    else:
                        destination = (row_internal, col)
                        print(f"Destination selected: {destination}")
                        return (source[0], source[1], destination[0], destination[1]), None

    def computeMove(self, move, flag):
        return self.chessboard.computeMove(move, flag)

    def changePerspective(self):
        return self.chessboard.changePerspective()
