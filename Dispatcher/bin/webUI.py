import __builtin__
import sqlite3
import web
import sys
import ConfigParser
from tweetLib import *
from awsClient import awsSender
import os.path

###############################################################################
#				Leggo il contenuto del file di configurazione

# Leggo i parametri di configurazione del dispatcher
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Recupero il nome del DataBase
dbName = Config.get("dbName", "dbName")

# Recupero i parametri di connessione ad AWS
dispatcherAuth = {}
# Il mio identificativo nella comunicazione
dispatcherAuth['tabId'] = "tabDispatcher"
for key, val in Config.items("dispatcher"):
	dispatcherAuth[key]=os.path.join(os.getcwd(), "certs\dispatcher\mainCA.crt")
	
# print ("Silvertab connection options: %s" %(dispatcherAuth) )
# print ("CWD: %s " %(os.getcwd()) )
# print "rootCAPath path: "+(os.path.join(os.getcwd(), "certs\dispatcher\mainCA.crt"))
# print ("rootCAPath exists: %s " %(os.path.exists(dispatcherAuth['rootcapath'])))
# print ("rootCAPath exists: %s " %(os.path.exists(os.path.join(os.getcwd(), "certs\dispatcher\mainCA.crt"))))
# sys.exit(0)

################################################################################
#				Configurazione della web interface

# Elenco delle pagine gestire dalla web application e relative
# classi associate.
urls = (
   '/', 'Index',
   '/delete', 'Delete',
   '/print', 'Print',

)

# Classe per la gestione della pagina index (/)
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

class Delete:
	def __init__(self):
		# Web.py crea un thread per ogni richiesta http.
		# Gli oggetti __builtin__ sono relativi solo al thred in cui sono stati creati
		# Per cui devo creare una connessione per ogni request HTTP
		__builtin__.dbConn = sqlite3.connect(dbName)	
	
	def GET(self):
		getData = web.input()
		
		if getData["id"]:
			tweet2Delete = Tweet(getData["id"])
			tweet2Delete.delete()
			print("Delete request for tweet id: %s\n" %(getData["id"]))
		else:
			print("Id not found: %s\n" %(getData))
		
	def __del__(self):
		__builtin__.dbConn.close()		
		
class Print:
	def __init__(self):
		# Web.py crea un thread per ogni richiesta http.
		# Gli oggetti __builtin__ sono relativi solo al thred in cui sono stati creati
		# Per cui devo creare una connessione per ogni request HTTP
		__builtin__.dbConn = sqlite3.connect(dbName)
		
	def GET(self):
		getData = web.input()
	
		if getData["id"]:
			
			# Recupero il tweet dal DB
			tweet2Print = Tweet(getData["id"])
			
			# Creo ed imposto il client di comunicazione con la stampante
			dispatcherClient = awsSender(dispatcherAuth)
			# Mi connetto alla stampante
			dispatcherClient.connect()
			# Invio il messaggio alla stampante
			dispatcherClient.sendMsg(getData["tab"], tweet2Print.getMsg())
			
			# Aggiorno lo stato del tweet
			tweet2Print.setStatus("Printing")
			tweet2Print.save()
			
			# Preparo l'output aggiornato
			# Parte ancora da implementare
			return tweet2Print.getStatus()
			
			print("Print request for tweet id: %s\n" %(getData["id"]))
		else:
			print("Id not found: %s\n" %(getData))
			
			
		def __del__(self):
			pass
		
# Attivazione della web application
app = web.application(urls, globals())

# Attivazione del motore dei template.
# I files .html dovranno essere posizionati nella catella teamplates/
# I file statici (immagini, css, javascript) nella cartella static/
render = web.template.render('templates/')


################################################################################
#						Ciclo principale

if __name__ == "__main__":
	try:
		
		# Avvio della ControlInterface web 
		app.run()
		
		# __builtin__.dbConn = sqlite3.connect(dbName)
		# tweetTest = Tweet("784040250175651840")
		# print("Tweet Msg: %s" %(tweetTest.getMsg()))

		
	except sqlite3.Error as e:
		print "Sqlite error:\n %s" % e.args[0]

	except Exception, e:
		print ("General error:\n %s" %(e))