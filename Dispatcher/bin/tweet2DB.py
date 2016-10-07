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

# Recupero l'elenco delle keywords e/o gli hashtags da tracciare
txtToTrack = []
for key, val in Config.items("textToTrack"):
	txtToTrack.append(val)

# Recupero il nome del DataBase
dbName = Config.get("dbName", "dbName")


# Aggiungo la variabile dbConn a quelle super-globali e la inizializzo a None
# __builtin__.dbConn = None

# Mi connetto al DB ed aggiungo la connessione alla var Super-Globali
# Attenzione: la connessione al DB deve essere definita per essere visibile
# a tutte le classi/istanze.
__builtin__.dbConn = sqlite3.connect(dbName)

# Elenco delle pagine gestire dalla web application e relative
# classi associate.
urls = (
   '/', 'Index',
   '/shutdown', 'Shutdown', 
)

class Index:
	
	dbConn = None
	
	def __init__(self):
		
		# Web.py crea un thread per ogni richiesta http.
		# Gli oggetti __builtin__ sono relativi solo al thred in cui sono stati creati
		# Per cui devo creare una connessione per ogni request HTTP
		__builtin__.dbConn = sqlite3.connect(dbName)
	
	def GET(self):
		
		# Estraggo l'elenco dei Tweet
		tweetList = TweetList()
		
		# Se i dati post contengono un'indicazione di filtro
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
		
		# Avvio della ControlInterface web 
		app.run()
		
		# Istanza tweetStreamerClient
		# tsc = twitterStreamClient(authData, txtToTrack)
		# twitterStreamClient(authData, txtToTrack)

		# Avvio l'hubListner
		# 
		
	except sqlite3.Error as e:
		print "Sqlite error:\n %s" % e.args[0]
	except tweepy.TweepError as e:
		print ("Tweepy error:\n %s" %(e))
	except Exception, e:
		print ("General error:\n %s" %(e))