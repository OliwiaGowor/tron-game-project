import unittest
from game import Game
from agent import Player, Agent, AggressiveAgent
from watchtower import Watchtower


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(1, (5, 5), 'P')

    def test_initialization(self):
        self.assertEqual(self.player.id, 1)
        self.assertEqual(self.player.position, (5, 5))
        self.assertEqual(self.player.symbol, 'P')
        self.assertFalse(self.player.crashed)

    def test_move_up(self):
        self.player.direction = "UP"
        self.player.move()
        self.assertEqual(self.player.position, (5, 4))

    def test_move_down(self):
        self.player.direction = "DOWN"
        self.player.move()
        self.assertEqual(self.player.position, (5, 6))

    def test_move_left(self):
        self.player.direction = "LEFT"
        self.player.move()
        self.assertEqual(self.player.position, (4, 5))

    def test_move_right(self):
        self.player.direction = "RIGHT"
        self.player.move()
        self.assertEqual(self.player.position, (6, 5))


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.game = Game(10, 10, [])
        self.watchtower = Watchtower()
        self.agent = Agent(2, (5, 5), 'A')

    def test_decide_move_follow_suggestion(self):
        self.watchtower.get_suggestion = lambda agent, game: "UP"
        self.agent.decide_move(self.game, self.watchtower)
        self.assertEqual(self.agent.direction, "UP")

    def test_decide_move_random_choice(self):
        self.watchtower.get_suggestion = lambda agent, game: "UP"
        self.agent.decide_move(self.game, self.watchtower)
        self.assertIn(self.agent.direction, ["UP", "DOWN", "LEFT", "RIGHT"])


class TestAggressiveAgent(unittest.TestCase):
    def setUp(self):
        self.game = Game(10, 10, [])
        self.watchtower = Watchtower()
        self.agent = AggressiveAgent(3, (5, 5), 'A')

    def test_decide_move_aggressive_suggestion(self):
        self.watchtower.get_aggressive_suggestion = lambda agent, game: "DOWN"
        self.agent.decide_move(self.game, self.watchtower)
        self.assertEqual(self.agent.direction, "DOWN")


class TestWatchtower(unittest.TestCase):
    def setUp(self):
        self.game = Game(10, 10, [])
        self.agent = Agent(2, (5, 5), 'A')
        self.watchtower = Watchtower()

    def test_get_safe_direction(self):
        self.game.board[4][5] = '..'
        self.assertEqual(self.watchtower.get_safe_direction(self.agent, self.game), "UP")

    def test_evaluate_move(self):
        score = self.watchtower.evaluate_move(5, 5, self.agent, self.game)
        self.assertIsInstance(score, int)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.players = [Player(1, (0, 0), 'P1')]
        self.game = Game(5, 5, self.players)

    def test_board_initialization(self):
        self.assertEqual(len(self.game.board), 5)
        self.assertEqual(len(self.game.board[0]), 5)

    def test_random_empty_position(self):
        pos = self.game.random_empty_position()
        self.assertTrue(0 <= pos[0] < 5 and 0 <= pos[1] < 5)
        self.assertEqual(self.game.board[pos[1]][pos[0]], '..')

    def test_update_player_move(self):
        player = Player(1, (0, 0), 'P1')
        self.game.players.append(player)
        player.direction = "RIGHT"
        self.game.update()
        self.assertEqual(player.position, (1, 0))
        self.assertEqual(self.game.board[0][1], 'P1')

    def test_all_players_crashed(self):
        self.game.players[0].crashed = True
        self.assertTrue(self.game.all_players_crashed())


if __name__ == "__main__":
    unittest.main()
