

import tweepy
import json
import pyodbc
from tweepy.streaming import StreamListener
from tweepy import Stream
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("twitterbitcoinscraper@gmail.com", "rubixkubrick")

apikey = '3crXZR1XLBQ25WXr1bqsVlyoj'
apisecret = 'qX5Aly2RE8YAnjViRcO9yz142jK3PYl3YJE33jhlLnzj48HQVr'
acesstoken = '887695665874251776-Qge8k2QQwOI4g0E76CRgWDAw2cAlEUX'
tokensecret = 'KwGpKS0BkFubtTLYJ3HZzMCF5ZRdN11p97aHGuiUkC2Pr'
auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(acesstoken, tokensecret)
api = tweepy.API(auth)
conn = pyodbc.connect(r'DSN=BitcoinTwitter') #Add database connection here
cursor =conn.cursor()
analyzer = SentimentIntensityAnalyzer()
from datetime import datetime as dt

class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)

        if 'text' in all_data:
            tweet = all_data["text"]
            username = all_data["user"]["screen_name"]
            userlocation = all_data["user"]["location"]
            created_by = all_data["user"]["created_at"]
            vs = analyzer.polarity_scores(tweet)
            neg = vs.get('neg', -99)
            neu = vs.get('neu', 0)
            pos = vs.get('pos', 0)
            compound = vs.get('compound', 0)
            datetime = dt.now().strftime('%Y''-''%m''-''%d''  ''%X')
            date = dt.now().strftime('%Y''-''%m''-''%d')
            time = dt.now().strftime('%X')
            cursor.execute(
                "INSERT INTO TwitterFeedETH ( User_Id , tweet , User_Location ,Created_at, neg, neu, pos, compound,datetime, date, time ) VALUES (?,?,?,?, ? , ? ,?,?,?,?,?)", #Make sure table with right values and name is created in SQL here
                username, tweet, userlocation, created_by, neg, neu, pos, compound, datetime, date, time)
            conn.commit()
            #print((username, tweet))
            return True
        else:
            print(status)
            msg = "Eth Down!"
            server.sendmail("twitterbitcoinscraper@gmail.com", "conorkennedy999@gmail.com", msg)
            server.quit()
            return True


twitterStream = Stream(auth, listener())
twitterStream.filter(track=["ethereum"])