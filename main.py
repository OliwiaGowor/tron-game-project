import curses
import random
from game import Game
from watchtower import Watchtower
from agent import Agent, AggressiveAgent, Player

def main_menu(stdscr):

    with open("game_logs.txt", "w") as log_file:  # Reset log file
        log_file.write("[Main] Game started.\n")

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose game mode:")
        stdscr.addstr(1, 0, "1: User vs computer")
        stdscr.addstr(2, 0, "2: Computer only")
        stdscr.addstr(3, 0, "Select a game mode (1 or 2), or write 'q' to quit: ")
        stdscr.refresh()

        # Get game mode from user
        try:
            choice = stdscr.getkey()
        except curses.error:
            choice = None
        if choice == 'q':  # Quit program
            break
        elif choice in ('1', '2'):
            game_mode = "user_vs_agents" if choice == '1' else "agents_only"
            
            stdscr.clear()
            
            if choice == '1':
                # Ask for the number of players
                stdscr.addstr(0, 0, "Enter the number of players (1-3): ")
                stdscr.refresh()

                try:
                    num_players = int(stdscr.getkey())
                    if num_players < 1 or num_players > 3:
                        raise ValueError
                except ValueError:
                    stdscr.addstr(1, 0, "Invalid input! Press any key to return to the main menu.")
                    stdscr.refresh()
                    stdscr.getch()
                    continue

            elif choice == '2':
                # Ask for the number of players
                stdscr.addstr(0, 0, "Enter the number of players (2-4): ")
                stdscr.refresh()

                try:
                    num_players = int(stdscr.getkey())
                    if num_players < 2 or num_players > 4:
                        raise ValueError
                except ValueError:
                    stdscr.addstr(1, 0, "Invalid input! Press any key to return to the main menu.")
                    stdscr.refresh()
                    stdscr.getch()
                    continue

            # Run the game with selected mode and number of players
            game, watchtower = create_game(game_mode, num_players)
            game_loop(stdscr, game, watchtower, game_mode)

def game_loop(stdscr, game, watchtower, mode):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Terminal in non-blocking mode

    max_y, max_x = stdscr.getmaxyx()
    if game.height > max_y or game.width * 2 > max_x:
        stdscr.addstr(0, 0, "The terminal window is too small!")
        stdscr.refresh()
        stdscr.getch()
        return

    crash_order = []  # To track the order in which players crash

    while True:
        stdscr.clear()

        # Display board
        for y, row in enumerate(game.board):
            if y < max_y:
                stdscr.addstr(y, 0, ' '.join(row))

        if mode == "user_vs_agents":
            key = stdscr.getch()
            if key == ord('w'):
                game.players[0].direction = "UP"
            elif key == ord('s'):
                game.players[0].direction = "DOWN"
            elif key == ord('a'):
                game.players[0].direction = "LEFT"
            elif key == ord('d'):
                game.players[0].direction = "RIGHT"

            # Agents decide their moves
            for agent in game.players[1:]:
                agent.decide_move(game, watchtower)

        elif mode == "agents_only":
            for agent in game.players:
                agent.decide_move(game, watchtower)

        game.update()

        # Record crash order
        for player in game.players:
            if player.crashed and player not in crash_order:
                crash_order.append(player)

        stdscr.refresh()

        # Check if game ended
        if game.all_players_crashed():
            break

        active_players = [player for player in game.players if not player.crashed]
        if len(active_players) == 1:
            crash_order.append(active_players[0])  # The last active player is added to the crash order
            break

        curses.napms(500)

    # Display rankings
    display_rankings(stdscr, crash_order)

def display_rankings(stdscr, crash_order):
    stdscr.clear()
    stdscr.addstr(0, 0, "Game Over! Final Rankings:")

    for idx, player in enumerate(reversed(crash_order), start=1):
        status = "Winner" if idx == 1 else "Crashed"
        stdscr.addstr(idx, 0, f"{idx}. {player.symbol} - {status}")
    
    stdscr.addstr(len(crash_order) + 1, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.nodelay(0)
    stdscr.getch()


def create_game(mode, num_players):
    board_size = 20
    game = Game(board_size, board_size, [])

    watchtower = Watchtower()

    players = []
    agent_types = [Agent, AggressiveAgent] 

    if mode == "user_vs_agents":
        players.append(Player(1, game.random_empty_position(), 'P1'))
        for i in range(1, num_players + 1):
            agent_class = random.choice(agent_types)
            players.append(agent_class(i, game.random_empty_position(), f'A{i}'))

    elif mode == "agents_only":
        for i in range(1, num_players + 1):
            agent_class = random.choice(agent_types)
            players.append(agent_class(i, game.random_empty_position(), f'A{i}'))

    game.players = players
    return game, watchtower


# Run menu in curses.wrapper
curses.wrapper(main_menu)

