import math
import pygame
from .validate import get_valid_locations, check_winner
from .board import drop_piece
from .display import draw_board, flip_board


def evaluate_line_state(line, piece, opponent):
    score = 0
    if line.count(piece) == 3 and line.count(0) == 1:
        score += 500
    if line.count(piece) == 2 and line.count(0) == 2:
        score += 50

    if line.count(opponent) == 3 and line.count(0) == 1:
        score -= 300
    if line.count(opponent) == 2 and line.count(0) == 2:
        score -= 20

    return score


def evaluate_board_score(board, piece, opponent):
    total_score = 0

    # Horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            row_list = board[row][col:col + 4]
            total_score += evaluate_line_state(row_list, piece, opponent)

    # Vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            col_list = [board[row + i][col] for i in range(4)]
            total_score += evaluate_line_state(col_list, piece, opponent)

    # Back slash
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            back_slash_list = [
                board[row][col], board[row + 1][col + 1],
                board[row + 2][col + 2], board[row + 3][col + 3]
            ]
            total_score += evaluate_line_state(back_slash_list, piece, opponent)

    # Forward slash
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            forward_slash_list = [
                board[row][col], board[row - 1][col + 1],
                board[row - 2][col + 2], board[row - 3][col + 3]
            ]
            total_score += evaluate_line_state(forward_slash_list, piece, opponent)

    return total_score


def ai_move(board, piece, window):
    best_score = -math.inf
    best_col = len(board[0]) // 2
    valid_locations = get_valid_locations(board)
    pygame.draw.rect(window, (0, 0, 0), (0, 0, 420, 60))
    draw_board(flip_board(board), False, window, None, None)
    pygame.display.update()
    for col in valid_locations:
        drop_piece(board, col, piece)
        score = minimax(board, 3, False)
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] != 0:
                board[row][col] = 0
                break
        if col == len(board[0]) // 2:
            score += 250
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 1:
        return -10000000 - depth
    elif winner == 2:
        return 10000000000 + depth
    elif winner == "tie":
        return 0

    if depth <= 0:
        return evaluate_board_score(board, 2, 1) + depth

    if is_maximizing:
        best_score = -math.inf
        valid_locations = get_valid_locations(board)
        for col in valid_locations:
            drop_piece(board, col, 2)
            score = minimax(board, depth - 1, False)
            for row in range(len(board) - 1, -1, -1):
                if board[row][col] != 0:
                    board[row][col] = 0
                    break
            if score > best_score:
                best_score = score

        return best_score

    else:
        best_score = math.inf
        valid_locations = get_valid_locations(board)
        for col in valid_locations:
            drop_piece(board, col, 1)
            score = minimax(board, depth - 1, True)
            for row in range(len(board) - 1, -1, -1):
                if board[row][col] != 0:
                    board[row][col] = 0
                    break
            if score < best_score:
                best_score = score

        return best_score