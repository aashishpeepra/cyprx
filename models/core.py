from binance.client import Client
from binance.enums import *
class Core():
    def __init__(self,client,balance,currency) -> None:
        self.client = client
        self.coins = 0
        self.balance = balance
        self.currency = currency
        self.orders = []
        self.actualOrders = []
    def can_place_order(self,order):
        if order["type"] == "BUY":
            return (order["price"] * order["quantity"]) < self.balance
        else:
            return (self.coins >= order["quantity"])
    def get_order_status(self,id):
        return self.client.get_order(symbol=self.currency,orderId=id)["status"]
    def place_order(self,order):
        side = SIDE_SELL if order["type"] == "SELL" else SIDE_BUY
        print(self.client.get_symbol_info(self.currency)['filters'][0])
        print(order)
        buyFunc = self.client.order_limit_buy
        sellFunc = self.client.order_limit_sell
        toUse = buyFunc if order["type"] == "BUY" else sellFunc
        order1 = 0
        try:
            order1 = toUse(
                symbol=self.currency,
                quantity=order["quantity"],
                price=order["price"]
            ) 
        except :
            print("Error while placing the order") 
        # order1 = self.client.create_test_order(
        #     symbol=self.currency,
        #     side=side,
        #     type=ORDER_TYPE_LIMIT,
        #     timeInForce=TIME_IN_FORCE_GTC,
        #     quantity=order["quantity"],
        #     price=order["price"])
        print("orderId",order1)
        self.orders.append(order1)
        if order["type"] == "SELL":
            self.coins-=order["quantity"]
        else:
            self.coins+=order["quantity"]
        return order1["orderId"]
    def show_price_info(self):
        res = self.client.get_avg_price(symbol=self.currency)
        print(res["price"])
        return float(res["price"])
    def show_orders(self):
        print("internally orders are ")
        for each in self.orders:
            print(each)
    def show_account_details(self,name):
        # print(self.client.get_account())
        print(self.client.get_all_orders(symbol=self.currency))
        print(self.client.get_asset_balance(name))

    