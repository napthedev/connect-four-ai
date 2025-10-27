import pygame
import math


def main():
    game_board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    pygame.init()

    game_window = pygame.display.set_mode((len(game_board[0]) * 60, len(game_board) * 60 + 60))
    pygame.display.set_caption("Connect 4")

    game_clock = pygame.time.Clock()
    game_font = pygame.font.Font("freesansbold.ttf", 30)

    is_running = True
    mouse_x = 210
    turn_count = 1
    mouse_col = 3
    game_winner = None

    while is_running:
        game_window.fill((0, 0, 0))

        if turn_count % 2 == 0 and game_winner is None:
            mouse_col = ai_move(game_board, 2, game_window)
            if is_available_col(game_board, mouse_col):
                drop_piece(game_board, mouse_col, 2)
                turn_count += 1
                game_winner = check_winner(game_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_col = event.pos[0] // 60
                mouse_x = event.pos[0]
                if mouse_x < 30:
                    mouse_x = 30
                elif mouse_x > len(game_board[0]) * 60 - 30:
                    mouse_x = len(game_board[0]) * 60 - 30
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_col = event.pos[0] // 60
                if is_available_col(game_board, mouse_col) and game_winner is None:
                    if turn_count % 2 == 1:
                        drop_piece(game_board, mouse_col, 1)
                        turn_count += 1
                        game_winner = check_winner(game_board)

        draw_board(flip_board(game_board), True, game_window, mouse_col, game_winner)

        if game_winner is None:
            draw_pointer(mouse_x, (255, 0, 0), game_window)

        if game_winner is not None:
            if game_winner == 1:
                win_text = game_font.render(f"YOU WINS", True, (255, 0, 0))
            elif game_winner == 2:
                win_text = game_font.render(f"COMPUTER WINS", True, (255, 255, 0))
            elif game_winner == "tie":
                win_text = game_font.render(f"TIE", True, (255, 255, 255))
            win_text_rect = win_text.get_rect(center=(210, 30))
            game_window.blit(win_text, win_text_rect)

        game_clock.tick(24)
        pygame.display.update()


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


def is_available_col(board, col):
    return board[5][col] == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(len(board[0])):
        if is_available_col(board, col):
            valid_locations.append(col)
    return valid_locations


def drop_piece(board, col, piece):
    for row in range(len(board)):
        if board[row][col] == 0:
            board[row][col] = piece
            break


def check_winner(board):
    # Horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row][
                    col + 1] and board[row][col] == board[row][
                        col + 2] and board[row][col] == board[row][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            if board[row][col] == board[row + 1][col] and board[row][
                    col] == board[row + 2][col] and board[row][col] == board[
                        row + 3][col] and board[row][col] != 0:
                return board[row][col]

    # Forward slash
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row + 1][
                    col + 1] and board[row][col] == board[row + 2][
                        col + 2] and board[row][col] == board[row + 3][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Back slash
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row - 1][
                    col + 1] and board[row][col] == board[row - 2][
                        col + 2] and board[row][col] == board[row - 3][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Tie
    tie_count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                tie_count += 1
    if tie_count >= len(board) * len(board[0]):
        return "tie"

    return None


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
            total_score += evaluate_line_state(row_list, piece, opponent)

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


if __name__ == "__main__":
    main()
