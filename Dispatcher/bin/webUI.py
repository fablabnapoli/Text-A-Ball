import __builtin__
import sqlite3
import web
import sys
import ConfigParser
from tweetLib import *
# from awsClient import awsSender
# import os.path
from tabHost import tabHost

###############################################################################
#				Leggo il contenuto del file di configurazione

# Leggo i parametri di configurazione del dispatcher
Config = ConfigParser.ConfigParser()
# Indico a ConfigParser di attivare il Case Sensitive Mode
Config.optionxform=str

# Config.read("config.ini") # File di configurazione per l'ambiente di produzione
Config.read("devConfig.ini") # File di configurazione per l'abiente di sviluppo

# Recupero il nome del DataBase
dbName = Config.get("dbName", "dbName")

# Recupero le informazioni di connessione alla stampante
port = Config.get("tabConnOpt", "port")
brate = Config.get("tabConnOpt", "brate")

# Recupero il path dell'interprete python
pythonBin = Config.get("binPath", "pythonBin")

# Recupero il path del Post-Processor
ppPath = Config.get("binPath", "ppPath")

# Recupero le opzioni di stampa
tabRunOptStr = ""
for key, val in Config.items("tabRunOpt"):
	# tabRunOpt[key] = val
	tabRunOptStr += '-'+key+val+' '
	
# print("Port: %s, Baund: %s" %(port, brate))
# print("Print options: %s" %(tabRunOpt))
# print("Bin paths:\n %s \n %s" %(pythonBin, ppPath))
# print("Print options string:\n %s" %(optStr))

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
			# Aggiorno lo stato del tweet
			tweet2Print = Tweet(getData["id"])
			
			# Invio il comando di stampa all'host
			# Parte ancora da implementare
			# os.system("/usr/bin/python ./bin/TaB_AWS_send.py -t %s -m %s" %(getData["tab"],tweet2Print.getMsg()))
			# os.system("G:\winPenPack\Bin\Python2\python.exe ./bin/TaB_AWS_send.py -t TaB_01 -m %s" %(tweet2Print.getMsg()))
			
			# Modalità di stampa "Standalone"
			host = tabHost(port, brate)
			
			host.connect()
			
			host.setRunOpt(tabRunOptStr)
			host.setPythonPath(pythonBin)
			host.setPpBin(ppPath)
			
			host.postProcess(msg=tweet2Print.getMsg())
			
			host.run()
			
			tweet2Print.setStatus("Printed")
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