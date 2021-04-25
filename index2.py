from binance.client import Client
from dotenv import load_dotenv
import os
load_dotenv()
KEY = os.environ["BINANCE_API_KEY"]
SECRET = (os.environ["BINANCE_API_SECRET"])
import time
client =Client(KEY,SECRET)
temp = client.get_account_snapshot(type="SPOT")

print(temp)
print("logged in")