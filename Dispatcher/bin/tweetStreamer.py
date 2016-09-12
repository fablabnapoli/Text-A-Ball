import tweepy
import sqlite3
import json
import sys

class dbStreamer(tweepy.StreamListener):

   def __init__(self, dbName):
      self.dbName = dbName
      
   def on_data(self, data):
      try:
         dbConn = sqlite3.connect(self.dbName)
         
         cursor = dbConn.cursor()
         
         decoded = json.loads(data)

         #print json.dumps(decoded, sort_keys=True, indent=4, separators=(',', ': '))
         
         # Insert a row of data
         cursor.execute("INSERT INTO spool (tweetId, userId, created_at, msgBody, location) VALUES (?,?,?,?,?)", (str(decoded['id']), decoded['user']['name'], decoded['created_at'], decoded['text'].encode('ascii', 'ignore'), decoded['user']['location']))
         dbConn.commit()
         
         # Da eliminare
         #sys.exit()
         
      except sqlite3.Error, e:
         print "Query Error %s:" % e.args[0]
         sys.exit(1)
         
      finally:
         if dbConn:
            dbConn.close()

   def on_error(self, status):
      print status

class twitterStreamClient:

   consumer_key = '###INSERT YOUR KEY HERE###'
   consumer_secret = '###INSERT YOUR KEY HERE###'
   access_token = '###INSERT YOUR KEY HERE###'
   access_token_secret = '###INSERT YOUR KEY HERE###'

   #Costruttore di classe
   def __init__(self):
      auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
      auth.set_access_token(self.access_token, self.access_token_secret)
      
      dbs = dbStreamer("database/tabDB.db")
      stream = tweepy.Stream(auth, dbs)
      stream.filter(track=['###INSERT YOUR SEARCHING KEYWORD HERE###'], async=False) 
