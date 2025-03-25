import time
import math
import copy

# Constants for evaluation weights and infinity.
INFINITY = float('inf')
MATERIAL_WEIGHT = 10      # Weight for material (pawn count)
ADVANCEMENT_WEIGHT = 1    # Weight for pawn advancement
MOBILITY_WEIGHT = 5       # Weight for mobility (number of legal moves)

# Transposition table for caching evaluations.
transposition_table = {}

def board_to_key(board_obj):
    #Convert the board's state (board_obj.boardArray) into a hashable tuple.
    return tuple(tuple(row) for row in board_obj.boardArray)

def evaluate(board_obj):
    #Static evaluation function for the board.

    if board_obj.gameOver:
        if board_obj.winner == 'W':
            return INFINITY
        elif board_obj.winner == 'B':
            return -INFINITY
        else:
            return 0

    white_material = 0
    black_material = 0
    white_advancement = 0
    black_advancement = 0
    white_moves = 0
    black_moves = 0

    for row in range(8):
        for col in range(8):
            piece = board_obj.boardArray[row][col]
            if piece == 'W':
                white_material += 1
                # For White: higher row index means closer to promotion.
                white_advancement += row  
                moves = board_obj.generate_moves_for_pawn(row, col)
                white_moves += len(moves)
            elif piece == 'B':
                black_material += 1
                # For Black: measure advancement from the other side.
                black_advancement += (7 - row)
                moves = board_obj.generate_moves_for_pawn(row, col)
                black_moves += len(moves)

    material_score = MATERIAL_WEIGHT * (white_material - black_material)
    advancement_score = ADVANCEMENT_WEIGHT * (white_advancement - black_advancement)
    mobility_score = MOBILITY_WEIGHT * (white_moves - black_moves)
    
    score = material_score + advancement_score + mobility_score
    return score

def generate_all_moves(board_obj, player):
    #Generate all legal moves for the given player ('W' for white, 'B' for black)
    #by scanning the board and calling board_obj.generate_moves_for_pawn for each pawn.
    moves = []
    for row in range(8):
        for col in range(8):
            if board_obj.boardArray[row][col] == player:
                moves.extend(board_obj.generate_moves_for_pawn(row, col))
    return moves

def simulate_move(board_obj, move):
    # Returns a deep copy of board_obj after applying the given move.
    new_board = copy.deepcopy(board_obj)
    new_board.apply_move(move)
    return new_board

def minimax(board_obj, depth, alpha, beta, maximizing_player, start_time, time_limit):
    # Minimax search with alpha–beta pruning.
    
    # Check time limit
    if time.time() - start_time > time_limit:
        raise TimeoutError

    # Terminal or depth limit: use evaluation function.
    if depth == 0 or board_obj.gameOver:
        return evaluate(board_obj), None

    board_key = board_to_key(board_obj)
    if board_key in transposition_table and transposition_table[board_key]['depth'] >= depth:
        cached = transposition_table[board_key]
        return cached['value'], cached['move']

    best_move = None
    if maximizing_player:
        max_eval = -INFINITY
        moves = generate_all_moves(board_obj, 'W')
        for move in moves:
            new_board = simulate_move(board_obj, move)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False, start_time, time_limit)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff.
        value = max_eval
    else:
        min_eval = INFINITY
        moves = generate_all_moves(board_obj, 'B')
        for move in moves:
            new_board = simulate_move(board_obj, move)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True, start_time, time_limit)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff.
        value = min_eval

    transposition_table[board_key] = {'value': value, 'move': best_move, 'depth': depth}
    return value, best_move

def iterative_deepening(board_obj, max_depth, time_limit, maximizing_player):
    # Run iterative deepening search with the minimax algorithm until the time limit is reached.
    start_time = time.time()
    best_move = None
    current_depth = 1
    while current_depth <= max_depth:
        try:
            score, move = minimax(board_obj, current_depth, -INFINITY, INFINITY, maximizing_player, start_time, time_limit)
            best_move = move
            current_depth += 1
        except TimeoutError:
            break
    return best_move


