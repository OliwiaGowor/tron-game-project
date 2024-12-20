import random

class Player:
    def __init__(self, player_id, start_pos=None, symbol='P1', direction="UP"):
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
    def __init__(self, player_id, start_pos, symbol):
        super().__init__(player_id, start_pos, symbol)

    def decide_move(self, game, watchtower):
        suggestion = watchtower.get_suggestion(self, game)
        if random.random() < 0.9:  # 90% chance to follow suggestion
            self.direction = suggestion
        else:
            # Randomly choose a valid alternative direction
            x, y = self.position
            directions = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0)
            }
            valid_directions = [
                dir_name for dir_name, (dx, dy) in directions.items()
                if 0 <= x + dx < game.width and 0 <= y + dy < game.height and game.board[y + dy][x + dx] == '..'
            ]
            if valid_directions:
                self.direction = random.choice(valid_directions)
            else:
                self.direction = suggestion

        self.log_decision(self.symbol, suggestion, self.direction)

    def log_decision(self, agent_symbol, suggestion, decision):
        """Loguje decyzję agenta."""
        with open("game_logs.txt", "a") as log_file:
            log_file.write(f"[Agent] Agent {agent_symbol} suggested '{suggestion}', decided on '{decision}'.\n")

class AggressiveAgent(Agent):
    def __init__(self, player_id, start_pos, symbol):
        super().__init__(player_id, start_pos, symbol)

    def decide_move(self, game, watchtower):
        suggestion = watchtower.get_aggressive_suggestion(self, game)
        if random.random() < 0.7:  # 70% chance to follow suggestion
            self.direction = suggestion
        else:
            x, y = self.position
            directions = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0)
            }
            valid_directions = [
                dir_name for dir_name, (dx, dy) in directions.items()
                if 0 <= x + dx < game.width and 0 <= y + dy < game.height and game.board[y + dy][x + dx] == '..'
            ]
            if valid_directions:
                self.direction = random.choice(valid_directions)
            else:
                self.direction = suggestion

        self.log_decision(self.symbol, suggestion, self.direction)
