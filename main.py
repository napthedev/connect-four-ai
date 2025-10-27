import pygame
from utils.ai import ai_move
from utils.validate import is_available_col, check_winner
from utils.board import drop_piece
from utils.display import draw_board, draw_pointer, flip_board


def main():
    game_board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

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

if __name__ == "__main__":
    main()
