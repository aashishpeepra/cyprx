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

# print(os.getenv("recvWindow"))
client =  Client(os.getenv("BINANCE_API_KEY"),os.getenv("BINANCE_API_SECRET"),tld="com")

# print(client)
# RECV_WINDOW=60001
# order = client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)
# print(order)
# orders = client.get_all_orders(symbol='BNBBTC', limit=10)
# order = client.create_order(
#     recvWindow=RECV_WINDOW,
#     symbol='BNBBTC',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=100,
#     price='0.00001')
# print(orders)
globalConstant = {
    "price":2**10,
    "prices":[],
    "max":0,
    "profits":0,
    "orders":[],
    "total":120
}
coins = 0
counter = 0
counter2 = 0

def show_klines_details(eachKlines):
    for id,value in KLINE_NAME["k"].items():
        print(value,":",eachKlines[id])
def show_klines(each):
    return " ".join(each.values())
    return """
    STARTIME : {}
    OPEN : {}
    HIGH : {}
    LOW : {}
    CLOSE : {}
    VOLUME : {}
    CLOSE TIME : {}
    ASSETV: {}
    TRADES : {}
    BUYBASE : {}
    QUOTE BASE : {}
    """.format(each.values()[:-1])
startTime = int(time.time())
print("STARTING AT ",startTime)
endTime = startTime + 30*1000
def show_trade_data(eachTrade,obj):
    global counter
    global coins
    global counter2
    endTime = int(time.time())
    # for each in eachTrade:
    #     print(TRADE_NAME[each],":",eachTrade[each])
    # print(eachTrade["p"])
    if startTime<endTime:
        obj.keep_track(eachTrade)
    # obj.show_details()
    return None
    eachTrade["p"] = float(eachTrade["p"])
    if eachTrade["p"]<globalConstant["price"] and globalConstant["total"]>0:
        if counter>5:
            counter = 0
            buyValue = sum(globalConstant["prices"])/5
            buyValue = round(buyValue,7)
            print("Bidding to buy at price ",globalConstant["price"],globalConstant)
            # sys.exit()
            # globalConstant["price"] = sum(globalConstant["prices"])/5
            globalConstant["prices"] = []
            coins+=40
            globalConstant["profits"]-=40*globalConstant["price"]
            globalConstant["total"]-=40*globalConstant["price"]
            order = client.create_test_order(
            symbol='DOGEUSDT',
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=40,
            price=globalConstant["price"])
            globalConstant["orders"].append(order)
            globalConstant["total"] -= 40*globalConstant["price"]
        globalConstant["price"] = eachTrade["p"]
        globalConstant["prices"].append(eachTrade['p'])
        counter+=1
    elif eachTrade["p"] > globalConstant["max"] and coins>0:

        globalConstant["max"] = eachTrade["p"]
        if counter2 >5:
            print("Wants to " if coins==0 else "","Bidding to sell at ",globalConstant["max"])
            counter2 = 0
            coins-=40
            order = client.create_test_order(
            symbol='DOGEUSDT',
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=40,
            price=globalConstant["max"])
            globalConstant["orders"].append(order)
            globalConstant["total"] += 40*globalConstant["max"]
            if coins>0:
                globalConstant["profits"]+=40*globalConstant["max"]
        counter2+=1
    # print("*"*10)
def show_details(data):
    print("message type ",data["e"],data["E"])
    show_klines_details(data["k"])
    print("*"*20)

# candles = client.get_klines(symbol='DOGEUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
# print(candles[-1])
# trades = client.get_recent_trades(symbol='DOGEUSDT')
# print()
# client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
bm = BinanceSocketManager(client,user_timeout=60)
# bm.start_user_socket(show_details)


#code to check the klines
# conn_key = bm.start_kline_socket('DOGEUSDT', show_details, interval=KLINE_INTERVAL_30MINUTE)
# print(conn_key)

#code to checkout the buy and sell trades
clientCore = Core(client,120,"LTCUSDT")
minimumModel = MinLasts(120,0.4,clientCore)

conn_key = bm.start_trade_socket('LTCUSDT', lambda a:show_trade_data(a,minimumModel))
print(conn_key)
print( client.get_symbol_info('LTCUSDT')['filters'][0])

#code to check the ticker
# conn_key = bm.start_symbol_ticker_socket('DOGEUSDT', lambda a :print(a["c"]))
# print(conn_key)

# bm.start_trade_socket('BNBBUSD', show_details)
# conn_key = bm.start_kline_socket('BNBBTC', show_details, interval=KLINE_INTERVAL_30MINUTE)
# conn_key = bm.start_user_socket(show_details)
# conn_key = bm.start_trade_socket('BNBBTC', show_details)
# conn_key = bm.start_trade_socket('BNBBTC', show_details)
bm.start()
time.sleep(30)
bm.close()
minimumModel.show_details()
clientCore.show_orders()
clientCore.show_account_details("LTC")
destroy() # Destroys everything
# print("Profit is ",globalConstant["profits"])
# print(client.get_account())
# print(client.get_asset_balance("DOGE"))
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