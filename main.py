from binance.client import Client

import os

import logging
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_moving_average(client, symbol, interval, window):
    klines = client.get_historical_klines(symbol, interval, f"{window+1} day ago UTC")
    closes = [float(kline[4]) for kline in klines]
    moving_average = sum(closes[-window:]) / window
    return moving_average

def execute_trades(client, symbol, quantity, fast_ma_days, slow_ma_days):
    fast_ma = get_moving_average(client, symbol, Client.KLINE_INTERVAL_1DAY, fast_ma_days)
    slow_ma = get_moving_average(client, symbol, Client.KLINE_INTERVAL_1DAY, slow_ma_days)

    if fast_ma > slow_ma:
        # Buy
        client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logger.info("Bought")
    elif fast_ma < slow_ma:
        # Sell
        client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logger.info("Sold")

def main():
    client = Client(os.environ.get("API_KEY"), os.environ.get("API_SECRET"))

    fast_ma_days = int(os.environ.get("FAST_MA_DAYS"))
    slow_ma_days = int(os.environ.get("SLOW_MA_DAYS"))

    while True:
        execute_trades(client, "BTCUSDT", "0.001", fast_ma_days, slow_ma_days)

if __name__ == '__main__':
    main()
