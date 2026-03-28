import curses


def menu(stdscr):
    """
    Displays an interactive menu using curses, allowing the user to select
    between game modes, toggle the forced capture rule, or quit. Returns the
    selected option and the current forced capture setting as a tuple.
    """

    curses.curs_set(0)

    forced_capture = True

    options = [
        "Player vs Player",
        "Player vs AI",
        "Forced Capture: ON",
        "Quit",
    ]

    current = 0

    while True:

        stdscr.clear()
        stdscr.addstr(1, 5, "CHECKERS")

        for i, option in enumerate(options):

            if i == current:
                stdscr.attron(curses.A_REVERSE)

            stdscr.addstr(3 + i, 5, option)

            if i == current:
                stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()

        if key == curses.KEY_UP and current > 0:
            current -= 1

        elif key == curses.KEY_DOWN and current < len(options) - 1:
            current += 1

        elif key == 10:

            if options[current].startswith("Forced Capture"):
                forced_capture = not forced_capture
                options[2] = f"Forced Capture: {'ON' if forced_capture else 'OFF'}"
                continue

            return options[current], forced_capture