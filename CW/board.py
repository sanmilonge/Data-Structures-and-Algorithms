checkerPieces = {
    "b": "●",   # player piece
    "B": "⬤",   # player king
    "c": "○",   # AI piece
    "C": "◯",   # AI king
    ".": "·"    # empty square
    }

# Converts the internal representation of the board to a human-readable format
def render_cell(cell): 
    return checkerPieces[cell]

class Board:
    def __init__(self):
        self.board = []

        for row in range(8):
            new_row = []
            for col in range(8):
                new_row.append(".")
            self.board.append(new_row)

        self.setup_pieces()

    def print_board(self):
        print("  ", end="  ")
        for col in range(8):
            print(col, end="  ")
        print()

        for row in range(8):
            print(row, end="   ")
            for col in range(8): 
                cell = self.board[row][col]
                print(render_cell(cell), end="  ")
            print()
    def setup_pieces(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = "c"
                    elif row > 4:
                        self.board[row][col] = "b"