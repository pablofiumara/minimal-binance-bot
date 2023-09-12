import unittest
from unittest.mock import MagicMock, Mock
from decimal import Decimal

from binance.client import Client

from main import MovingAverageStrategy

class MovingAverageStrategyTests(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock(spec=Client)
        self.strategy = MovingAverageStrategy()

    
    def test_get_moving_average(self):
        client = Mock()
        client.get_historical_klines.return_value = [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 3],
            [0, 0, 0, 0, 4],
            [0, 0, 0, 0, 5],
        ]

        strategy = MovingAverageStrategy()
        result = strategy.get_moving_average(client, 'BTCUSDT', '1d', 5)

        self.assertEqual(result, Decimal("3.0"))

if __name__ == '__main__':
    unittest.main()