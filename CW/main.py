import curses
from board import Board
from curses_ui import run_curses_game
from menu import menu


def main(stdscr):

    choice, forced_capture = menu(stdscr)

    if choice == "Quit":
        return

    if choice == "Player vs Player":

        stdscr.clear()
        stdscr.addstr(5, 5, "Board Size")
        stdscr.addstr(7, 5, "1) 8x8")
        stdscr.addstr(8, 5, "2) 10x10")
        stdscr.addstr(9, 5, "3) 12x12")

        key = stdscr.getch()

        size = 8
        if key == ord("2"):
            size = 10
        elif key == ord("3"):
            size = 12

        stdscr.clear()
        stdscr.addstr(5, 5, "Timer")
        stdscr.addstr(7, 5, "1) No Timer")
        stdscr.addstr(8, 5, "2) 5 minutes")
        stdscr.addstr(9, 5, "3) 10 minutes")

        key = stdscr.getch()

        timer = None
        if key == ord("2"):
            timer = 300
        elif key == ord("3"):
            timer = 600

        game = Board(size, forced_capture)

        run_curses_game(stdscr, game, False, timer=timer)

    elif choice == "Player vs AI":

        stdscr.clear()
        stdscr.addstr(5, 5, "Difficulty")
        stdscr.addstr(7, 5, "1) Easy")
        stdscr.addstr(8, 5, "2) Medium")
        stdscr.addstr(9, 5, "3) Hard")

        key = stdscr.getch()

        depth = 2
        if key == ord("2"):
            depth = 3
        elif key == ord("3"):
            depth = 4

        game = Board(8, forced_capture)

        run_curses_game(stdscr, game, True, depth)


curses.wrapper(main)