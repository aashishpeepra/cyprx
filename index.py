from dotenv import load_dotenv
import os
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
load_dotenv()
import time

# print(os.getenv("recvWindow"))
client =  Client(os.getenv("BINANCE_API_KEY"),os.getenv("BINANCE_API_SECRET"))
print(client)
RECV_WINDOW=60001
orders = client.get_all_orders(symbol='BNBBTC', limit=10,timestamp=int(time.time()*1000),recvWindow=5000)
# order = client.create_order(
#     recvWindow=RECV_WINDOW,
#     symbol='BNBBTC',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=100,
#     price='0.00001')
print(orders)
def show_details(data):
    print("message type ",data["e"],data)

bm = BinanceSocketManager(client,user_timeout=60)
# bm.start_user_socket(show_details)
# bm.start_trade_socket('BNBBTC', show_details)
# conn_key = bm.start_kline_socket('BNBBTC', show_details, interval=KLINE_INTERVAL_30MINUTE)
# conn_key = bm.start_user_socket(show_details)
# conn_key = bm.start_trade_socket('BNBBTC', show_details)
# conn_key = bm.start_trade_socket('BNBBTC', show_details)
bm.start()

# temp = client.create_order(symbol='BNBBTC',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=100,
#     price='0.00001')

# print(client.get_avg_price(symbol="BNBBTC"))
# print(client.get_all_tickers()) # gives all the prices
# print(client.get_all_orders(symbol='BNBBTC', limit=10))
# print(client.get_ticker()[0])
# print(client.get_order_book(symbol='BNBBTC'))
# data = client.get_recent_trades(symbol='BNBBTC')
# print(data[0])
# print(client.get_klines(symbol='BNBBTC',interval="30m"))

# print(client.get_products())
# print(client.get_all_coins_info())
# print(client.get_symbol_info('BNBBTC'))
# data = client.get_exchange_info()
# print(data["symbols"][0])
# print([each["symbol"] for each in data["symbols"]])