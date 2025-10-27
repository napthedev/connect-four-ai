def drop_piece(board, col, piece):
    for row in range(len(board)):
        if board[row][col] == 0:
            board[row][col] = piece
            break