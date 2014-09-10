import MySQLdb

DB_HOST = 'localhost' 
DB_USER = 'pghumor' 
DB_PASS = 'ckP8t/2l'
DB_NAME = 'chistesdb'

class Tweet:

	def __init__(self):
		self.id = 0
		self.texto = ""
		self.retweets = 0
		self.favoritos = 0
		self.cuenta = ""
		self.seguidores = 0
		self.es_humor = False

		self.features = {}

	def persistir(self):
		
		datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
		conection = MySQLdb.connect(*datos)
		cursor = conection.cursor()

		cursor.execute(query)		
			for key,value in self.features.items():
				query = "INSERT INTO features VALUES (" + `self.id` + ",'" + key+ "'," + value + ") ON DUPLICATE KEY UPDATE valor_feature = " + value
				cursor.execute(query)

		conection.commit()
