import __builtin__
import sqlite3
import web
import tweepy
import sys
from tweetStreamer import twitterStreamClient
import ConfigParser
from tweetLib import *

# Leggo i parametri di configurazione del dispatcher
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Recupero i dati di accesso all'account Twitter
# Il comando items restituisce una lista, uso "dict" per convertire la lista in un dizionario (array associativo)
# un dizionario (array associativo)
authData = dict(Config.items("authData"))

# Recupero l'elenco delle keywords e gli hashtags da tracciare
# Il comando items restituisce una lista, uso "str" per convertire la lista in
# un array di stringhe 
txtToTrack = str(Config.items("textToTrack"))

# Recupero il nome del DataBase
dbName = Config.get("dbName", "dbName")


# Aggiungo la variabile dbConn a quelle super-globali e la inizializzo a None
__builtin__.dbConn = None

# Mi connetto al DB ed aggiungo la connessione alla var Super-Globali
# Attenzione: la connessione al DB deve essere definita per essere visibile
# a tutte le classi/istanze.
# __builtin__.dbConn = sqlite3.connect(dbName)

# Elenco delle pagine gestire dalla web application e relative
# classi associate.
urls = (
   '/', 'Index',
   '/shutdown', 'Shutdown', 
)

class Index:
	
	dbConn = None
	
	def __init__(self):
		
		# import __builtin__
		# Recupero la connessione al DB dalle variabili "super-globali"
		# if __builtin__.dbConn is not None:
			# self.dbConn = __builtin__.dbConn
		# else:
			# raise Exception("Index.__init__: Data base not connected")	
		
		# Web.py crea un thread per ogni richiesta http.
		# Gli oggetti __builtin__ sono relativi solo al thred in cui sono stati creati
		# Per cui devo creare una connessione per ogni request HTTP
		
		__builtin__.dbConn = sqlite3.connect(dbName)
	
	def GET(self):
		
		# Estraggo l'elenco dei Tweet
		tweetList = TweetList()
		# tweetList.setFilters({'user':"pluto"})
		
		return render.index(tweetList = tweetList.getTweets())
	
	def __del__(self):
		__builtin__.dbConn.close()

# Attivazione della web application
app = web.application(urls, globals())
# Attivazione del motore dei template
render = web.template.render('templates/')

if __name__ == "__main__":
	try:
		
		
		# Istanza tweetStreamerClient
		# tsc = twitterStreamClient(dbConn, authData, txtToTrack)
		
		# Avvio della ControlInterface web 
		app.run()

		# Avvio l'hubListner
		# 
		
		# from tweetLib import *
		# tweetList = TweetList()
		# tweetList.setFilters({'user':"pluto"})
		# for tweet in tweetList.getTweets():
			# print tweet.getMsg()
		
	except sqlite3.Error as e:
		print "Data base error %s" % e.args[0]
	except Exception, e:
		print e
		sys.exit(1)