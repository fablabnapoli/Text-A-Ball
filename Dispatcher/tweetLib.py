
class tweetException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class tweet():

	dbConn = ""
	id = ""
	msg = ""
	user = ""
	date = ""
	tableName = "tweets"


	def __init__(self, dbConn, id=""):
		self.dbConn = dbConn
		
		if id: # Se è stato fornito un id recupero il tweet rorrispondente dal DB
			cur = self.dbConn.cursor()
			
			# Ricerco il tweet corrispondente all'id fornito.
			cur.execute('SELECT * FROM tweets WHERE id=?', (id,))
			results = cur.fetchall()
			
			if len(results) == 1 : # Se il tweet ricercato esiste ed � unico
				(self.id, self.msg, self.user, self.date) = results[0]
			else:
				raise tweetException("Something went wrong seeking for the tweet %s" %(id))
		else: # Se non è stato fornito un id valido 
			print("New Tweet")	

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
		
	def getId(self):
		# Restituisce il valore del Tweet
		return self.id
		
	def setId(self, id):
		# Imposta il valore del id
		self.id = id
		
	def save(self):
		# Salva il tweet nel DB
		
		cur = self.dbConn.cursor()			
		# if self.id: # Se l'id è definito, aggiorno il record nel DB
			# cur.execute('UPDATE tweets  SET msg=?, user=?, date=? WHERE id=?', (self.msg, self.user, self.date,self.id))
			# self.dbConn.commit()
						
		# else:  # Se l'id non è definito aggiungo un nuovo tweet al DB
		cur.execute('INSERT OR REPLACE INTO tweets  (id, msg, user, date) VALUES (?, ?, ?, ?)', (self.id, self.msg, self.user, self.date))
		self.dbConn.commit()
			
		
"""	
	def delete():
		# Elimina il tweet dal DB
"""
		