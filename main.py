import os

from binance.client import Client

def get_moving_average(client, symbol, interval, window):
    klines = client.get_historical_klines(symbol, interval, f"{window+1} day ago UTC")
    closes = [float(kline[4]) for kline in klines]
    moving_average = sum(closes[-window:]) / window
    return moving_average

def execute_trades(client, symbol, quantity):
    # get from env var 20 and 50
    ma_20 = get_moving_average(client, symbol, Client.KLINE_INTERVAL_1DAY, 20)
    ma_50 = get_moving_average(client, symbol, Client.KLINE_INTERVAL_1DAY, 50)

    if ma_20 > ma_50:
        # Buy
        client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
    elif ma_20 < ma_50:
        # Sell
        client.create_test_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )

def main():
    client = Client(os.environ.get("API_KEY"), os.environ.get("API_SECRET"))

    while True:
        execute_trades(client, "BTCUSDT", "0.001")

if __name__ == '__main__':
    main()
