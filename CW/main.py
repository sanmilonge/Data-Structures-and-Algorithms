from board import Board
import utility as t

board_size = 8
players_turn = True
forced_capture = False
is_AI_mode = True
player1 = "Player 1"
player2 = "AI"

game = Board(board_size=board_size, forced_capture=forced_capture)

t.typewriter("Welcome to Checkers!\n")
t.wait(2)
t.typewriter("Enter your name\nPlayer 1: ")
player1 = input()
if is_AI_mode:
    t.typewriter("Player 2: ")
    player2 = input()
    t.wait()

t.typewriter(f"\n\n                 {player1} vs {player2}                   \n\n")
t.wait(2)

game.print_board()

while True:
    try:
        current_player = "b" if players_turn else "c"
        current_name = player1 if players_turn else player2

        t.typewriter(f"{current_name}'s turn\n")

        all_moves = game.get_all_moves(current_player)

        if not all_moves:
            winner = "c" if current_player == "b" else "b"
            if winner == "b":
                t.typewriter(f"{player1} wins!\n")
            else:
                t.typewriter(f"{player2} wins!\n")
            break
        
        t.typewriter("Enter the row of the piece you want to move (from the side of the board): ")
        start_row = int(input()) - 1
        t.typewriter("Enter the column of the piece you want to move (from the top of the board): ")
        start_col = int(input()) - 1

        if not (0 <= start_row < board_size and 0 <= start_col < board_size):
            t.typewriter("Invalid coordinates. Please choose a square on the board.\n")
            continue

        square = game.board[start_row][start_col]

        if square == "." or square.lower() != current_player:
            t.typewriter("Invalid piece. Please input the coordinates for one of your pieces.\n")
            continue

        if (start_row, start_col) not in all_moves:
            t.typewriter("That piece cannot be moved right now.\n")
            if forced_capture and game.has_capture(current_player):
                t.typewriter("A capture is available, so you must choose a capturing piece.\n")
            continue

        available_moves = all_moves[(start_row, start_col)]

        ("Available moves:")
        for move_row, move_col in available_moves:
            t.typewriter(f"({move_row + 1}, {move_col + 1})\n")

        end_row = int(input("Enter the row of the square you want to move to (from the side of the board): ")) - 1
        end_col = int(input("Enter the column of the square you want to move to (from the top of the board): ")) - 1

        if not (0 <= end_row < board_size and 0 <= end_col < board_size):
            t.typewriter("Invalid destination. Please choose a square on the board.\n")
            continue

        if (end_row, end_col) not in available_moves:
            t.typewriter("Invalid move. Please choose a valid move for the selected piece.\n")
            continue

        moved = game.make_move(start_row, start_col, end_row, end_col)
        if not moved:
            t.typewriter("Move could not be completed.\n")
            continue

        game.print_board()

        was_capture = abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2

        if was_capture:
            current_row, current_col = end_row, end_col

            while True:
                extra_captures = game.captures(current_row, current_col)

                if not extra_captures:
                    break

                t.typewriter("Multi-jump available. You must continue capturing with the same piece.\n")
                t.typewriter("Available capture moves:")
                for move_row, move_col in extra_captures:
                    t.typewriter(f"({move_row + 1}, {move_col + 1})")

                t.typewriter("Enter the next capture row: ")
                next_row = int(input()) - 1
                t.typewriter("Enter the next capture column: ")
                next_col = int(input()) - 1

                if not (0 <= next_row < board_size and 0 <= next_col < board_size):
                    t.typewriter("Invalid destination. Please choose a square on the board.\n")
                    continue

                if (next_row, next_col) not in extra_captures:
                    t.typewriter("Invalid capture. You must choose one of the listed capture moves.\n")
                    continue

                moved = game.make_move(current_row, current_col, next_row, next_col)
                if not moved:
                    t.typewriter("Move could not be completed.\n")
                    continue

                current_row, current_col = next_row, next_col
                game.print_board()

        winner = game.check_winner()
        if winner == "b":
            t.typewriter(f"{player1} wins!")
            break
        elif winner == "c":
            t.typewriter(f"{player2} wins!")
            break

        players_turn = not players_turn

    except KeyboardInterrupt:
        t.typewriter("\nGame interrupted. Exiting...")
        break
    except ValueError:
        t.typewriter("Invalid input. Please enter numeric values for rows and columns.\n")
        continue