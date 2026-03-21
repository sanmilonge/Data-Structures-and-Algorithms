import curses
import time
from copy import deepcopy
from board import render_cell
from ai import minimax


def animate_ai_move(stdscr, game, start, end):

    sr, sc = start
    er, ec = end

    for _ in range(2):

        draw_board(stdscr, game, (sr, sc), None, [(er, ec)])
        stdscr.refresh()
        time.sleep(0.15)

        draw_board(stdscr, game, (er, ec), None, [])
        stdscr.refresh()
        time.sleep(0.15)


def move_cursor(key, cursor, size):

    r, c = cursor

    if key == curses.KEY_UP and r > 0:
        r -= 1
    elif key == curses.KEY_DOWN and r < size - 1:
        r += 1
    elif key == curses.KEY_LEFT and c > 0:
        c -= 1
    elif key == curses.KEY_RIGHT and c < size - 1:
        c += 1

    return (r, c)


def draw_board(stdscr, game, cursor, selected, moves, ai_time=None, timers=None,
               p1_name=None, p2_name=None, players_turn=True, history_mode=False,
               history_index=None, history_len=None, ai_mode=False,
               p1_captures=0, p2_captures=0, alert_msg=None):

    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    info_col = max_x - 22

    size = game.board_size
    left = 10

    # --- Header: names ---
    name1 = p1_name or "Player 1"
    name2 = p2_name or "Player 2"
    header = f"{name1}  vs  {name2}"
    stdscr.addstr(0, left, header, curses.A_BOLD)

    # Turn indicator
    if not history_mode:
        if players_turn:
            turn_msg = f"{name1}'s turn"
        else:
            turn_msg = f"{name2}'s turn"
        stdscr.addstr(0, info_col, turn_msg)

    # column numbers
    stdscr.addstr(2, left + 2, "   ".join(str(i + 1) for i in range(size)))

    border = "+---" * size + "+"

    for r in range(size):

        stdscr.addstr(r * 2 + 3, left, border)
        stdscr.addstr(r * 2 + 4, left - 2, str(r + 1))

        for c in range(size):

            piece = game.board[r][c]
            symbol = render_cell(piece)

            y = r * 2 + 4
            x = left + c * 4 + 1

            stdscr.addstr(y, left + c * 4, "|")

            attrs = 0

            if (r, c) == cursor:
                attrs |= curses.A_REVERSE

            if selected == (r, c):
                # Highlight selected piece: bold + reverse + underline for visibility
                attrs |= curses.A_BOLD | curses.A_REVERSE | curses.A_UNDERLINE

            if (r, c) in moves:
                attrs |= curses.A_DIM

            if attrs:
                stdscr.attron(attrs)

            stdscr.addstr(y, x, symbol)

            if attrs:
                stdscr.attroff(attrs)

        y = r * 2 + 4
        stdscr.addstr(y, left + size * 4, "|")

    stdscr.addstr(size * 2 + 3, left, border)

    # --- Capture counts: P1 bottom-left, P2 top-right of board ---
    board_bottom = size * 2 + 4
    piece_symbol_p1 = "●"
    piece_symbol_p2 = "○"
    p1_capture_str = f"{name1} captured: {piece_symbol_p2} x{p1_captures}"
    p2_capture_str = f"{name2} captured: {piece_symbol_p1} x{p2_captures}"
    try:
        stdscr.addstr(board_bottom, left, p1_capture_str, curses.A_BOLD)
        stdscr.addstr(board_bottom, left + len(p1_capture_str) + 4, p2_capture_str, curses.A_BOLD)
    except curses.error:
        pass

    # --- Right panel ---
    if ai_time is not None:
        stdscr.addstr(2, info_col, f"AI time: {ai_time:.2f}s")

    if timers:
        p1, p2 = timers
        stdscr.addstr(4, info_col, f"{name1}: {int(p1)}s")
        stdscr.addstr(5, info_col, f"{name2}: {int(p2)}s")

    # History mode indicator
    if history_mode:
        stdscr.addstr(2, info_col, "[ HISTORY MODE ]", curses.A_BOLD | curses.A_REVERSE)
        if history_index is not None and history_len is not None:
            stdscr.addstr(3, info_col, f"Move {history_index}/{history_len - 1}")

    # --- Alert message (forced capture / multi-jump) ---
    if alert_msg and not history_mode:
        alert_y = max_y - 3
        try:
            stdscr.addstr(alert_y, 0, f" {alert_msg} ".center(max_x - 1), curses.A_BOLD | curses.A_BLINK)
        except curses.error:
            pass

    # --- Footer instructions ---
    footer_y = max_y - 2
    if history_mode:
        footer = " u: undo  r: redo  Enter: confirm & resume "
    elif ai_mode:
        footer = " Arrows: move  Enter: select/move  u: history  q: quit "
    else:
        footer = " Arrows: move  Enter: select/move  q: quit "

    try:
        stdscr.addstr(footer_y, 0, footer.ljust(max_x - 1), curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()


def prompt_name(stdscr, prompt):
    """Simple name input using curses."""
    curses.echo()
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(5, 5, prompt)
    stdscr.refresh()
    name = stdscr.getstr(7, 5, 20).decode("utf-8").strip()
    curses.noecho()
    curses.curs_set(0)
    return name if name else None


def show_message(stdscr, game, cursor, selected, moves, message, ai_time=None,
                 timers=None, p1_name=None, p2_name=None, players_turn=True,
                 history_mode=False, history_index=None, history_len=None, ai_mode=False,
                 p1_captures=0, p2_captures=0):
    """Draw the board and overlay a temporary message below the board."""
    draw_board(stdscr, game, cursor, selected, moves, ai_time, timers,
               p1_name, p2_name, players_turn, history_mode, history_index, history_len,
               ai_mode=ai_mode, p1_captures=p1_captures, p2_captures=p2_captures)
    max_y, max_x = stdscr.getmaxyx()
    size = game.board_size
    msg_y = size * 2 + 5
    if msg_y < max_y - 3:
        stdscr.addstr(msg_y, 10, message, curses.A_BOLD)
    stdscr.refresh()


def run_curses_game(stdscr, game, ai_mode=False, ai_depth=2, timer=None,
                    p1_name=None, p2_name=None):

    curses.curs_set(0)

    cursor = (0, 0)
    selected = None
    moves = []

    players_turn = True

    if timer is not None:
        p1_time = float(timer)
        p2_time = float(timer)
    else:
        p1_time = None
        p2_time = None
    last_tick = time.time()

    ai_time = None

    # Capture counts
    p1_captures = 0
    p2_captures = 0

    def count_pieces(board):
        p1 = sum(row.count("b") + row.count("B") for row in board)
        p2 = sum(row.count("c") + row.count("C") for row in board)
        return p1, p2

    # History: list of (board_snapshot, players_turn_snapshot, moved_to)
    # moved_to is the (row, col) the piece landed on — used for highlighting in history mode
    history = [(deepcopy(game.board), True, None)]
    history_index = 0  # points to current state

    history_mode = False
    history_cursor_index = 0  # index being browsed in history mode

    name1 = p1_name or "Player 1"
    name2 = p2_name or ("AI" if ai_mode else "Player 2")

    winner = None

    while True:

        if p1_time is not None and p2_time is not None:
            now = time.time()
            elapsed = now - last_tick
            last_tick = now

            if not history_mode:
                if players_turn:
                    p1_time -= elapsed
                else:
                    p2_time -= elapsed

            if p1_time <= 0:
                winner = name2
                break
            if p2_time <= 0:
                winner = name1
                break

        timers_display = (p1_time, p2_time) if timer else None

        # --- History mode ---
        if history_mode:
            # Highlight the piece at the destination of the current history state
            # Index 0 (game start) has no moved_to, so nothing is highlighted
            history_highlight = history[history_cursor_index][2]

            draw_board(
                stdscr, game, cursor, history_highlight, [],
                ai_time, timers_display,
                name1, name2, players_turn,
                history_mode=True,
                history_index=history_cursor_index,
                history_len=len(history),
                ai_mode=ai_mode,
                p1_captures=p1_captures,
                p2_captures=p2_captures,
            )

            stdscr.timeout(200)
            key = stdscr.getch()
            stdscr.timeout(-1)

            if key == ord("u"):
                if history_cursor_index > 0:
                    history_cursor_index -= 1
                    game.board = deepcopy(history[history_cursor_index][0])
                else:
                    show_message(
                        stdscr, game, cursor, history[history_cursor_index][2], [],
                        "Nothing left to undo!",
                        ai_time, timers_display, name1, name2, players_turn,
                        history_mode=True,
                        history_index=history_cursor_index,
                        history_len=len(history),
                        ai_mode=ai_mode,
                        p1_captures=p1_captures,
                        p2_captures=p2_captures,
                    )
                    time.sleep(1)

            elif key == ord("r"):
                if history_cursor_index < len(history) - 1:
                    history_cursor_index += 1
                    game.board = deepcopy(history[history_cursor_index][0])
                else:
                    show_message(
                        stdscr, game, cursor, history[history_cursor_index][2], [],
                        "Nothing left to redo!",
                        ai_time, timers_display, name1, name2, players_turn,
                        history_mode=True,
                        history_index=history_cursor_index,
                        history_len=len(history),
                        ai_mode=ai_mode,
                        p1_captures=p1_captures,
                        p2_captures=p2_captures,
                    )
                    time.sleep(1)

            elif key == 10:  # Enter — confirm and resume
                # Truncate future history beyond confirmed point
                history = history[:history_cursor_index + 1]
                history_index = history_cursor_index
                players_turn = history[history_index][1]
                selected = None
                moves = []
                history_mode = False
                last_tick = time.time()

            elif key == ord("q"):
                break

            continue

        # --- Normal play ---
        # Compute alert for forced capture / multi-jump
        alert_msg = None
        current_player = "b" if players_turn else "c"
        current_name = name1 if players_turn else name2
        if not (ai_mode and not players_turn):
            if selected is not None:
                # Check for multi-jump: piece just landed and still has captures
                multi_jumps = game.captures(selected[0], selected[1])
                if multi_jumps:
                    alert_msg = f"Multi-jump available! You must continue capturing."
            elif game.forced_capture and game.has_capture(current_player):
                alert_msg = f"Forced capture! {current_name} must take an opponent piece."

        draw_board(
            stdscr, game, cursor, selected, moves,
            ai_time, timers_display,
            name1, name2, players_turn,
            ai_mode=ai_mode,
            p1_captures=p1_captures,
            p2_captures=p2_captures,
            alert_msg=alert_msg,
        )

        winner = game.check_winner()

        if winner:
            win_name = name1 if winner == "b" else name2
            max_y, max_x = stdscr.getmaxyx()
            msg = f"  {win_name} WINS!  Press q to exit  "
            stdscr.addstr(max_y // 2, max(0, (max_x - len(msg)) // 2), msg,
                          curses.A_BOLD | curses.A_REVERSE)
            stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord("q"):
                    return

        # AI move
        if ai_mode and not players_turn:

            start = time.time()
            score, move, chain = minimax(game, ai_depth, float("-inf"), float("inf"), True)
            end = time.time()

            ai_time = end - start

            if move is None or chain is None:
                break

            # Execute and animate each hop in the chain
            for i in range(len(chain) - 1):
                sr, sc = chain[i]
                er, ec = chain[i + 1]

                animate_ai_move(stdscr, game, (sr, sc), (er, ec))

                before_p1, _ = count_pieces(game.board)
                game.make_move(sr, sc, er, ec)
                after_p1, _ = count_pieces(game.board)
                p2_captures += max(0, before_p1 - after_p1)

            final_pos = (chain[-1][0], chain[-1][1])

            # Save full chain as one history entry (start -> final)
            history = history[:history_index + 1]
            history.append((deepcopy(game.board), True, final_pos))
            history_index = len(history) - 1
            history_cursor_index = history_index

            players_turn = True
            continue

        stdscr.timeout(200)
        key = stdscr.getch()
        stdscr.timeout(-1)

        if key == -1:
            continue

        if key == ord("q"):
            break

        # Enter history mode
        if key == ord("u") and ai_mode:
            history_mode = True
            history_cursor_index = history_index
            continue

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            cursor = move_cursor(key, cursor, game.board_size)

        elif key == 10:  # Enter

            r, c = cursor

            if selected is None:

                piece = game.board[r][c]
                current = "b" if players_turn else "c"

                if piece != "." and piece.lower() == current:

                    all_moves = game.get_all_moves(current)

                    if (r, c) in all_moves:
                        selected = (r, c)
                        moves = all_moves[(r, c)]

            else:

                if (r, c) in moves:

                    sr, sc = selected
                    is_capture = abs(r - sr) == 2

                    animate_ai_move(stdscr, game, (sr, sc), (r, c))

                    _, before_p2 = count_pieces(game.board)
                    game.make_move(sr, sc, r, c)
                    _, after_p2 = count_pieces(game.board)
                    p1_captures += max(0, before_p2 - after_p2)

                    # Check for multi-jump: if this was a capture and the piece
                    # can still capture, lock it in place — don't end the turn yet
                    further_captures = game.captures(r, c) if is_capture else []

                    if further_captures:
                        # Stay in same turn, lock piece to (r, c)
                        selected = (r, c)
                        moves = further_captures
                        cursor = (r, c)
                        # Save intermediate hop to history so undo works per-hop
                        history = history[:history_index + 1]
                        history.append((deepcopy(game.board), players_turn, (r, c)))
                        history_index = len(history) - 1
                        history_cursor_index = history_index
                    else:
                        # Turn is over
                        next_turn = not players_turn
                        history = history[:history_index + 1]
                        history.append((deepcopy(game.board), next_turn, (r, c)))
                        history_index = len(history) - 1
                        history_cursor_index = history_index

                        players_turn = next_turn
                        selected = None
                        moves = []

                else:
                    # Clicked somewhere invalid — deselect only if not mid-chain
                    if not (selected and game.captures(selected[0], selected[1])):
                        selected = None
                        moves = []