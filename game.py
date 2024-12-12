import random

class Game:
    def __init__(self, width, height, players):
        self.width = width
        self.height = height
        self.players = players
        self.board = [['..' for _ in range(width)] for _ in range(height)]
        self.occupied_positions = set() 
        
        for player in self.players:
            player.position = self.random_empty_position()
            x, y = player.position
            self.board[y][x] = player.symbol
            
    def random_empty_position(self):
        """Returns random, empty positon on the board."""
        while True:
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
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


