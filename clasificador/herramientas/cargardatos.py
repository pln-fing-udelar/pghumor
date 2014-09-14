import MySQLdb
import sys

from realidad.tweet import Tweet

DB_HOST				= 'localhost' 
DB_USER				= 'pghumor' 
DB_PASS				= 'ckP8t/2l'
DB_NAME				= 'chistesdb'
DB_NAME_NO_CHISTES	= 'nochistesdb'

def extraerHumor():
	datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
	connection = MySQLdb.connect(*datos)
	cursor = connection.cursor()

	query = 'SELECT * FROM chistesdb.tweets AS T JOIN chistesdb.twitter_accounts AS A ON T.twitter_accounts_id_account = A.id_account'

	cursor.execute(query)

	result = cursor.fetchall();

	resultado = []

	for t in result:
		try:
			t[1].decode('utf-8')
			t[8].decode('utf-8')
			tw = Tweet()
			tw.id = t[0]
			tw.texto = t[1]
			tw.favoritos = t[2]
			tw.retweets = t[3]
			tw.cuenta = t[8]
			tw.seguidores = t[9]
			tw.es_humor = True

			resultado.append(tw)
		except UnicodeDecodeError as e:
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

	connection = MySQLdb.connect(*datos)
	cursor = connection.cursor()

	query = 'SELECT * FROM nochistesdb.tweets AS T JOIN nochistesdb.twitter_accounts AS A ON T.id_account = A.id_account'

	cursor.execute(query)

	result = cursor.fetchall();	

	resultado = []
	
	for t in result:
		try:
			t[1].decode('utf-8')
			t[6].decode('utf-8')
			tw = Tweet()
			tw.id = t[0]
			tw.texto = t[1]
			tw.favoritos = t[2]
			tw.retweets = t[3]
			tw.cuenta = t[6]
			tw.seguidores = t[7]
			tw.es_humor = False

			resultado.append(tw)
		except UnicodeDecodeError as e:
			pass

	return resultado

def extraerTweets():
	return extraerHumor(), extraerNoHumor()
