import MySQLdb
import sys

sys.path.append("../realidad")

import tweet

DB_HOST				= 'localhost' 
DB_USER				= 'pghumor' 
DB_PASS				= 'ckP8t/2l'
DB_NAME				= 'chistesdb'
DB_NAME_NO_CHISTES	= 'nochistesdb'

def extraerHumor():
	datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
	conection = MySQLdb.connect(*datos)
	cursor = conection.cursor()

	query = "SELECT * FROM chistesdb.tweets AS T JOIN chistesdb.twitter_accounts AS A ON T.twitter_accounts_id_account = A.id_account"

	cursor.execute(query)

	result = cursor.fetchall();

	resultado = []
	
	for tweet in result:
		try:
			tweet[1].decode('utf-8')
			tweet[8].decode('utf-8')
			tw = Tweet.Tweet()
			tw.id = tweet[0]
			tw.texto = tweet[1]
			tw.favoritos = tweet[2]
			tw.retweets = tweet[3]
			tw.cuenta = tweet[8]
			tw.seguidores = tweet[9]
			tw.es_humor = True

			resultado.append(tw)
		except:
			pass

	return resultado

## Por ahora hace lo mismo que extraerHumor
def extraerNoHumor():
	datos = [
		DB_HOST,
		DB_USER,
		DB_PASS,
		DB_NAME_NO_CHISTES,
	]

	conection = MySQLdb.connect(*datos)
	cursor = conection.cursor()

	query = 'SELECT * FROM nochistesdb.tweets AS T JOIN nochistesdb.twitter_accounts AS A ON T.id_account = A.id_account'

	cursor.execute(query)

	result = cursor.fetchall();	

	resultado = []
	
	for tweet in result:
		try:
			tweet[1].decode('utf-8')
			tweet[6].decode('utf-8')
			tw = Tweet.Tweet()
			tw.id = tweet[0]
			tw.texto = tweet[1]
			tw.favoritos = tweet[2]
			tw.retweets = tweet[3]
			tw.cuenta = tweet[6]
			tw.seguidores = tweet[7]#
			tw.es_humor = False

			resultado.append(tw)
		except:
			pass

	return resultado

def extraer():
	return extraerHumor(), extraerNoHumor()
