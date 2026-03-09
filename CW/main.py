from board import Board

game = Board()
game.print_board()
players_turn = True
forced_capture = False
while True:
    try:
        if players_turn:
            print("Player's turn")
            start_row = int(input("Enter the row of the piece you want to move (from the side of the board): ")) - 1
            start_col = int(input("Enter the column of the piece you want to move (from the top of the board): ")) - 1
            square = game.board[start_row][start_col]
            if square.lower() != 'b':
                print("Invalid piece. Please input the coordinates for one of your pieces.")
                continue
        else:
            print("Opponent's turn")
            start_row = int(input("Enter the row of the piece you want to move (from the side of the board): ")) - 1
            start_col = int(input("Enter the column of the piece you want to move (from the top of the board): ")) - 1
            square = game.board[start_row][start_col]
            if square.lower() != 'c':
                print("Invalid piece. Please input the coordinates for one of your pieces.")
                continue
        available_moves = game.get_available_moves(start_row, start_col)
        if not available_moves:
            print("No available moves for this piece. Please choose another piece.")
            continue
        end_row = int(input("Enter the row of the square you want to move to (from the side of the board): ")) - 1
        end_col = int(input("Enter the column of the square you want to move to (from the top of the board): ")) - 1
        if end_col == 100 or end_row == 100:
            print("Exiting the game. Goodbye!")
            break
        if (end_row, end_col) not in available_moves:
            print("Invalid move. Please choose a valid move for the selected piece.")
            continue
        game.make_move(start_row, start_col, end_row, end_col)
        game.print_board()
        players_turn = not players_turn
        winner = game.check_winner()
        if winner:
            print(winner)
            break
    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting...")
        break
    except ValueError:
        print("Invalid input. Please enter numeric values for rows and columns.")
        continue