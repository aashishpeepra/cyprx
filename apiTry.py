# code to place order

import requests
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import time
import json
from requests.api import head
load_dotenv()
def dict_to_byte_string(body):
    # converts ict to str
    output = ""
    maxer = len(body.values())
    i = 0
    for a,b in body.items():
        output+=str(a)+"="+str(b)
        if i>=maxer-1:
            continue
        i+=1
        output+="&"
    print(output)
    return output.encode("utf-8")
def generate_hash_from_string(integer, string):
    digest = hmac.new(integer, msg=string, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode()
def current_timestamp():
    return int(time.time()*1000)
BASE_API = "https://api.binance.com/api/v3/"
SECRET_KEY = os.environ["BINANCE_API_KEY"]
SECRET_NUMBER = os.environ["BINANCE_API_SECRET"]
body = {"symbol":"LTCBTC","side":"BUY","type":"LIMIT","timeInForce":"GTC","quantity":"1","price":"0.1","recvWindow":"5000","timestamp":current_timestamp()}
hashedValue = generate_hash_from_string(str(SECRET_NUMBER).encode("utf-8"),dict_to_byte_string(body))

headers = {
    'X-MBX-APIKEY': SECRET_KEY,
    "content-type":"application/x-www-form-urlencoded"
}
print(hashedValue)
# HashedToken = hmac.new(SECRET_NUMBER,body)
body.update({"signature":hashedValue})
res = requests.post(BASE_API+"order",headers=headers,data=body)
print(res.content,res.status_code,res.json(),res.content)
