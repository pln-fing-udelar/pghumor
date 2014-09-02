import MySQLdb
import Tweet

DB_HOST = 'localhost' 
DB_USER = 'pghumor' 
DB_PASS = 'ckP8t/2l'
DB_NAME = 'chistesdb'

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

			resultado.append(tw)
		except:
			pass

	return resultado


## Por ahora hace lo mismo que extraerHumor
def extraerNoHumor():
	return extraerHumor()

def extraer():
	return extraerHumor(), extraerNoHumor
