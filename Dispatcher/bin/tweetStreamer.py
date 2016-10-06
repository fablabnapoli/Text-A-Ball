import tweepy
import sqlite3
import json
import sys

from tweet import Tweet
from tweet import TweetException

class dbStreamer(tweepy.StreamListener):

	# def __init__(self, dbConn):
	def __init__(self):
		# self.dbConn = dbConn
		pass
		
	def on_data(self, data):
		# global dbConn
		
		try:
			
			decoded = json.loads(data)
			
			# newTweet = tweet(self.dbConn)
			newTweet = Tweet()
			newTweet.setId(str(decoded['id']))
			newTweet.setMsg(decoded['text'].encode('ascii', 'ignore'))
			newTweet.setUser(decoded['user']['name'])
			# newTweet.setDate()
			newTweet.save()
			
			# Insert a row of data
			# cursor.execute("INSERT INTO spool (tweetId, userId, created_at, msgBody, location) VALUES (?,?,?,?,?)", (str(decoded['id']), decoded['user']['name'], decoded['created_at'], decoded['text'].encode('ascii', 'ignore'), decoded['user']['location']))
			# dbConn.commit()
			
			# Da eliminare
			#sys.exit()
			
		except sqlite3.Error, e:
			print "Query Error %s:" % e.args[0]
			sys.exit(1)
	
	def on_error(self, status):
		print status
	
	def on_exception(self, exception):
		print exception
	
class twitterStreamClient:

	#Costruttore di classe
	def __init__(self, dbConn, authData, txtToTrack):
		auth = tweepy.OAuthHandler(authData['consumer_key'], authData['consumer_secret'])
		auth.set_access_token(authData['access_token'], authData['access_token_secret'])
		
		# dbs = dbStreamer(dbConn)
		dbs = dbStreamer()
		stream = tweepy.Stream(auth, dbs)
		stream.filter(track=txtToTrack, async=False) 