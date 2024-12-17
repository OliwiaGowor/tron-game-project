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
            
            # Run game in selected mode
            game, watchtower = create_game(game_mode)
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
        stdscr.refresh()
        
        # Check if game ended
        if game.all_players_crashed():
            break
        curses.napms(300)
        
        # Check for a winner
        active_players = [player for player in game.players if not player.crashed]
        if len(active_players) == 1:
            winner = active_players[0]
            stdscr.addstr(len(game.board) + 1, 0, f"The winner is {winner.symbol}! Press any button to continue...")
            stdscr.refresh()
            stdscr.nodelay(0)  # Terminal lock mode, to wait for button press
            stdscr.getch()
            break
        elif len(active_players) == 0:
            stdscr.addstr(max_y // 2, max_x // 2 - 10, "It's a draw! Press any button to continue...")
            stdscr.refresh()
            stdscr.nodelay(0)
            stdscr.getch()
            break

        # Pause for a short time
        curses.napms(500)


# Initialization of the game and agents
def create_game(mode):
    # Create game and watchtower
    board_size = 20
    game = Game(board_size, board_size, [])

    watchtower = Watchtower()
    
    if mode == "user_vs_agents":
        player1 = Player(1, game.random_empty_position(), 'P1')
        agent1 = AggressiveAgent(2, game.random_empty_position(), 'A1')
        agent2 = AggressiveAgent(3, game.random_empty_position(), 'A2')
        game.players = [player1, agent1, agent2]
    
    elif mode == "agents_only":
        agent1 = AggressiveAgent(1, game.random_empty_position(), 'A1')
        agent2 = AggressiveAgent(2, game.random_empty_position(), 'A2')
        agent3 = Agent(3, game.random_empty_position(), 'A3')
        agent4 = Agent(4, game.random_empty_position(), 'A4')
        game.players = [agent1, agent2, agent3,agent4]
    
    return game, watchtower


# Run menu in curses.wrapper
curses.wrapper(main_menu)

