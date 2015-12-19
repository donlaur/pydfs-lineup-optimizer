import unittest
from pydfs_lineup_optimizer.lineup_optimizer import LineupOptimizer
from pydfs_lineup_optimizer.player import Player
from pydfs_lineup_optimizer import settings


class TestLineupOptimizer(unittest.TestCase):
    def setUp(self):
        self.lineup_optimizer = LineupOptimizer(settings.YahooDailyFantasyBasketballSettings)
        self.lineup_optimizer.load_players_from_CSV("tests/yahoo_dfs_test_sample.csv")
        self._player1 = self.lineup_optimizer._players[0]

    def test_add_player_to_lineup(self):
        self.lineup_optimizer.reset_lineup()
        self.lineup_optimizer.add_player_to_lineup(self._player1)
        self.assertTrue(self._player1 in self.lineup_optimizer._lineup)

    def test_same_players_in_lineup(self):
        self.lineup_optimizer.reset_lineup()
        self.lineup_optimizer.add_player_to_lineup(self._player1)
        self.assertFalse(self.lineup_optimizer.add_player_to_lineup(self._player1))

    def test_adding_player_with_salary_bigger_than_budget(self):
        self.lineup_optimizer.reset_lineup()
        player = Player('', '', 'PG', 'DEN', 'SAC', 100000, 2)
        self.assertFalse(self.lineup_optimizer.add_player_to_lineup(player))

    def test_adding_player_to_formed_lineup(self):
        self.lineup_optimizer.reset_lineup()
        self.lineup_optimizer.optimize()
        self.assertFalse(self.lineup_optimizer.add_player_to_lineup(self._player1))

    def test_adding_player_to_formed_position(self):
        self.lineup_optimizer.reset_lineup()
        players = []
        for i in 'abcd':
            players.append(Player(i, i, 'PG', 'DEN', 'SAC', 10, 2))
        for i in range(3):
            self.lineup_optimizer.add_player_to_lineup(players[i])
        self.assertFalse(self.lineup_optimizer.add_player_to_lineup(players[3]))

    def test_remove_player_from_lineup(self):
        self.lineup_optimizer.reset_lineup()
        player1 = Player('P', 'P', 'PG', 'DEN', 'SAC', 10, 2)
        player2 = Player('C', 'C', 'PG', 'DEN', 'SAC', 10, 2)
        player3 = Player('P', 'P', 'PG', 'DEN', 'SAC', 10, 2)
        self.lineup_optimizer.add_player_to_lineup(player1)
        self.lineup_optimizer.remove_player_from_lineup(player1)
        self.assertEqual(len(self.lineup_optimizer._lineup), 0)
        self.lineup_optimizer.add_player_to_lineup(player1)
        self.lineup_optimizer.add_player_to_lineup(player2)
        self.lineup_optimizer.add_player_to_lineup(player3)
        self.lineup_optimizer.remove_player_from_lineup(player1)
        self.assertEqual(self.lineup_optimizer._positions[('PG', )], 0)
        self.assertEqual(self.lineup_optimizer._positions[('PG', 'SG')], 1)
        self.lineup_optimizer.remove_player_from_lineup(player2)
        self.assertEqual(self.lineup_optimizer._positions[('PG', )], 0)
        self.assertEqual(self.lineup_optimizer._positions[('PG', 'SG')], 2)
        self.lineup_optimizer.remove_player_from_lineup(player3)
        self.assertEqual(self.lineup_optimizer._positions[('PG', )], 1)
        self.assertEqual(self.lineup_optimizer._positions[('PG', 'SG')], 3)


if __name__ == '__main__':
    unittest.main()