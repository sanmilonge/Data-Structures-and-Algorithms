from board import Board, render_cell
from ai import minimax
from copy import deepcopy
import time


def get_choice(prompt, options):
    """
    Repeatedly prompt until the user enters a valid option number.
    options is a list of strings. Returns the chosen string.
    @param prompt: The prompt to display to the user when asking for input
    @param options: A list of string options to present to the user for selection
    @return: The string from options that the user selected based on their input
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}) {option}")
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"Please enter a number between 1 and {len(options)}.")


def get_name(prompt, default):
    """
    Returns user input as a string from a prompt, or the default value if
    input is empty.
    @param prompt: The prompt to display to the user when asking for input
    @param default: The default value to return if the user provides no input
    @return: The user's input as a string, or the default value if input is empty
    """
    name = input(f"\n{prompt} (press Enter for '{default}'): ").strip()
    return name if name else default




def parse_coord(text, size):
    """
    Parse 'row,col' input (1-indexed) into a (row, col) tuple (0-indexed).
    Returns None if input is invalid.
    @param text: The input string to parse, expected in the format 'row,col' (1-indexed)
    @param size: The size of the board, used to validate that the parsed coordinates are within bounds
    @return: A tuple (row, col) with 0-indexed coordinates if parsing is successful and within bounds, or None if input is invalid
    """
    try:
        parts = text.strip().split(",")
        if len(parts) != 2:
            return None
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= r < size and 0 <= c < size:
            return (r, c)
    except ValueError:
        pass
    return None


def count_pieces(board):
    """
    Returns a tuple with the counts of player 1 ("b" and "B") and player 2
    ("c" and "C") pieces on the given board.
    Player 1 is the human player ('b'), and Player 2 is the AI opponent ('c').
    @param board: The current state of the game board as a 2D list of strings, 
    where each string represents a cell that may contain a piece ('b', 'B', 'c', 'C') or be empty ('.')
    @return: A tuple (p1_count, p2_count) where p1_count is the total number of player 1 pieces 
    ('b' and 'B') and p2_count is the total number of player 2 pieces ('c' and 'C') on the board
    """
    p1 = sum(row.count("b") + row.count("B") for row in board)
    p2 = sum(row.count("c") + row.count("C") for row in board)
    return p1, p2


def history_mode(game, history, history_index, p1_name, p2_name):
    """
    Interactive history browser. Shows board snapshots, lets the user
    step back (u) and forward (r), then confirm (c) to resume from
    the chosen point, or q to quit entirely.

    Returns (new_history_index, quit) where:
      - new_history_index is the confirmed position in history
      - quit is True if the player typed q
    """
    idx = history_index

    while True:
        snapshot, players_turn, p1_cap, p2_cap, description, moved_to = history[idx]

        print(f"\n{'═' * 40}")
        print(f"  [ HISTORY MODE ]  Move {idx} / {len(history) - 1}")
        print(f"  {description}")
        print(f"  {p1_name} captured: {p1_cap}  |  {p2_name} captured: {p2_cap}")
        print(f"{'═' * 40}")

        # Show the board at this snapshot, highlighting the moved-to piece
        temp_board = deepcopy(snapshot)
        game.board = temp_board
        game.print_board(game, highlight=moved_to)

        print("  u = undo (go back)   r = redo (go forward)")
        print("  c = confirm and resume from here   q = quit game")
        cmd = input("  > ").strip().lower()

        if cmd == "u":
            if idx > 0:
                idx -= 1
            else:
                print("  Nothing left to undo.")

        elif cmd == "r":
            if idx < len(history) - 1:
                idx += 1
            else:
                print("  Nothing left to redo.")

        elif cmd == "c":
            # Restore game to this snapshot
            game.board = deepcopy(history[idx][0])
            return idx, False

        elif cmd == "q":
            return idx, True

        else:
            print("  Unknown command.")


def player_turn_ai(game, player, name, history, history_index, p1_name, p2_name):
    """
    Handles a full player turn with history mode support (AI mode only).
    Returns (captures, new_history_index, quit_flag)
    - captures: number of opponent pieces captured this turn
    - new_history_index: updated index in history after confirming a resume point (or unchanged if no history jump)
    - quit_flag: True if the player chose to quit during this turn
    @param game: The current game state object, which will be modified by this function to reflect the player's moves
    @param player: The current player's piece type ('b' for human player, 'c' for AI opponent)
    @param name: The name of the current player, used for display purposes in prompts   
    @param history: A list of tuples representing the history of game states, where each tuple contains (board_snapshot, 
    players_turn, p1_captures, p2_captures, description, moved_to)
    @param history_index: The current index in the history list representing the current game state
    @param p1_name: The name of player 1 (human player), used for display in history mode
    @param p2_name: The name of player 2 (AI opponent), used for display in history mode
    @return: A tuple (captures, new_history_index, quit_flag) where:
    """
    captured = 0
    locked_piece = None

    while True:
        game.print_board(game)

        if locked_piece:
            print(f"  Multi-jump! You must keep capturing with the piece at "
                  f"row {locked_piece[0] + 1}, col {locked_piece[1] + 1}.")
            all_moves = {locked_piece: game.captures(*locked_piece)}
        else:
            all_moves = game.get_all_moves(player)
            if game.forced_capture and game.has_capture(player):
                print(f"  Forced capture! {name} must take an opponent piece.")

        print(f"  {name}'s available pieces: "
              + ", ".join(f"({r+1},{c+1})" for r, c in sorted(all_moves.keys())))
        print(f"  (type 'u' to enter history mode, 'q' to quit)")

        # Select a piece
        while True:
            raw = input(f"  Select piece (row,col): ").strip().lower()

            if raw == "q":
                print("  Quitting game.")
                return None, history_index, True

            if raw == "u":
                if not locked_piece:
                    new_idx, quit_flag = history_mode(game, history, history_index, p1_name, p2_name)
                    history_index = new_idx
                    if quit_flag:
                        return None, history_index, True
                    # History may have been truncated — recalculate captures from snapshot
                    _, players_turn_snap, p1_cap_snap, p2_cap_snap, _, _ = history[history_index]
                    # Return special signal to run_game to reload state
                    return "history_jumped", history_index, False
                else:
                    print("  Can't enter history mode mid-jump chain.")
                continue

            coord = parse_coord(raw, game.board_size)
            if coord is None:
                print("  Invalid format. Use row,col e.g. 3,2")
                continue
            if locked_piece and coord != locked_piece:
                print(f"  You must continue jumping with ({locked_piece[0]+1},{locked_piece[1]+1}).")
                continue
            if coord not in all_moves:
                print("  That piece has no available moves right now.")
                continue
            selected = coord
            break

        moves = all_moves[selected]
        print(f"  Valid moves for ({selected[0]+1},{selected[1]+1}): "
              + ", ".join(f"({r+1},{c+1})" for r, c in moves))

        # Select a destination
        while True:
            raw = input("  Move to (row,col): ").strip().lower()
            if raw == "q":
                print("  Quitting game.")
                return None, history_index, True
            coord = parse_coord(raw, game.board_size)
            if coord is None:
                print("  Invalid format. Use row,col e.g. 5,4")
                continue
            if coord not in moves:
                print("  That's not a valid destination for the selected piece.")
                continue
            destination = coord
            break

        is_capture = abs(destination[0] - selected[0]) == 2
        before_p1, before_p2 = count_pieces(game.board)

        game.make_move(selected[0], selected[1], destination[0], destination[1])

        after_p1, after_p2 = count_pieces(game.board)
        if player == "b":
            captured += max(0, before_p2 - after_p2)
        else:
            captured += max(0, before_p1 - after_p1)

        # Check for multi-jump
        if is_capture and game.captures(destination[0], destination[1]):
            locked_piece = destination
            print(f"  Captured! You can keep jumping.")
        else:
            if is_capture:
                print(f"  Captured!")
            break

    return captured, history_index, False


def player_turn_pvp(game, player, name):
    """
    Handles a full player turn with no history support (PVP mode).
    Returns (captures, quit_flag)
    """
    captured = 0
    locked_piece = None

    while True:
        game.print_board(game)


        if locked_piece:
            print(f"  Multi-jump! You must keep capturing with the piece at "
                  f"row {locked_piece[0] + 1}, col {locked_piece[1] + 1}.")
            all_moves = {locked_piece: game.captures(*locked_piece)}
        else:
            all_moves = game.get_all_moves(player)
            if game.forced_capture and game.has_capture(player):
                print(f"  Forced capture! {name} must take an opponent piece.")

        print(f"  {name}'s available pieces: "
              + ", ".join(f"({r+1},{c+1})" for r, c in sorted(all_moves.keys())))
        print(f"  (type 'q' to quit)")

        # Select a piece
        while True:
            raw = input(f"  Select piece (row,col): ").strip().lower()
            if raw == "q":
                print("  Quitting game.")
                return None, True
            coord = parse_coord(raw, game.board_size)
            if coord is None:
                print("  Invalid format. Use row,col e.g. 3,2")
                continue
            if locked_piece and coord != locked_piece:
                print(f"  You must continue jumping with ({locked_piece[0]+1},{locked_piece[1]+1}).")
                continue
            if coord not in all_moves:
                print("  That piece has no available moves right now.")
                continue
            selected = coord
            break

        moves = all_moves[selected]
        print(f"  Valid moves for ({selected[0]+1},{selected[1]+1}): "
              + ", ".join(f"({r+1},{c+1})" for r, c in moves))

        # Select a destination
        while True:
            raw = input("  Move to (row,col): ").strip().lower()
            if raw == "q":
                print("  Quitting game.")
                return None, True
            coord = parse_coord(raw, game.board_size)
            if coord is None:
                print("  Invalid format. Use row,col e.g. 5,4")
                continue
            if coord not in moves:
                print("  That's not a valid destination for the selected piece.")
                continue
            destination = coord
            break

        is_capture = abs(destination[0] - selected[0]) == 2
        before_p1, before_p2 = count_pieces(game.board)

        game.make_move(selected[0], selected[1], destination[0], destination[1])

        after_p1, after_p2 = count_pieces(game.board)
        if player == "b":
            captured += max(0, before_p2 - after_p2)
        else:
            captured += max(0, before_p1 - after_p1)

        if is_capture and game.captures(destination[0], destination[1]):
            locked_piece = destination
            print(f"  Captured! You can keep jumping.")
        else:
            if is_capture:
                print(f"  Captured!")
            break

    return captured, False


def run_game(game, ai_mode, ai_depth, p1_name, p2_name):
    """Main game loop."""
    players_turn = True
    p1_captures = 0
    p2_captures = 0

    # History tuple: (board_snapshot, players_turn, p1_captures, p2_captures, description, moved_to)
    # moved_to is the (row, col) the piece landed on, used for highlighting in history mode
    # description is a human-readable summary of the move
    history = [(deepcopy(game.board), True, 0, 0, "Game start", None)]
    history_index = 0

    while True:
        winner = game.check_winner()
        if winner:
            game.print_board(game)
            win_name = p1_name if winner == "b" else p2_name
            print(f"\n{'=' * 40}")
            print(f"  {win_name} WINS!")
            print(f"  {p1_name} captured: {p1_captures}  |  {p2_name} captured: {p2_captures}")
            print(f"{'=' * 40}\n")
            return

        if players_turn:
            print(f"\n{'─' * 40}")
            print(f"  {p1_name}'s turn  |  "
                  f"{p1_name} captured: {p1_captures}  |  {p2_name} captured: {p2_captures}")

            if ai_mode:
                result, history_index, quit_flag = player_turn_ai(
                    game, "b", p1_name, history, history_index, p1_name, p2_name
                )
                if quit_flag:
                    return
                if result == "history_jumped":
                    _, players_turn, p1_captures, p2_captures, _, _ = history[history_index]
                    history = history[:history_index + 1]
                    continue
                p1_captures += result
                history = history[:history_index + 1]
                desc = f"{p1_name} moved (turn {len(history)})"
                history.append((deepcopy(game.board), False, p1_captures, p2_captures, desc, None))
                history_index = len(history) - 1
            else:
                result, quit_flag = player_turn_pvp(game, "b", p1_name)
                if quit_flag:
                    return
                p1_captures += result

        else:
            if ai_mode:
                print(f"\n{'─' * 40}")
                print(f"  {p2_name} is thinking...")
                t_start = time.time()
                score, move, chain = minimax(game, ai_depth, float("-inf"), float("inf"), True)
                t_end = time.time()

                if move is None or chain is None:
                    print(f"  {p2_name} has no moves. {p1_name} wins!")
                    return

                print(f"  {p2_name} thinking time: {t_end - t_start:.2f}s")

                for i in range(len(chain) - 1):
                    sr, sc = chain[i]
                    er, ec = chain[i + 1]
                    before_p1, _ = count_pieces(game.board)
                    game.make_move(sr, sc, er, ec)
                    after_p1, _ = count_pieces(game.board)
                    p2_captures += max(0, before_p1 - after_p1)

                start_pos = f"({chain[0][0]+1},{chain[0][1]+1})"
                end_pos = f"({chain[-1][0]+1},{chain[-1][1]+1})"
                hops = len(chain) - 1
                hop_str = f"{hops} hop{'s' if hops > 1 else ''}"
                moved_to = (chain[-1][0], chain[-1][1])
                desc = f"{p2_name} moved: {start_pos} → {end_pos} ({hop_str})"
                print(f"  {desc}")

                # Save to history
                history = history[:history_index + 1]
                history.append((deepcopy(game.board), True, p1_captures, p2_captures, desc, moved_to))
                history_index = len(history) - 1

            else:
                print(f"\n{'─' * 40}")
                print(f"  {p2_name}'s turn  |  "
                      f"{p1_name} captured: {p1_captures}  |  {p2_name} captured: {p2_captures}")

                result, quit_flag = player_turn_pvp(game, "c", p2_name)
                if quit_flag:
                    return
                p2_captures += result

        players_turn = not players_turn


def main():
    print("\n" + "=" * 40)
    print("         CHECKERS")
    print("=" * 40)

    mode = get_choice("Game mode:", ["Player vs Player", "Player vs AI", "Quit"])

    if mode == "Quit":
        return

    forced_capture_choice = get_choice("Forced capture:", ["On", "Off"])
    forced_capture = forced_capture_choice == "On"

    if mode == "Player vs Player":
        p1_name = get_name("Player 1 name", "Player 1")
        p2_name = get_name("Player 2 name", "Player 2")

        size_choice = get_choice("Board size:", ["8x8", "10x10", "12x12"])
        size = {"8x8": 8, "10x10": 10, "12x12": 12}[size_choice]

        game = Board(size, forced_capture)
        run_game(game, ai_mode=False, ai_depth=None,
                 p1_name=p1_name, p2_name=p2_name)

    elif mode == "Player vs AI":
        p1_name = get_name("Your name", "Player")
        p2_name = "AI"

        size_choice = get_choice("Board size:", ["8x8", "10x10", "12x12"])
        size = {"8x8": 8, "10x10": 10, "12x12": 12}[size_choice]

        diff = get_choice("Difficulty:", ["Easy", "Medium", "Hard"])
        depth = {"Easy": 2, "Medium": 3, "Hard": 4}[diff]

        game = Board(size, forced_capture)
        run_game(game, ai_mode=True, ai_depth=depth,
                 p1_name=p1_name, p2_name=p2_name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")