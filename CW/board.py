checkerPieces = {
    "b": "●",   # player piece
    "B": "⬤",   # player king
    "c": "○",   # AI piece/opponent
    "C": "◯",   # AI king
    ".": "·"    # empty square
    }


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
    def __init__(self, board_size, forced_capture):
        '''
        Initializes the board as an 8x8 grid filled with "." to represent empty squares, 
        and then sets up the pieces in their starting positions using the setup_pieces method.
        @return: None
        '''
        self.board = []
        self.board_size = board_size
        self.forced_capture = forced_capture

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
        for col in range(self.board_size):
            print(f"{col+1:^4}", end="")
        print()

        border = "   +" + "---+" * self.board_size
        print(border)

        for row in range(self.board_size):
            print(f"{row+1:<2} |", end="")

            for col in range(self.board_size):
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
        for row in range(self.board_size):
            for col in range(self.board_size):
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
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == ".":
                        moves.append((r,c))
            elif square == "c":
                for dr, dc in ai_moves:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == ".":
                        moves.append((r,c))
            elif square == "B" or square == "C":
                for dr, dc in player_moves + ai_moves:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == ".":
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
                0 <= enemy_row < self.board_size
                and 0 <= enemy_col < self.board_size
                and 0 <= landing_row < self.board_size
                and 0 <= landing_col < self.board_size
            ):
                
                if (
                    self.board[enemy_row][enemy_col] in enemies 
                    and self.board[landing_row][landing_col] == "."
                ):
                    captures.append((landing_row, landing_col))
        return captures
                
    def get_available_moves(self, row, col):
        """
        Returns a list of available moves for the piece at the specified row and
        col. Prioritizes capture moves if any are possible; otherwise, returns
        standard moves.
        @param row: The row index of the piece for which to get available moves
        @param col: The column index of the piece for which to get available moves
        @return: A list of available move positions (row, col) for the specified piece
        """
        captures = self.captures(row, col)
        if captures:
            return captures
        else:
            return self.get_moves(row, col)

    def make_move(self, start_row, start_col, end_row, end_col):
        """
        Handles moving a piece on the board from (start_row, start_col) to
        (end_row, end_col), validating the move, updating the board, processing
        captures, and promoting pieces when applicable. Returns True if the move
        is successful, otherwise False.
        @param start_row: The starting row index of the piece to move
        @param start_col: The starting column index of the piece to move
        @param end_row: The destination row index for the piece to move
        @param end_col: The destination column index for the piece to move
        @return: True if the move was successful, False if the move was invalid
        """
        piece = self.board[start_row][start_col]

        if piece == ".":
            return False

        all_moves = self.get_all_moves(piece.lower())

        if (start_row, start_col) not in all_moves:
            print("That piece cannot be moved right now.")
            return False

        legal_moves = all_moves[(start_row, start_col)]

        if (end_row, end_col) not in legal_moves:
            print("Invalid move. Please choose a valid move for the selected piece.")
            return False

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            self.board[captured_row][captured_col] = "."

        if piece == "b" and end_row == 0:
            self.board[end_row][end_col] = "B"
        elif piece == "c" and end_row == self.board_size - 1:
            self.board[end_row][end_col] = "C"

        return True
    
    def check_winner(self):
        '''
        Checks for a winner by counting the remaining pieces for both the player and the AI, 
        and also checking if either player has no valid moves left. If one player has no pieces or no valid moves, 
        the other player is declared the winner.
        @return: A string indicating the winner ("b" or "c") or None if there is no winner yet
        '''
        player_pieces = sum(row.count("b") + row.count("B") for row in self.board)
        ai_pieces = sum(row.count("c") + row.count("C") for row in self.board)

        if player_pieces == 0:
            return "c"
        elif ai_pieces == 0:
            return "b"
        elif not self.get_all_moves("b"):
            return "c"
        elif not self.get_all_moves("c"):
            return "b"
        else:
            return None

    def get_all_moves(self, player):
        all_moves = {}
        capture_moves = {}

        for row in range(self.board_size):
            for col in range(self.board_size):
                square = self.board[row][col]

                if square != "." and square.lower() == player:
                    piece_moves = self.get_moves(row, col)
                    piece_captures = self.captures(row, col)

                    moves = piece_moves + piece_captures
                    if moves:
                        all_moves[(row, col)] = moves

                    if piece_captures:
                        capture_moves[(row, col)] = piece_captures

        if self.forced_capture and capture_moves:
            return capture_moves

        return all_moves
    
    def has_capture(self, player):
        for row in range(self.board_size):
            for col in range(self.board_size):
                square = self.board[row][col]
                if square != "." and square.lower() == player:
                    if self.captures(row, col):
                        return True
        return False