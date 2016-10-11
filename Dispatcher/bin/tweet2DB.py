import __builtin__
import sqlite3
import tweepy
from tweetStreamer import twitterStreamClient
import sys
import ConfigParser
from tweetLib import *


################################################################################
#				Leggo il contenuto del file di configurazione

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


################################################################################
#						Avvio la connessione al DB

# Mi connetto al DB ed aggiungo la connessione alla var Super-Globali
# Attenzione: la connessione al DB deve essere definita per essere visibile
# a tutte le classi/istanze.
__builtin__.dbConn = sqlite3.connect(dbName)


################################################################################
#						Ciclo principale

if __name__ == "__main__":
	try:
		
		# Istanza tweetStreamerClient
		# tsc = twitterStreamClient(authData, txtToTrack)
		twitterStreamClient(authData, txtToTrack)

		# Avvio l'hubListner
		# 
		
	except sqlite3.Error as e:
		print "Sqlite error:\n %s" % e.args[0]
	# except tweepy.TweetError as e:
		# print ("Tweepy error:\n %s" %(e))
	# except Exception, e:
		# print ("General error:\n %s" %(e))