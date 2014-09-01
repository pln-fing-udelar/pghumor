import cargarDatos
import tokenizacion

tweets = cargarDatos.extraer()
tweets_tokenizados = [tokenizacion.tokenizar(tweet) for tweet in tweets]

tweets_tokenizados[0]
