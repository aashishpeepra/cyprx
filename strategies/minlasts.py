
import time
import random
import math
from binance.client import Client
from utils.destroy import destroy
class MinLasts():
    def __init__(self,balance,quantity,clientCore,minOrderPrice,skip):
        self.trades = []
        self.orders = []
        self.balance = balance
        self.BLOCK_SIZE = 5
        self.quantity = quantity
        self.mode = "BUY"
        self.waiting = False
        self.startAmount = self.balance
        self.coins = 0
        self.minOrderPrice = minOrderPrice
        # self.minQty = minQty
        self.canCall = True
        self.clientCore = clientCore
        self.skip = skip
        self.counter = 0
    def round_price(self,price):
        return round(price,7)
    def filter_for_price(self,trades):
        return [each["price"] for each in trades]
    def place_order(self,price,quantity,type):
        temp = {"type":type,"quantity":quantity,"price":price,"accepted":False,"id":random.randint(1,1000)}
        if self.clientCore.can_place_order(temp):
            
            print("Account details ")
            self.clientCore.show_account_details("DOGE")
            self.clientCore.show_price_info()
            print("Placing order {} Do you agree y/n".format(temp))
            choice = input("enter choice : ")
            if choice == "y":
                print("Order placed ",price,quantity,type)
                self.orders.append(temp)
                self.post_order_processing(temp["id"])
                self.waiting = True
                orderId = self.clientCore.place_order(temp)
                while self.clientCore.get_order_status(orderId) == "NEW":
                    print("processing order {} with details {}".format(orderId,temp))
                    time.sleep(1)
                print("ORDER {} PROCESSED {}".format(orderId,temp))
            else:
                print("Order skipped do you wanna continue ? ")
                choice = input("Choice y/n : ")
                if choice == "n":
                    destroy()
                else:
                    print("conitnuing the process ")

        else:
            print("can't place the order ",temp)
    def choose_transaction_type(self):
        if self.waiting[0] == "NONE" and self.waiting[1] == "NONE":
            return "BUY"
        elif self.waiting[0] == "BUY" and self.waiting[1] == "NONE":
            return "SELL"
        elif self.waiting[0] == "SELL" and self.waiting[1] == "BUY":
            return "BUY"
    def last_buy_price(self):
        if len(self.orders) == 0 and self.skip == 1:
            return 0
        length = len(self.orders)-1
        while length>=0:
            if self.orders[length]["type"] == "BUY":
                return self.orders[length]["price"]
            length-=1
        return 0
    def show_buy_price(self):
        lastestPrice = self.round_price(sum(self.filter_for_price(self.trades[-10:])) / 10)
        MINIMUM = self.round_price(sum(self.filter_for_price(self.trades))/len(self.trades))
        if lastestPrice <= MINIMUM:
            return lastestPrice
        else:
            return MINIMUM
    def keep_track(self,eachOrder):
        # if eachOrder["m"] == True:
        self.trades.append({"price":float(eachOrder["p"]),"time":eachOrder["T"]})
        # print(self.orders)
        # print("I'mlengthj",len(self.trades))
        if len(self.trades)==100:
            MINIMUM = self.show_buy_price()
            MAXIMUM = max(self.filter_for_price(self.trades))
            print(MAXIMUM)
            # print("checking for ",self.waiting,self.mode,self.coins,self.mode == "SELL" , self.waiting == False , self.coins>=self.quantity)
            
            if self.mode == "BUY"  and MINIMUM*self.quantity<=self.balance and (self.skip == 1 and self.counter>0) :
                quantity = math.ceil(self.minOrderPrice / MINIMUM)
                sendQty = self.quantity
                if quantity > self.quantity:
                    sendQty = quantity

                self.place_order(MINIMUM,sendQty,"BUY")
            elif self.mode == "SELL"  and ((self.coins>=self.quantity) or (self.skip==1 and self.counter==0)) and MAXIMUM > self.last_buy_price():
                print("sold")
                
                # time.sleep(5)
                self.place_order(MAXIMUM,self.quantity,"SELL")
                self.counter=1
            
            self.trades = self.trades[50:]
    def show_details(self):
        print("Total balance ",self.balance)
        print("TOTAL COINS ",self.coins)
        print("COIN PRICE ",self.coins*self.orders[-1]["price"])
        self.balance+=self.coins*self.orders[-1]["price"]
        print("Total Profit/Loss ",-self.startAmount+self.balance)
        print("Total orders {} ".format(len(self.orders)))
        # print("Total ")
        print("All Transactions : ")
        # print("TOTAL BUYS ")
        for each in self.orders:
            print(each["type"],each["price"],end = " | ")
        # for each in self.orders[:10]:
        #     print("""
        #     TYPE: {}
        #     PRICE: {}
        #     QUANTITY: {}
        #     ACCEPTED: {}
        #     """.format(each["type"],each["price"],each["quantity"],each["accepted"]))
    
    def set_to_processed(self,id):
        print(id)
        for i in range(len(self.orders)):
            if self.orders[i]["id"] == id:
                self.orders[i]["accepted"] = True
                if self.orders[i]["type"] == "BUY":
                    self.balance -= self.round_price(self.orders[i]["price"]*self.orders[i]["quantity"])
                    self.coins+=self.orders[i]["quantity"]
                else:
                    self.balance += self.round_price(self.orders[i]["price"]*self.orders[i]["quantity"])
                    self.coins-=self.orders[i]["quantity"]
                self.mode = "SELL" if self.orders[i]["type"] == "BUY" else "BUY"
                self.waiting = False
    def post_order_processing(self,id):
        self.canCall = False
        time.sleep(10)
        self.canCall = True
        self.set_to_processed(id)
        # threading.Timer(2.0,self.set_to_processed(id)).start()
        
