import random

class Watchtower:
    def get_suggestion(self, agent, game):
        """
        Suggests a move for the agent while enforcing basic rules.
        """
        suggested_direction = self._evaluate_directions(agent, game)
        # Enforce basic rules
        if not self.is_within_bounds(agent.position, suggested_direction, game):
            # If the suggestion violates rules, default to a valid direction
            suggested_direction = self.get_safe_direction(agent, game)
        return suggested_direction

    def is_within_bounds(self, position, direction, game):
        """
        Checks if a move keeps the agent within bounds.
        """
        x, y = position
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        dx, dy = directions[direction]
        new_x, new_y = x + dx, y + dy
        return 0 <= new_x < game.width and 0 <= new_y < game.height

    def get_safe_direction(self, agent, game):
        """
        Finds a safe direction within bounds.
        """
        x, y = agent.position
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        for direction, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < game.width and 0 <= new_y < game.height and game.board[new_y][new_x] == '..':
                return direction
        # If no safe move, stay in place
        return agent.direction

    def _evaluate_directions(self, agent, game):
        """
        Suggest the best direction based on evaluation.
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
            if 0 <= new_x < game.width and 0 <= new_y < game.height:
                if game.board[new_y][new_x] == '..':
                    score = self.evaluate_move(new_x, new_y, agent, game)
                    if score > best_score:
                        best_score = score
                        best_direction = direction

        return best_direction if best_direction else random.choice(list(directions.keys()))

    def evaluate_move(self, x, y, agent, game):
        """
        Przykładowa funkcja oceny ruchu dla wieży. 
        """
        score = 0
        
        # Więcej punktów za wolne miejsca wokół
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < game.width and 0 <= ny < game.height:
                if game.board[ny][nx] == '..':
                    score += 1  # Wolne pole to +1 punkt

        # Kary za bliskość innych agentów
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)
                if distance == 1:
                    score -= 10  # Bardzo blisko – duża kara
                elif distance == 2:
                    score -= 3   # Blisko – mniejsza kara

        return score

    def get_best_aggressive_move(self, agent, game):
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
            if 0 <= new_x < game.width and 0 <= new_y < game.height:
                # Sprawdzenie, czy nowa pozycja jest pusta
                if game.board[new_y][new_x] == '..':
                    # Ocena ruchu na podstawie agresywnej strategii
                    score = self.evaluate_aggressive_move(new_x, new_y, agent)
                    
                    if score > best_score:
                        best_score = score
                        best_direction = direction
        
        return best_direction if best_direction else random.choice(list(directions.keys()))  # Losowy ruch w braku lepszych opcji

    def evaluate_aggressive_move(self, x, y, agent, game):
        """
        Ocena ruchu dla agresywnego agenta.
        """
        score = 0
        
        # Punkty za bliskość innych graczy (im bliżej, tym lepiej)
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)
                if distance == 1:
                    score += 20  # Bardzo blisko – wysoka premia
                elif distance == 2:
                    score += 5   # Blisko – umiarkowana premia
        
        # Kara za kolizję lub wyjście poza planszę
        if game.board[y][x] != '..':
            score -= 50  # Ryzyko kolizji
        elif not (0 <= x < game.width and 0 <= y < game.height):
            score -= 100  # Wyjście poza planszę
        elif distance > 3:
            score -=1
        
        return score 




