import pygame


def flip_board(board):
    flipped_board = []
    for i in range(len(board) - 1, -1, -1):
        flipped_board.append(board[i])
    return flipped_board


def draw_pointer(x, color, window):
    pygame.draw.circle(window, color, (x, 30), 28)


def draw_board(board, current_col, window, mouse_col, winner):
    pygame.draw.rect(window, (0, 0, 255),
                     (0, 60, len(board[0]) * 60, len(board) * 60))
    if current_col and winner is None:
        pygame.draw.rect(window, (70, 70, 255),
                         (mouse_col * 60, 60, 60, len(board) * 60))
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                pygame.draw.circle(window, (0, 0, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 1:
                pygame.draw.circle(window, (255, 0, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 2:
                pygame.draw.circle(window, (255, 255, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)