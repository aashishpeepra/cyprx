
from datetime import date, datetime
import sys
import time
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
import math
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import requests
from utils.destroy import destroy
from threading import Timer
from utils.constants import TRADE_NAME
load_dotenv()


twilioObj = TwilioClient(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
totalRequests = 2
maximumRequests = 90000


def send_message(object, message):
    msg = object.messages.create(
        from_=os.getenv("FROM"),
        body=message,
        to=os.getenv("NUMBER")
    )
    print(msg)


def send_whatsapp_message(msg): return send_message(twilioObj, msg)


client = Client(os.getenv("BINANCE_API_KEY"),
                os.getenv("BINANCE_API_SECRET"), {"timeout": 2000000})


# INFORM WHEN BOT STARTS
CURRENCY = "DOGEUSDT"


# This code will grab the current account details

def return_order_details(order):
    print(order)
    timeValue = ""
    try:
        timeValue = order["time"]
    except:
        timeValue = order["transactTime"]
    if order["status"] == "NEW":
        timeKey = "transactTime"
    heading = ""
    if order["side"] == "SELL":
        heading = "💰"
    else:
        heading = "💲"

    return """
    SYMBOL     : {}
    ORDERID    : {}
    PRICE          : {}
    QUANTITY : {}
    TOTAL         : {}
    TYPE           : {} {}
    TIME           : {}
    """.format(
        order["symbol"],
        order["orderId"],
        "$ "+str(round(float(order["price"]), 7)),
        str(round(float(order["origQty"]), 7)),
        "$ "+str(round(float(order["price"])*float(order["origQty"]), 5)),
        heading,
        order["side"],
        str(datetime.fromtimestamp(timeValue/1000).strftime('%H:%M:%S'))
    )


orders = client.get_open_orders(symbol=CURRENCY)
if len(orders) > 0:
    send_whatsapp_message("🛑 RESOLVING OLD ORDER\n" +
                          return_order_details(orders[0]))

anyPendingOrder = False

if len(orders) == 1:
    startTime = int(time.time())
    while client.get_order(symbol=CURRENCY, orderId=orders[0]["orderId"])["status"] == "NEW":
        print("Waiting for {} order to finish at price {} | {} seconds".format(
            orders[0]["side"], orders[0]["price"], int(time.time())-startTime))
        time.sleep(60)
        totalRequests += 1
    print("Last order processed | continue", orders[0])
    send_whatsapp_message("⌛ Previous order processed!\n"+return_order_details(orders[0]))
    anyPendingOrder = True
elif len(orders) > 1:
    send_whatsapp_message(
        "!important. 2 unfilled orders are there. Killing instance. ")
    sys.exit()

all_orders = client.get_all_orders(symbol=CURRENCY)
print(return_order_details(all_orders[-1]))
finalLast = None
allOrderLength = len(all_orders)-1
i = allOrderLength
while i >= 0:
    if all_orders[i]["status"] == "FILLED":
        finalLast = all_orders[i]
        break
    i -= 1
if all_orders == None:
    send_whatsapp_message("Can't find reliable last order. Killing instance. ")
    sys.exit()


USDT = client.get_asset_balance(asset='USDT')
if USDT != None:
    USDT = float(USDT["free"])
DOGE = client.get_asset_balance(asset="DOGE")
if DOGE != None:
    DOGE = int(float(DOGE["free"]))
print(USDT, DOGE)

# SHOULD REACH HERE ONLY IF NO ORDERS ARE LEFT

start, counter = 0, 0
p, l = 0, 0
balance = USDT-3
brought = DOGE
lastBuy = 0
minQty = 0
if finalLast["side"] == "BUY":
    lastBuy = float(finalLast["price"])
    minQty = int(float(finalLast["origQty"]))
send_whatsapp_message("""
🤖 BOOTING CYPRX 1.0 at {} for trades on {} 🐕
USDT : $ {}
DOGE : {}
""".format(str(datetime.now().strftime('%H:%M:%S')), CURRENCY, USDT, DOGE))
print(balance, brought, lastBuy)


def wait_n_minutes(N):
    start = int(time.time())
    end = N*1000 + start
    while start < end:
        start = int(time.time())


def rounder(data):
    return round(float(data), 7)


def get_new_price(oldPrice, deduction, deductionPrecision=3):
    # deductionPrecision is 3
    length = len(str(oldPrice))-2
    toAdd = length - deductionPrecision
    toAdd = "8"*toAdd
    power = pow(10, deductionPrecision)
    intPart = int((oldPrice-deduction)*power)
    floatPart = intPart / power
    return float(str(floatPart)+toAdd)


def trade(eachTrade):
    global start
    global counter
    global p
    global brought
    global lastBuy
    global l
    global balance
    global totalRequests
    global client
    
    counter += 1
    print(eachTrade["p"])
    # for each in eachTrade:
    #     print(TRADE_NAME[each],":",eachTrade[each])
    if start == 0:
        start = float(eachTrade["p"])
    elif counter >= 50:
        if start < float(eachTrade["p"]):
            p += 1
            if p >= 30:
                # extraPrice = lastBuy
                # if float(eachTrade["p"])>(lastBuy+0.01):
                #     extraPrice = lastBuy
                temp = lastBuy + 0.00353
                temp = round(temp, 7)
                print("Price will rise ", p, temp)
                p = 0
                qty = brought
                if qty < minQty:
                    qty = minQty
                if qty > brought:
                    print("can't buy")
                    return
                if temp*qty < 10:
                    qty += 1
                if qty >= brought:
                    return
                print(qty, temp*qty)
                if temp > lastBuy and brought >= qty:
                    # choice = input("Sell now ? ")
                    choice = "y"
                    if choice == "y":
                        order1 = client.order_limit_sell(
                            symbol=CURRENCY,
                            quantity=qty,
                            price=temp)
                        send_whatsapp_message(
                            "🏦 SELLING CYYPTO\n"+return_order_details(order1))
                        # currentStatus = "NEW"
                        time.sleep(10)
                        while client.get_order(symbol=CURRENCY, orderId=order1["orderId"])["status"] == "NEW":
                            # send_whatsapp_message( "⚡ Some other error occured.")
                            print("processing...", order1)
                            time.sleep(60)
                            totalRequests += 1
                        print("Sold at at {}", eachTrade["p"])
                        send_whatsapp_message(
                            "✅ SELLING CRYPTO DONE\n"+return_order_details(order1))
                        balance += round(temp*qty, 5)
                        brought -= qty
                counter = 0

        else:
            l += 1
            if l >= 30:

                temp = get_new_price(float(eachTrade["p"]), 0.0008, 5)
                print("Price will fall ", l, eachTrade["p"], temp)
                if balance < 10.2:
                    print("cant buy")
                    l = 0
                    return
                # choice = input("buy now ? ")
                choice = "y"
                qty = int(balance/temp)
                if temp*qty < 10:
                    qty += 1

                if choice == "y":
                    order1 = client.order_limit_buy(
                        symbol=CURRENCY,
                        quantity=qty,
                        price=temp
                    )
                    l = 0
                    print(order1)
                    send_whatsapp_message(
                        "💳 BUYING CRYPTO\n"+return_order_details(order1))
                    time.sleep(3)
                    startTime = int(time.time())
                    endTime = startTime + 120
                    becauseOfTime = False
                    while client.get_order(symbol=CURRENCY, orderId=order1["orderId"])["status"] == "NEW":
                        if startTime > endTime:
                            becauseOfTime = True
                            print("Canelling order ")
                            break
                        print("Remaining ", endTime-startTime, " seconds")
                        startTime = int(time.time())
                        time.sleep(5)
                        totalRequests += 1
                    if becauseOfTime:
                        result = client.cancel_order(
                            symbol=CURRENCY,
                            orderId=order1["orderId"])
                        print("Cancelled order due to maximum timeout ", result)
                        send_whatsapp_message(
                            "☠️ CANCELLED ORDER DUE TO TIMEOUT\n"+return_order_details(order1))
                        return
                    send_whatsapp_message(
                        "✅ BUYING CRYPTO DONE\n"+return_order_details(order1))
                    print("Bought at {}", temp)
                    lastBuy = temp
                    brought += qty
                    balance -= (lastBuy*qty)
                    print("Reduced balance ", balance)
                counter = 0
                l = 0


    # print(each)
bm = BinanceSocketManager(client)

# print( client.get_symbol_info(CURRENCY)['filters'][:])
# clientCore.show_account_details("DOGE")


# info = client.get_account()
# print(info)
# #FIRST WILL WAIT FOR OLD ORDERS TO BE FINISHED


# THIS CODE STARTS THE TRADING
def start_code():
    try:
        conn_key = bm.start_trade_socket(CURRENCY, trade)
        print(conn_key)
    except requests.exceptions.ConnectionError:
        print("Connection timeout ")
        client = Client(os.getenv("BINANCE_API_KEY"),
                        os.getenv("BINANCE_API_SECRET"), {"timeout": 2000000})
        send_whatsapp_message(
            "Connection was timed-out. Reconnecting to server.")
        start_code()
    except:
        print("Something else went wrong")
        send_whatsapp_message("Something went wrong. Killing the instance.")

# diff_key = bm.start_depth_socket(CURRENCY, lambda a :print(a))
# print(diff_key)


start_code()
bm.start()


def end_results():
    bm.close()
    send_whatsapp_message(
        "Killing the instance. Have a great day!!"+str(totalRequests))
    destroy()


Timer(2000000, end_results).start()
