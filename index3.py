from dotenv import load_dotenv
import os
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from utils.constants import KLINE_NAME
from utils.constants import TRADE_NAME
load_dotenv()
import time
from strategies.minlasts import MinLasts
from models.core import Core
from utils.destroy import destroy
from threading import Timer, current_thread
CURRENCY = "DOGEUSDT"
# print(os.getenv("recvWindow"))
client =  Client(os.getenv("BINANCE_API_KEY"),os.getenv("BINANCE_API_SECRET"),tld="com")
STARTTIME = int(time.time())
ENDTIME = STARTTIME + 6000*1000 
def show_trade_data(eachTrade,obj):
    STARTTIME = int(time.time())
    if STARTTIME<ENDTIME:
        obj.keep_track(eachTrade)
bm = BinanceSocketManager(client,user_timeout=60)
clientCore = Core(client,11,CURRENCY)
minimumModel = MinLasts(11,40,clientCore,10,1)
# clientCore.show_account_details("DOGE")
conn_key = bm.start_trade_socket(CURRENCY, lambda a:show_trade_data(a,minimumModel))
print(conn_key)
# print(client.get_trade_fee(symbol=CURRENCY))
# print(client.get_account())
# print(client.get_open_orders())
# print(client.get_all_orders(symbol=CURRENCY))
# print( client.get_symbol_info(CURRENCY)['filters'][:])
# conn =bm.start_user_socket(lambda a:print(a))
# print(conn)
bm.start()
def end_results():
    bm.close()
    minimumModel.show_details()
    clientCore.show_orders()
    destroy()
Timer(6000,end_results).start()
