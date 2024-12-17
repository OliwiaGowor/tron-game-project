import unittest
import os
import random
import sys
import importlib.util

# Add project directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dynamic import of project modules
def import_module(module_name):
    module_path = os.path.join(os.path.dirname(__file__), '..', f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import modules
game_module = import_module('game')
agent_module = import_module('agent')
watchtower_module = import_module('watchtower')

class TestGridGame(unittest.TestCase):
    def setUp(self):
        """Set up a fresh game environment before each test."""
        self.board_size = 20
        self.game = game_module.Game(self.board_size, self.board_size, [])
        self.watchtower = watchtower_module.Watchtower()

    def test_game_initialization(self):
        """Test that the game is initialized correctly."""
        # Check board dimensions
        self.assertEqual(len(self.game.board), self.board_size)
        self.assertEqual(len(self.game.board[0]), self.board_size)
        
        # Check initial board state
        empty_board = all(cell == '..' for row in self.game.board for cell in row)
        self.assertTrue(empty_board)

    def test_player_initialization(self):
        """Test player initialization on the board."""
        # Create players
        player1 = agent_module.Player(1, self.game.random_empty_position(), 'P1')
        player2 = agent_module.Agent(2, self.game.random_empty_position(), 'A1')
        
        # Explicitly add players to the game
        self.game.players = [player1, player2]
        
        # Manually update the board with player positions
        for player in self.game.players:
            x, y = player.position
            self.game.board[y][x] = player.symbol
        
        # Check players are placed on different positions
        player_positions = {player.position for player in self.game.players}
        self.assertEqual(len(player_positions), 2)
        
        # Check board reflects player positions
        for player in self.game.players:
            x, y = player.position
            self.assertEqual(self.game.board[y][x], player.symbol)

    def test_player_movement(self):
        """Test basic player movement mechanics."""
        player = agent_module.Player(1, (10, 10), 'P1')
        
        # Test each direction
        test_cases = [
            ("UP", (10, 9)),
            ("DOWN", (10, 11)),
            ("LEFT", (9, 10)),
            ("RIGHT", (11, 10))
        ]
        
        for direction, expected_pos in test_cases:
            player.direction = direction
            player.move()
            self.assertEqual(player.position, expected_pos)
            # Reset position for next test
            player.position = (10, 10)

    def test_agent_decision_making(self):
        """Test agent decision-making process."""
        # Create game with multiple agents
        agents = [
            agent_module.Agent(1, self.game.random_empty_position(), 'A1'),
            agent_module.AggressiveAgent(2, self.game.random_empty_position(), 'A2')
        ]
        self.game.players = agents
        
        # Test each agent's decision-making
        for agent in agents:
            original_direction = agent.direction
            agent.decide_move(self.game, self.watchtower)
            
            # Ensure a decision was made
            self.assertIsNotNone(agent.direction)
            
            # Check that the direction is valid (UP, DOWN, LEFT, RIGHT)
            valid_directions = {"UP", "DOWN", "LEFT", "RIGHT"}
            self.assertIn(agent.direction, valid_directions)

    def test_game_boundary_conditions(self):
        """Test game behavior at board boundaries."""
        player = agent_module.Player(1, (0, 0), 'P1', direction="LEFT")
        self.game.players = [player]
        
        # Move player to trigger boundary crash
        player.move()
        self.game.update()
        
        # Player should be marked as crashed
        self.assertTrue(player.crashed)

    def test_logging_functionality(self):
        """Test that game logging works correctly."""
        # Clear existing log
        log_path = "game_logs.txt"
        if os.path.exists(log_path):
            os.remove(log_path)
        
        # Create a game and trigger some logging
        game = game_module.Game(10, 10, [])
        game.log_event("Test logging event")
        
        # Check log file was created and contains the event
        self.assertTrue(os.path.exists(log_path))
        
        with open(log_path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn("Test logging event", log_contents)

    def test_watchtower_suggestion(self):
        """Test watchtower's move suggestion mechanism."""
        agent = agent_module.Agent(1, (10, 10), 'A1')
        self.game.players = [agent]
        
        # Get suggestion and validate
        suggestion = self.watchtower.get_suggestion(agent, self.game)
        
        # Suggestion should be a valid direction
        valid_directions = {"UP", "DOWN", "LEFT", "RIGHT"}
        self.assertIn(suggestion, valid_directions)

    def test_aggressive_agent_strategy(self):
        """Test aggressive agent's specific decision-making."""
        aggressive_agent = agent_module.AggressiveAgent(1, self.game.random_empty_position(), 'AA')
        other_agents = [
            agent_module.Agent(2, self.game.random_empty_position(), 'A1'),
            agent_module.Agent(3, self.game.random_empty_position(), 'A2')
        ]
        self.game.players = [aggressive_agent] + other_agents
        
        # Get aggressive suggestion
        suggestion = self.watchtower.get_aggressive_suggestion(aggressive_agent, self.game)
        
        # Validate suggestion
        valid_directions = {"UP", "DOWN", "LEFT", "RIGHT"}
        self.assertIn(suggestion, valid_directions)

def run_tests():
    """Run all tests and print results."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGridGame)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with non-zero code if tests fail
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    run_tests()