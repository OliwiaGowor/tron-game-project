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
        Function to evaluate move
        """
        score = 0
        
        # More points for empty fields around
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < game.width and 0 <= ny < game.height:
                if game.board[ny][nx] == '..':
                    score += 1  # Wolne pole to +1 punkt

        # Penalty for other agents being near
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)
                if distance == 1:
                    score -= 10  # Very close - big penalty
                elif distance == 2:
                    score -= 3   # Close - moderate penalty

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
            
            # Check of new position is in the board
            if 0 <= new_x < game.width and 0 <= new_y < game.height:
                # Check if new position is empty
                if game.board[new_y][new_x] == '..':
                    # Evaluate move based on aggressive strategy
                    score = self.evaluate_aggressive_move(new_x, new_y, agent)
                    
                    if score > best_score:
                        best_score = score
                        best_direction = direction
        
        return best_direction if best_direction else random.choice(list(directions.keys()))  # Random move if no better options

    def evaluate_aggressive_move(self, x, y, agent, game):
        """
        Evaluate move for aggressive agent 
        """
        score = 0
        
        # Points for other agents being near (the closer, the better)
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)
                if distance == 1:
                    score += 20  # Very close - big bonus
                elif distance == 2:
                    score += 5   # Close - moderate bonus
        
        # Penalty for collision or going out of bounds
        if game.board[y][x] != '..':
            score -= 50  # Risk of collision 
        elif not (0 <= x < game.width and 0 <= y < game.height):
            score -= 100  # Out of bounds
        elif distance > 3:
            score -=1
        
        return score 




