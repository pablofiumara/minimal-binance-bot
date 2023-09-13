import unittest
from unittest.mock import MagicMock, Mock, patch
from decimal import Decimal

from binance.client import Client

from main import MovingAverageStrategy

class MovingAverageStrategyTests(unittest.TestCase):
    def setUp(self):
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

        result = self.strategy.get_moving_average(client, "BTCUSDT", "1d", 5)

        self.assertEqual(result, Decimal("3"))

    @patch("binance.client.Client")
    def test_execute_trades(self, mocked_binance_client):

        with self.subTest("should buy when fast MA value is higher than slow MA value"):
            # side effect: [fast_MA, slow_MA]
            self.strategy.get_moving_average = MagicMock(side_effect=[Decimal("130"), Decimal("120")])

            self.strategy.execute_trades(mocked_binance_client, "BTCUSDT", "0.001", 5, 10)

            mocked_binance_client.create_test_order.assert_called_with(
                symbol="BTCUSDT",
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity="0.001"
            )

        with self.subTest("should sell when fast MA value is less than slow MA value"):
            # side effect: [fast_MA, slow_MA]
            self.strategy.get_moving_average = MagicMock(side_effect=[Decimal("120"), Decimal("130")])

            self.strategy.execute_trades(mocked_binance_client, "BTCUSDT", "0.001", 5, 10)

            mocked_binance_client.create_test_order.assert_called_with(
                symbol="BTCUSDT",
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity="0.001"
            )

        mocked_binance_client.reset_mock()
        with self.subTest("should not buy or sell when fast MA value is equal to slow MA value"):
            # side effect: [fast_MA, slow_MA]
            self.strategy.get_moving_average = MagicMock(side_effect=[Decimal("120"), Decimal("120")])

            self.strategy.execute_trades(mocked_binance_client, "BTCUSDT", "0.001", 5, 10)

            mocked_binance_client.create_test_order.assert_not_called()

if __name__ == '__main__':
    unittest.main()