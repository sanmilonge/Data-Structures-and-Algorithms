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
        self.board = []
        self.board_size = board_size
        self.forced_capture = forced_capture

        for row in range(board_size):
            new_row = []
            for col in range(board_size):
                new_row.append(".")
            self.board.append(new_row)

        self.setup_pieces()


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
        rows_of_pieces = (self.board_size // 2) - 1  # e.g. 3 for 8x8, 4 for 10x10, 5 for 12x12

        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    if row < rows_of_pieces:
                        self.board[row][col] = "c"
                    elif row >= self.board_size - rows_of_pieces:
                        self.board[row][col] = "b"


    def get_moves(self, row, col):
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
        captures = self.captures(row, col)
        if captures:
            return captures
        else:
            return self.get_moves(row, col)

    def make_move(self, start_row, start_col, end_row, end_col):
        """
        Executes a single move or single capture hop on the board.
        Does NOT enforce turn order or multi-jump chaining — callers handle that.
        Returns True if successful, False if invalid.
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

        # Remove captured piece if this was a jump
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            self.board[captured_row][captured_col] = "."

        # Promotion — but don't promote mid-chain (piece keeps jumping as king from here)
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

        e.g. [(2,3), (4,5), (6,7)] means: piece at (2,3) jumps to (4,5) then to (6,7)
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