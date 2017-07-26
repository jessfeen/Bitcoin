import requests
from bs4 import BeautifulSoup
import time
import urllib
import json
from datetime import datetime as dt

r=requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR,GBP")
c=r.content
soup=BeautifulSoup(c,"html.parser")
value=soup.find_all("span",{"class":"choiceValue"})
print(value)

import urllib.request, json
import time, threading
import pyodbc

conn = pyodbc.connect(r'DSN=BitcoinTwitter')
curr = conn.cursor()


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            with urllib.request.urlopen(
                    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR,GBP") as url:
                data = url.read().decode()  # .json_t*json_string()
                BTC = data.split(':')[1].split(',')[0]
                USD = data.split(':')[2].split(',')[0]
                EUR = data.split(':')[3].split(',')[0]
                GBP = data.split(':')[4].split(',')[0].split('}')[0]
                datetime = dt.now().strftime('%Y''-''%m''-''%d''  ''%X')
                date = dt.now().strftime('%Y''-''%m''-''%d')
                time = dt.now().strftime('%X')
                print(BTC)
                print(USD)
                print(EUR)
                print(GBP)
                curr.execute(
                    "INSERT INTO BitcoinRate2 ( BTC , USD , EUR , GBP, datetime, date, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    BTC, USD, EUR, GBP, datetime, date, time)
                conn.commit()
                self.event.wait(30)

    def stop(self):
        self.event.set()


tmr = Timer()
tmr.start()

