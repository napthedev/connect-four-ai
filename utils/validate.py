def is_available_col(board, col):
    return board[5][col] == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(len(board[0])):
        if is_available_col(board, col):
            valid_locations.append(col)
    return valid_locations


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