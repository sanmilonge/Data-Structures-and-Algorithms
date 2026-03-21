import curses
import time
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


def draw_board(stdscr, game, cursor, selected, moves, ai_time=None, timers=None):

    stdscr.clear()

    size = game.board_size
    left = 10

    # column numbers
    stdscr.addstr(0, left + 2, "   ".join(str(i + 1) for i in range(size)))

    border = "+---" * size + "+"

    for r in range(size):

        stdscr.addstr(r * 2 + 1, left, border)
        stdscr.addstr(r * 2 + 2, left - 2, str(r + 1))

        for c in range(size):

            piece = game.board[r][c]
            symbol = render_cell(piece)

            y = r * 2 + 2
            x = left + c * 4 + 1

            stdscr.addstr(y, left + c * 4, "|")

            if (r, c) == cursor:
                stdscr.attron(curses.A_REVERSE)

            if selected == (r, c):
                stdscr.attron(curses.A_BOLD)

            if (r, c) in moves:
                stdscr.attron(curses.A_DIM)

            stdscr.addstr(y, x, symbol)

            stdscr.attroff(curses.A_REVERSE)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.A_DIM)
        y = r * 2 + 2
        stdscr.addstr(y, left + size * 4, "|")

    stdscr.addstr(size * 2 + 1, left, border)

    if ai_time is not None:
        stdscr.addstr(1, 50, f"AI thinking: {ai_time:.2f}s")

    if timers:
        p1, p2 = timers
        stdscr.addstr(3, 50, f"P1 time: {int(p1)}s")
        stdscr.addstr(4, 50, f"P2 time: {int(p2)}s")

    stdscr.refresh()


def run_curses_game(stdscr, game, ai_mode=False, ai_depth=2, timer=None):

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

    while True:

        if p1_time is not None and p2_time is not None:
            now = time.time()
            elapsed = now - last_tick
            last_tick = now

            if players_turn:
                p1_time -= elapsed
            else:
                p2_time -= elapsed

            if p1_time <= 0 :
                winner = 'c'
                break
            if p2_time <= 0:
                winner = 'b'
                break


        draw_board(
            stdscr,
            game,
            cursor,
            selected,
            moves,
            ai_time,
            (p1_time, p2_time) if timer else None,
        )

        winner = game.check_winner()

        if winner:
            stdscr.addstr(20, 10, f"{winner.upper()} WINS! Press q")
            key = stdscr.getch()
            if key == ord("q"):
                break

        if ai_mode and not players_turn:

            start = time.time()
            score, move = minimax(game, ai_depth, float("-inf"), float("inf"), True)
            end = time.time()

            ai_time = end - start

            if move is None:
                break

            (sr, sc), (er, ec) = move

            animate_ai_move(stdscr, game, (sr, sc), (er, ec))

            game.make_move(sr, sc, er, ec)

            players_turn = True
            continue

        key = stdscr.getch()

        if key == ord("q"):
            break

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            cursor = move_cursor(key, cursor, game.board_size)

        elif key == 10:

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

                    animate_ai_move(stdscr, game, (sr, sc), (r, c))

                    game.make_move(sr, sc, r, c)

                    players_turn = not players_turn

                selected = None
                moves = []