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
    
    def get_aggressive_suggestion(self, agent, game):
        """
        Suggests a move for the agent while enforcing basic rules.
        """
        agg_suggested_direction = self._evaluate_directions_aggressive(agent, game)
        # Enforce basic rules
        if not self.is_within_bounds(agent.position, agg_suggested_direction, game):
            # If the suggestion violates rules, default to a valid direction
            agg_suggested_direction = self.get_best_aggressive_move(agent, game)
        return agg_suggested_direction

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
    
    def _evaluate_directions_aggressive(self, agent, game):
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
                    score = self.evaluate_aggressive_move(new_x, new_y, agent, game)
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

            # Check if the new position is within the game board
            if 0 <= new_x < game.width and 0 <= new_y < game.height:
                # Check if the new position is empty
                if game.board[new_y][new_x] == '..':
                    # Evaluate the move based on aggressive strategy
                    score = self.evaluate_aggressive_move(new_x, new_y, agent, game)

                    if score > best_score:
                        best_score = score
                        best_direction = direction

        return best_direction if best_direction else random.choice(list(directions.keys()))  # Random move if no better options

    def evaluate_aggressive_move(self, x, y, agent, game):
        """
        Evaluates a move for the aggressive agent.
        """
        score = 0

        # Reward for proximity to opponents (the closer, the better)
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                distance = abs(ox - x) + abs(oy - y)

                if distance == 1:
                    score += 30  # Very close - highest reward
                elif distance == 2:
                    score += 10  # Moderate reward
                elif distance == 3:
                    score += 2   # Minimal reward

                # Additional reward for limiting the opponent's moves
                if distance == 1:
                    score += self.evaluate_trap_potential(x, y, ox, oy, game)

        # Penalty for choosing a field near the edge of the board (less maneuverability)
        if x == 0 or x == game.width - 1 or y == 0 or y == game.height - 1:
            score -= 5

        # Penalty for selecting a move that increases distance from the opponent
        for other_agent in game.players:
            if other_agent.id != agent.id and not other_agent.crashed:
                ox, oy = other_agent.position
                prev_distance = abs(ox - agent.position[0]) + abs(oy - agent.position[1])
                new_distance = abs(ox - x) + abs(oy - y)
                if new_distance > prev_distance:
                    score -= 5  # Penalty for moving away from the opponent

        return score

    def evaluate_trap_potential(self, x, y, ox, oy, game):
        """
        Evaluates the potential to trap an opponent.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        trapped_count = 0

        for dx, dy in directions:
            nx, ny = ox + dx, oy + dy
            if not (0 <= nx < game.width and 0 <= ny < game.height) or game.board[ny][nx] != '..':
                trapped_count += 1

        # If the opponent is surrounded on 3 sides, it's a great move
        if trapped_count >= 3:
            return 20
        elif trapped_count == 2:
            return 10
        return 0




