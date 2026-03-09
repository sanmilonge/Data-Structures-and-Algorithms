checkerPieces = {
    "b": "●",   # player piece
    "B": "⬤",   # player king
    "c": "○",   # AI piece/opponent
    "C": "◯",   # AI king
    ".": "·"    # empty square
    }

board_size = 8

def render_cell(cell): 
    '''
    Converts the internal representation of the board to a human-readable format
    @param cell: A character representing the state of a cell on the board
    '''
    return checkerPieces[cell]

class Board:
    '''
    Represents the game board and contains methods for initializing the board, printing it, 
    and calculating valid moves and captures for pieces.
    '''
    def __init__(self):
        '''
        Initializes the board as an 8x8 grid filled with "." to represent empty squares, 
        and then sets up the pieces in their starting positions using the setup_pieces method.
        @return: None
        '''
        self.board = []

        for row in range(board_size):
            new_row = []
            for col in range(board_size):
                new_row.append(".")
            self.board.append(new_row)

        self.setup_pieces()

    # def print_board(self):
    #     '''
    #     Prints the current state of the board to the console in a human-readable format.
    #     @return: None
    #     '''
    #     print("  ", end="  ")
    #     for col in range(board_size):
    #         print(col + 1, end="  ")
    #     print()

    #     for row in range(board_size):
    #         print(row + 1, end="   ")
    #         for col in range(board_size): 
    #             cell = self.board[row][col]
    #             print(render_cell(cell), end="  ")
    #         print()
    def print_board(self):
        print("    ", end="")
        for col in range(board_size):
            print(f"{col+1:^4}", end="")
        print()

        border = "   +" + "---+" * board_size
        print(border)

        for row in range(board_size):
            print(f"{row+1:<2} |", end="")

            for col in range(board_size):
                cell = self.board[row][col]
                print(f" {render_cell(cell)} |", end="")

            print()
            print(border)

    def setup_pieces(self):
        '''
        Initializes the board with pieces in their starting positions. The top three rows are filled with "c" (AI pieces) 
        and the bottom three rows are filled with "b" (player pieces), placed on alternating squares.
        @return: None
        '''
        for row in range(board_size):
            for col in range(board_size):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = "c"
                    elif row > 4:
                        self.board[row][col] = "b"


    def get_moves(self, row, col):
        '''
        Calculates the valid moves for a piece located at the specified row and column. 
        The valid moves depend on the type of piece (regular or king) and its color (player or AI). 
        Regular pieces can only move forward diagonally, while kings can move in both directions. 
        The method checks for empty squares in the appropriate directions to determine valid moves.
        @param row: The row index of the piece for which to calculate moves
        @param col: The column index of the piece for which to calculate moves
        @return: A list of valid move positions (row, col) for the specified piece
        '''
        player_moves = [(-1,-1), (-1,1,)]
        ai_moves = [(1,1), (1,-1)]
        square = self.board[row][col]
        moves = []
        if square == ".":
            return []
        else:
            if square == "b":
                for dr, dc in player_moves:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < board_size and 0 <= c < board_size and self.board[r][c] == ".":
                        moves.append((r,c))
            elif square == "c":
                for dr, dc in ai_moves:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < board_size and 0 <= c < board_size and self.board[r][c] == ".":
                        moves.append((r,c))
            elif square == "B" or square == "C":
                for dr, dc in player_moves + ai_moves:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < board_size and 0 <= c < board_size and self.board[r][c] == ".":
                        moves.append((r,c))
        return moves
    
    def captures(self, row, col):
        '''
        Determines the valid capture moves for a piece located at the specified row and column. 
        A capture move involves jumping over an opponent's piece to an empty square directly beyond it. 
        The method checks for opponent pieces in the appropriate directions and ensures that the landing square 
        is empty to determine valid captures.
        @param row: The row index of the piece for which to calculate captures
        @param col: The column index of the piece for which to calculate captures
        @return: A list of valid capture move positions (row, col) for the specified piece
        '''
        player_moves = [(-1,-1), (-1,1,)]
        ai_moves = [(1,1), (1,-1)]
        square = self.board[row][col]
        captures = []

        if square == ".":
            return captures
        
        elif square == "b":
            directions = player_moves
            enemies = ("c", "C")
        elif square == "c":
            directions = ai_moves
            enemies = ("b", "B")
        elif square == "C":
            directions = ai_moves + player_moves
            enemies = ("b", "B")
        elif square == "B":
            directions = ai_moves + player_moves
            enemies = ("c", "C")
        else:
            return captures
        
        for dr, dc in directions:
            enemy_row = row + dr
            enemy_col = col + dc
            landing_row = row + 2 * dr
            landing_col = col + 2 * dc

            if (
                0 <= enemy_row < board_size
                and 0 <= enemy_col < board_size
                and 0 <= landing_row < board_size
                and 0 <= landing_col < board_size
            ):
                
                if (
                    self.board[enemy_row][enemy_col] in enemies 
                    and self.board[landing_row][landing_col] == "."
                ):
                    captures.append((landing_row, landing_col))
        return captures
                
    def get_available_moves(self, row, col):
        '''
        Returns valid moves for a specific piece.
        If piece cannot capture, it only returns regular diagonal moves
        @param row: The row index of the piece for which to calculate available moves
        @param col: The column index of the piece for which to calculate available moves
        @return: A list of valid move positions (row, col) for the specified piece, including 
        both regular moves and captures
        '''
        captures = self.captures(row, col)
        if captures:
            return captures
        else:
            return self.get_moves(row, col)

    def make_move(self, start_row, start_col, end_row, end_col):
        """
        Moves a piece from (start_row, start_col) to (end_row, end_col) on the
        board, handles captures and promotion, and returns True if the move is
        valid, False otherwise.
        @param start_row: The row index of the piece to move
        @param start_col: The column index of the piece to move
        @param end_row: The row index of the destination square
        @param end_col: The column index of the destination square
        @return: True if the move was successfully made, False if the move was invalid
        """
        piece = self.board[start_row][start_col]
        legal_moves = self.get_available_moves(start_row, start_col)
        if (end_row, end_col) not in legal_moves:
            print("Invalid move. Please choose a valid move for the selected piece.")
            return False
        if piece == ".":
            return False
        else:
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = "."
            if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
                captured_row = (start_row + end_row) // 2
                captured_col = (start_col + end_col) // 2
                self.board[captured_row][captured_col] = "."
            if piece == "b" and end_row == 0:
                self.board[end_row][end_col] = "B"
            elif piece == "c" and end_row == board_size - 1:
                self.board[end_row][end_col] = "C"
            return True
    def check_winner(self):
        '''
        Checks for a winner by counting the remaining pieces for both the player and the AI.
        If one side has no pieces left, the other side is declared the winner.
        @return: A string indicating the winner ("Player wins!" or "AI wins!") or None if there is no winner yet
        '''
        player_pieces = sum(row.count("b") + row.count("B") for row in self.board)
        ai_pieces = sum(row.count("c") + row.count("C") for row in self.board)

        if player_pieces == 0:
            return "AI wins!"
        elif ai_pieces == 0:
            return "Player wins!"
        else:
            return None