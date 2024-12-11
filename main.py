import curses
import random
from game import Game
from watchtower import Watchtower
from agent import Agent, AggressiveAgent, Player

def main_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Wybierz tryb gry:")
        stdscr.addstr(1, 0, "1: Użytkownik steruje jednym graczem, reszta to agenci")
        stdscr.addstr(2, 0, "2: Grają sami agenci")
        stdscr.addstr(3, 0, "Podaj numer trybu (1 lub 2), lub 'q' aby wyjść: ")
        stdscr.refresh()

        # Pobieranie wyboru trybu gry
        try:
            choice = stdscr.getkey()
        except curses.error:
            choice = None
        if choice == 'q':  # Wyjście z programu
            break
        elif choice in ('1', '2'):
            game_mode = "user_vs_agents" if choice == '1' else "agents_only"
            
            # Uruchomienie gry w wybranym trybie
            game, watchtower = create_game(game_mode)
            game_loop(stdscr, game, watchtower, game_mode)
            
            
def game_loop(stdscr, game, watchtower, mode):
    curses.curs_set(0)  # Ukrycie kursora
    stdscr.nodelay(1)   # Terminal w trybie non-blocking
    
    max_y, max_x = stdscr.getmaxyx()
    if game.height > max_y or game.width * 2 > max_x:
        stdscr.addstr(0, 0, "Za małe okno terminala!")
        stdscr.refresh()
        stdscr.getch()
        return

    while True:
        stdscr.clear()
        
        # Wyświetlenie planszy
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
        
        # Sprawdzenie, czy gra się skończyła
        if game.all_players_crashed():
            break
        curses.napms(300)
        
        # Check for a winner
        active_players = [player for player in game.players if not player.crashed]
        if len(active_players) == 1:
            winner = active_players[0]
            stdscr.addstr(len(game.board) + 1, 0, f"The winner is {winner.symbol}!")
            stdscr.refresh()
            stdscr.nodelay(0)  # Tryb blokowania terminala, aby czekać na naciśnięcie klawisza
            stdscr.getch()
            break
        elif len(active_players) == 0:
            stdscr.addstr(max_y // 2, max_x // 2 - 10, "It's a draw!")
            stdscr.refresh()
            stdscr.nodelay(0)  # Tryb blokowania terminala, aby czekać na naciśnięcie klawisza
            stdscr.getch()
            break

        # Pause for a short time
        curses.napms(500)


# Inicjalizacja graczy i agentów
def create_game(mode):
    # Tworzymy grę i wieżę
    board_size = 20
    game = Game(board_size, board_size, [])
    watchtower = Watchtower()
    
    if mode == "user_vs_agents":
        player1 = Player(1, game.random_empty_position(), 'P1')
        agent1 = AggressiveAgent(2, game.random_empty_position(), 'A1')
        agent2 = Agent(3, game.random_empty_position(), 'A2')
        game.players = [player1, agent1, agent2]
    
    elif mode == "agents_only":
        agent1 = AggressiveAgent(1, game.random_empty_position(), 'A1')
        agent2 = AggressiveAgent(2, game.random_empty_position(), 'A2')
        agent3 = Agent(3, game.random_empty_position(), 'A3')
        agent4 = Agent(4, game.random_empty_position(), 'A4')
        game.players = [agent1, agent2, agent3,agent4]
    
    return game, watchtower


# Uruchomienie menu w curses.wrapper
curses.wrapper(main_menu)
