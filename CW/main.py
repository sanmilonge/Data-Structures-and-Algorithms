import curses
from board import Board
from curses_ui import run_curses_game, prompt_name
from menu import menu


def ask_name(stdscr, prompt, default):
    """
    Prompts the user for a name using stdscr and prompt; returns the entered
    name or default if no input is provided.
    @param stdscr: The curses standard screen object to use for input
    @param prompt: The prompt message to display when asking for the name
    @param default: The default name to return if the user enters an empty string
    @return: The entered name or the default name if input is empty
    """
    name = prompt_name(stdscr, prompt) # Asks for player name with a prompt, returns the entered name or default if empty
    return name if name else default


def main(stdscr):
    """
    Handles the main game loop using a curses-based UI, allowing the user to
    select between Player vs Player and Player vs AI modes, configure game
    options (names, board size, timer, difficulty), and start the game with
    the chosen settings.
    @param stdscr: The curses standard screen object to use for UI rendering
    @return: None
    """
    choice, forced_capture = menu(stdscr)

    if choice == "Quit":
        return

    if choice == "Player vs Player":

        # Ask for names
        p1_name = ask_name(stdscr, "Enter Player 1 name (press Enter to confirm):", "Player 1")
        p2_name = ask_name(stdscr, "Enter Player 2 name (press Enter to confirm):", "Player 2")

        stdscr.clear()

        # Dynamic board size selection
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

        # Timer selection
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

        run_curses_game(stdscr, game, False, timer=timer, p1_name=p1_name, p2_name=p2_name)

    elif choice == "Player vs AI":

        # Ask for player name
        p1_name = ask_name(stdscr, "Enter your name (press Enter to confirm):", "Player")

        stdscr.clear()
        stdscr.addstr(5, 5, "Difficulty")
        stdscr.addstr(7, 5, "1) Easy")
        stdscr.addstr(8, 5, "2) Medium")
        stdscr.addstr(9, 5, "3) Hard")

        key = stdscr.getch()

        depth = 3
        if key == ord("2"):
            depth = 4
        elif key == ord("3"):
            depth = 5

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

        game = Board(size, forced_capture)

        run_curses_game(stdscr, game, True, depth, p1_name=p1_name, p2_name="AI")


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")