import tweepy
import sqlite3
import json
import sys

from tweetLib import *
# from Tweet import TweetException

class dbStreamer(tweepy.StreamListener):

	def __init__(self):
		# self.dbConn = dbConn
		pass
		
	def on_data(self, data):
		try:
			decoded = json.loads(data)
			
			# newTweet = Tweet(self.dbConn)
			newTweet = Tweet()
			newTweet.setId(str(decoded['id']))
			newTweet.setMsg(decoded['text'].encode('ascii', 'ignore'))
			newTweet.setUser(decoded['user']['name'])
			# newTweet.setDate("")
			newTweet.setStatus("new")
			newTweet.save()
			
			# print("Tweet2DB - New Tweet: %s " %(newTweet.getId()))
			
		except sqlite3.Error, e:
			print "Query Error %s:" % e.args[0]
			sys.exit(1)
	
	def on_error(self, status):
		print ("dbStreamer error: %s" %(status))
	
	def on_exception(self, exception):
		return ("dbStreamer exception: %s" %(exception))
	
class twitterStreamClient:

	#Costruttore di classe
	def __init__(self, authData, txtToTrack):
		auth = tweepy.OAuthHandler(authData['consumer_key'], authData['consumer_secret'])
		auth.set_access_token(authData['access_token'], authData['access_token_secret'])
		
		# dbs = dbStreamer(dbConn)
		dbs = dbStreamer()
		stream = tweepy.Stream(auth, dbs)
		stream.filter(track=txtToTrack, async=False) 