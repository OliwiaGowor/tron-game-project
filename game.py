import random

# Definicja klasy Game
class Game:
    def __init__(self, width, height, players):
        self.width = width
        self.height = height
        self.board = [['..' for _ in range(width)] for _ in range(height)]
        self.occupied_positions = set()
        
        # Explicitly update the board for each player
        for player in players:
            x, y = player.position
            self.board[y][x] = player.symbol
            self.occupied_positions.add((x, y))
        
        self.players = players


    def random_empty_position(self):
        """Zwraca losową, wolną pozycję na planszy."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == '..':
                self.occupied_positions.add((x, y))
                # print(f"[Game] Assigning position ({x}, {y}) to a player.")  # Debug
                return (x, y)


    def update(self):
        for player in self.players:
            if not player.crashed:
                prev_position = player.position
                player.move()
                x, y = player.position
                if not (0 <= x < self.width and 0 <= y < self.height) or self.board[y][x] != '..':
                    player.crashed = True
                    print(f"[Game] Player {player.symbol} crashed at ({x}, {y}).")  # Debug
                else:
                    self.board[y][x] = player.symbol
                    print(f"[Game] Player {player.symbol} moved from {prev_position} to ({x}, {y}).")  # Debug


    def all_players_crashed(self):
        all_crashed = all(player.crashed for player in self.players)
        if all_crashed:
            self.log_event("All players have crashed.")
        return all_crashed

    def log_event(self, message):
        """Loguje zdarzenie do pliku."""
        with open("game_logs.txt", "a") as log_file:
            log_file.write(f"[Game] {message}\n")
