import random

class Player:
    def __init__(self, player_id, start_pos, symbol, direction="UP"):
        self.id = player_id
        self.symbol = symbol
        self.position = start_pos
        self.direction = direction
        self.crashed = False
    
    def move(self):
        x, y = self.position
        if self.direction == "UP":
            y -= 1
        elif self.direction == "DOWN":
            y += 1
        elif self.direction == "LEFT":
            x -= 1
        elif self.direction == "RIGHT":
            x += 1
        self.position = (x, y)

class Agent(Player):
    def __init__(self, player_id, start_pos, symbol, watchtower):
        super().__init__(player_id, start_pos, symbol)
        self.watchtower = watchtower  # Odniesienie do wieży
    
    def decide_move(self):
        # Pobiera najlepszy ruch od wieży
        self.direction = self.watchtower.get_best_move(self)
 
        
class Watchtower:
    def __init__(self, game):
        self.game = game  # Obiekt gry, który zawiera planszę i agentów
    
    def get_best_move(self, agent):
        """
        Analizuje najlepszy ruch dla podanego agenta na podstawie stanu planszy.
        """
        x, y = agent.position
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        
        best_direction = None
        best_score = float('-inf')
        
        for direction, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            
            # Sprawdzenie czy nowa pozycja jest w obrębie planszy
            if 0 <= new_x < self.game.width and 0 <= new_y < self.game.height:
                # Sprawdzenie, czy nowa pozycja jest pusta
                if self.game.board[new_y][new_x] == '..':
                    # Ocena ruchu 
                    score = self.evaluate_move(new_x, new_y, agent)
                    
                    if score > best_score:
                        best_score = score
                        best_direction = direction
        
        return best_direction if best_direction else random.choice(list(directions.keys()))  # Jeśli brak opcji, wylosuj ruch

    def evaluate_move(self, x, y, agent):
        """
        Przykładowa funkcja oceny ruchu dla wieży. 
        """
        score = 0
        
        # Więcej punktów za wolne miejsca wokół
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.game.width and 0 <= ny < self.game.height:
                if self.game.board[ny][nx] == '.':
                    score += 1  # Wolne pole to +1 punkt

        # Kary za bliskość innych agentów
        for other_agent in self.game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)
                if distance == 1:
                    score -= 10  # Bardzo blisko – duża kara
                elif distance == 2:
                    score -= 3   # Blisko – mniejsza kara

        return score


 
import curses
def main_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Wybierz tryb gry:")
        stdscr.addstr(1, 0, "1: Użytkownik steruje jednym graczem, reszta to agenci")
        stdscr.addstr(2, 0, "2: Grają sami agenci")
        stdscr.addstr(3, 0, "Podaj numer trybu (1 lub 2), lub 'q' aby wyjść: ")
        stdscr.refresh()

        # Pobieranie wyboru trybu gry
        choice = stdscr.getkey()
        if choice == 'q':  # Wyjście z programu
            break
        elif choice in ('1', '2'):
            game_mode = "user_vs_agents" if choice == '1' else "agents_only"
            
            # Uruchomienie gry w wybranym trybie
            game = create_game(game_mode)
            curses.wrapper(game_loop, game, game_mode)

def game_loop(stdscr, game, mode):
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
            
            for agent in game.players[1:]:
                if not agent.crashed:
                    agent.decide_move()
        
        elif mode == "agents_only":
            for agent in game.players:
                if not agent.crashed:
                    agent.decide_move()
        
        game.update()
        stdscr.refresh()
        
        # Sprawdzenie, czy gra się skończyła
        if game.all_players_crashed():
            break
        curses.napms(1000)

    # Po zakończeniu gry
    stdscr.addstr(max_y // 2, max_x // 2 - 10, "Koniec gry! Wciśnij dowolny klawisz, aby wrócić do menu.")
    stdscr.refresh()
    stdscr.nodelay(0)  # Tryb blokowania terminala, aby czekać na naciśnięcie klawisza
    stdscr.getch()


# Inicjalizacja graczy i agentów
def create_game(mode):
    # Tworzymy grę i wieżę
    board_size = 20
    game = Game(board_size, board_size, [])
    watchtower = Watchtower(game)
    
    if mode == "user_vs_agents":
        player1 = Player(1, game.random_empty_position(), 'P1', "UP")
        agent1 = Agent(2, game.random_empty_position(), 'A1', watchtower)
        agent2 = Agent(3, game.random_empty_position(), 'A2', watchtower)
        game.players = [player1, agent1, agent2]
    
    elif mode == "agents_only":
        agent1 = Agent(1, game.random_empty_position(), 'A1', watchtower)
        agent2 = Agent(2, game.random_empty_position(), 'A2', watchtower)
        agent3 = Agent(3, game.random_empty_position(), 'A3', watchtower)
        game.players = [agent1, agent2, agent3]
    
    return game


# Definicja klasy Game
class Game:
    def __init__(self, width, height, players):
        self.width = width
        self.height = height
        self.players = players
        self.board = [['..' for _ in range(width)] for _ in range(height)]
        self.occupied_positions = set()  # Zbiór zajętych pozycji
        
        for player in self.players:
            player.position = self.random_empty_position()
            x, y = player.position
            self.board[y][x] = player.symbol
            
    def random_empty_position(self):
        """Zwraca losową, wolną pozycję na planszy."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == '..':
                self.occupied_positions.add((x, y))
                return (x, y)
    
    def update(self):
        for player in self.players:
            if not player.crashed:
                player.move()
                x, y = player.position
                if not (0 <= x < self.width and 0 <= y < self.height) or self.board[y][x] != '..':
                    player.crashed = True
                else:
                    self.board[y][x] = player.symbol
    
    def all_players_crashed(self):
        return all(player.crashed for player in self.players)
    
    def display(self):
        for row in self.board:
            print(' '.join(row))


# Uruchomienie menu w curses.wrapper
curses.wrapper(main_menu)
