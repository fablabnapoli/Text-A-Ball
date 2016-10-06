import __builtin__
import sqlite3

class TweetException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Tweet():

	dbConn = None
	
	id = ""
	msg = ""
	user = ""
	date = ""
	tableName = "tweets"


	def __init__(self, id=""):
	
		# Recupero la connessione al DB dalle variabili "super-globali"
		if __builtin__.dbConn is not None:
			self.dbConn = __builtin__.dbConn
		else:
			raise Exception("Tweet.__init__: Data base not connected")	
		
		if id: # Se è stato fornito un id recupero il tweet rorrispondente dal DB
			cur = self.dbConn.cursor()
			
			# Ricerco il tweet corrispondente all'id fornito.
			cur.execute('SELECT * FROM tweets WHERE id=?', (id,))
			results = cur.fetchall()
			
			if len(results) == 1 : # Se il tweet ricercato esiste ed � unico
				(self.id, self.msg, self.user, self.date) = results[0]
			else:
				raise Exception("Tweet.__init__: Tweet %s non trovato" %(id))
		# elif dataArray:
			
			
		else: # Se non è stato fornito un id valido creao un oggetto Tweet vuoto
			pass

	def getId(self):
		# Restituisce il valore del Tweet
		return self.id

	def setUser(self, user):
		# Imposta il nome dell'autore
		self.user = user

	def getUser():
		# Restituisce il nome dell'autore
		return self.user

	def setMsg(self,msg):
		# Imposta il corpo del messaggio
		self.msg = msg

	def getMsg(self):
		# Restituisce il corpo del messaggio
		return self.msg
		
		
	def setId(self, id):
		# Imposta il valore del id
		self.id = id
		
	def save(self):
		# Salva il tweet nel DB
		
		cur = self.dbConn.cursor()			
						
		cur.execute('INSERT OR REPLACE INTO tweets  (id, msg, user, date) VALUES (?, ?, ?, ?)', (self.id, self.msg, self.user, self.date))
		self.dbConn.commit()
			
		
"""	
	def delete():
		# Elimina il tweet dal DB
"""

class TweetList():
		"""
			La classe consente di operare su un insieme di tweets
		"""
		filters = None
		cur = None

		def __init__(self):
			# Recupero la connessione al DB dalle variabili "super-globali"
			if __builtin__.dbConn is not None:
				self.cur = __builtin__.dbConn.cursor()
			else:
				raise Exception("TweetList.__init__: Data base not connected")	
		
		def setFilters(self, filter = None):
			self.filters = filter
			
		def getTweets(self):
			
			sql = "SELECT * FROM tweets"
			tweetList = []
			
			if self.filters is None:
				self.cur.execute(sql)
			else:
				cond =','.join(' {0}="{1}"'.format(key, val) for key, val in self.filters.items())
				sql = sql + " WHERE" + cond  
				self.cur.execute(sql)
			
			# Per ogni riga estratta dal DB creao un nuovo Tweet object e lo 
			# popolo con i dati ricavati dalla query.
			for tweetLine in self.cur.fetchall():
				newTweet = Tweet()				# Creo un Tweet vuto
				newTweet.setId(tweetLine[0])	# Imposto l'ID
				newTweet.setMsg(tweetLine[1])	# Imposto il msg
				newTweet.setUser(tweetLine[2])	# Imposto l'utente
				newTweet.setUser(tweetLine[3])	# Imposto la data				
				# newTweet.setUser(tweetLine[4])	# Imposto lo stato
				
				tweetList.append(newTweet)		# Aggiungo all'elenco
			
			return tweetList					# Restituisco l'elenco dei Tweet
		