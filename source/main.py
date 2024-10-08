import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *

import config, RSI_Trade01, order_actions

# tld: "us" for usa based IP and "com" for global.
client = Client(config.API_KEY, config.API_SECRET, tld="com")


# Get data from binance. graph: "ltcbusd"(change this in config.), timeframe: 1m
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_1m".format(
    config.TRADE_SYMBOL.lower()
)


# this is the array for storing closed candle values gathered from socket.
closes = []


def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global closes

    print("received message")
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    # look-up the payload of the websocket stream on here https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
    candle = json_message["k"]

    is_candle_closed = candle["x"]
    price_closed = candle["c"]
    print(price_closed)
    # initiate logic upon new candle information.
    if is_candle_closed:
        print("candle closed at {}".format(price_closed))
        closes.append(float(price_closed))
        print("closes")
        print(closes)
        RSI_Trade01.calculate_trade(client=client, closes=closes)


# Get updates from socket.
ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message
)

ws.run_forever()
