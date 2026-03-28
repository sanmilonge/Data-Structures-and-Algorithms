checkerPieces = {
    "b": "●",   # player piece
    "B": "⬤",   # player king
    "c": "○",   # AI piece
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
        self.board = []
        self.board_size = board_size
        self.forced_capture = forced_capture

        for row in range(board_size):
            new_row = []
            for col in range(board_size):
                new_row.append(".")
            self.board.append(new_row)

        self.setup_pieces()


    def print_board(self, game, highlight=None):
        """
        Prints the board with row/col labels and Unicode pieces.
        highlight: a (row, col) to mark with brackets e.g. [●] — used in history mode.
        """
        size = game.board_size
        print()
        print("    " + "   ".join(str(c + 1) for c in range(size)))
        border = "   +" + "---+" * size
        print(border)
        for r in range(size):
            row_str = f"{r + 1:<2} |"
            for c in range(size):
                symbol = render_cell(game.board[r][c])
                if highlight == (r, c):
                    row_str += f"[{symbol}]|"
                else:
                    row_str += f" {symbol} |"
            print(row_str)
            print(border)
        print()

    def setup_pieces(self):
        """
        Initializes the board by placing "c" and "b" pieces on alternating
        squares in the starting rows for each player, based on the board size.
        @return: None
        """
        rows_of_pieces = (self.board_size // 2) - 1 # Number of rows to fill with pieces for each player

        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    if row < rows_of_pieces:
                        self.board[row][col] = "c"
                    elif row >= self.board_size - rows_of_pieces:
                        self.board[row][col] = "b"


    def get_moves(self, row, col):
        """
        Returns a list of valid move positions for the piece at the specified
        row and col on the board, based on the piece type and board boundaries.
        @param row: The row index of the piece to check for moves
        @param col: The column index of the piece to check for moves
        @return: A list of tuples representing valid move coordinates for the piece at (row, col)
        """
        player_moves = [(-1,-1), (-1,1,)]
        ai_moves = [(1,1), (1,-1)] # Directions pieces can move in: player pieces move up the board (negative row direction), AI pieces move down (positive row direction)
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
        """
        Returns a list of valid capture moves for the piece at the specified row
        and col on the board, based on the piece type and its allowed
        directions. Each capture is represented as a tuple of landing
        coordinates.
        @param row: The row index of the piece to check for captures
        @param col: The column index of the piece to check for captures
        @return: A list of tuples, where each tuple is (landing_row, landing_col) representing a 
        valid capture move for the piece at (row, col)
        """
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
                
    # def get_available_moves(self, row, col):
    #     """
    #     Returns a list of available moves for the piece at the specified row and
    #     col. Prioritizes capture moves if available; otherwise, returns standard
    #     moves.
    #     @param row: The row index of the piece to check for moves
    #     @param col: The column index of the piece to check for moves
    #     @return: A list of tuples representing valid move coordinates for the piece at (row, col)
    #     """
    #     captures = self.captures(row, col)
    #     if captures:
    #         return captures
    #     else:
    #         return self.get_moves(row, col)

    def make_move(self, start_row, start_col, end_row, end_col):
        """
        Executes a single move or single capture hop on the board.
        Does not enforce turn order or multi-jump chaining — callers handle that.
        @param start_row: The starting row index of the piece being moved
        @param start_col: The starting column index of the piece being moved
        @param end_row: The ending row index where the piece will land
        @param end_col: The ending column index where the piece will land
        @return: True if the move was successfully made, False if the move was invalid
        """
        piece = self.board[start_row][start_col]

        if piece == ".":
            return False

        all_moves = self.get_all_moves(piece.lower())

        if (start_row, start_col) not in all_moves:
            return False

        legal_moves = all_moves[(start_row, start_col)]

        if (end_row, end_col) not in legal_moves:
            return False

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        # Removes captured piece if this was a jump
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2: 
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            self.board[captured_row][captured_col] = "."

        # Promotion
        if piece == "b" and end_row == 0:
            self.board[end_row][end_col] = "B"
        elif piece == "c" and end_row == self.board_size - 1:
            self.board[end_row][end_col] = "C"

        return True

    def make_move_no_validate(self, start_row, start_col, end_row, end_col):
        """
        Executes a single hop without full move validation.
        Used internally by get_all_jump_chains to simulate chains efficiently.
        Assumes the move is already known to be a valid capture hop.
        Returns the captured piece's position.
        @param start_row: The starting row index of the piece being moved
        @param start_col: The starting column index of the piece being moved
        @param end_row: The ending row index where the piece will land
        @param end_col: The ending column index where the piece will land
        @return: A tuple (captured_row, captured_col, captured_piece) representing the position 
        and type of the piece that was captured
        """
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        captured_row = (start_row + end_row) // 2
        captured_col = (start_col + end_col) // 2
        captured_piece = self.board[captured_row][captured_col]
        self.board[captured_row][captured_col] = "."

        # Promotion
        if piece == "b" and end_row == 0:
            self.board[end_row][end_col] = "B"
        elif piece == "c" and end_row == self.board_size - 1:
            self.board[end_row][end_col] = "C"

        return captured_row, captured_col, captured_piece

    def get_jump_chains(self, row, col, chain_so_far=None, captured_so_far=None):
        """
        Recursively finds all complete capture chains starting from (row, col).
        Returns a list of chains, where each chain is a list of (row, col) positions
        starting from the piece's current position through all hops.
        @param row: The starting row index of the piece to find chains for
        @param col: The starting column index of the piece to find chains for
        @param chain_so_far: Used internally to build the current chain during recursion
        @param captured_so_far: Used internally to track which enemy pieces have been 
        captured in the current chain to avoid re-capturing them
        @return: A list of chains, where each chain is a list of (row, col) 
        tuples representing the sequence of positions in that capture chain
        """
        if chain_so_far is None:
            chain_so_far = [(row, col)]
        if captured_so_far is None:
            captured_so_far = set()

        further_captures = self.captures(row, col)
        # Filter out any landing squares that would require jumping the same piece twice
        # (captured_so_far tracks which enemy squares are already removed)
        valid_captures = []
        for (lr, lc) in further_captures:
            mid_r = (row + lr) // 2
            mid_c = (col + lc) // 2
            if (mid_r, mid_c) not in captured_so_far:
                valid_captures.append((lr, lc))

        if not valid_captures:
            # No more jumps — this chain is complete
            return [chain_so_far]

        all_chains = []
        for (lr, lc) in valid_captures:
            mid_r = (row + lr) // 2
            mid_c = (col + lc) // 2

            # Simulate the hop
            cr, cc, cp = self.make_move_no_validate(row, col, lr, lc)

            new_captured = captured_so_far | {(cr, cc)}
            sub_chains = self.get_jump_chains(lr, lc, chain_so_far + [(lr, lc)], new_captured)
            all_chains.extend(sub_chains)

            # Undo the hop
            self.board[row][col] = self.board[lr][lc]
            self.board[lr][lc] = "."
            self.board[cr][cc] = cp

            # Undo any promotion that happened
            piece = self.board[row][col]
            if piece == "B" and row != 0:
                self.board[row][col] = "b"
            elif piece == "C" and row != self.board_size - 1:
                self.board[row][col] = "c"

        return all_chains

    def get_all_jump_chains(self, player):
        """
        Returns all complete capture chains for the given player as a dict:
          { (start_row, start_col): [ [(r0,c0),(r1,c1),...], ... ] }
        Only pieces that have captures are included.
        @param player: The player ("b" or "c") to find jump chains for
        @return: A dictionary mapping piece positions to lists of capture chains, 
        where each chain is a list of (row, col) tuples representing the sequence of positions in that capture chain
        """
        chains = {}
        for row in range(self.board_size):
            for col in range(self.board_size):
                square = self.board[row][col]
                if square != "." and square.lower() == player:
                    if self.captures(row, col):
                        piece_chains = self.get_jump_chains(row, col)
                        if piece_chains:
                            chains[(row, col)] = piece_chains
        return chains

    def check_winner(self):
        """
        Determines the winner of the game by checking if either player has no
        remaining pieces or valid moves. Returns 'c' if the AI wins, 'b' if the
        player wins, or None if there is no winner yet.
        @return: 'c' if the AI wins, 'b' if the player wins, or None if there is no winner yet
        @note: This method checks for both piece count and move availability to determine the winner, 
        ensuring that a player who is blocked but still has pieces is also considered defeated.
        """
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
        """
        Returns a dictionary mapping each of the current player's pieces to
        their available moves. If forced captures are enabled and any capture
        moves exist, only those capture moves are returned.
        @param player: The player ("b" or "c") to get moves for
        @return: A dictionary mapping piece positions to lists of valid move coordinates for that piece,
        """
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
        """
        Checks if the specified player has any available capture moves on the
        board. Returns True if at least one capture is possible; otherwise,
        returns False.
        @param player: The player ("b" or "c") to check for available captures
        @return: True if the player has at least one available capture move, False otherwise
        """
        for row in range(self.board_size):
            for col in range(self.board_size):
                square = self.board[row][col]
                if square != "." and square.lower() == player:
                    if self.captures(row, col):
                        return True
        return False