import cargarDatos
import tokenizacion

humor, no_humor = cargarDatos.extraer()
tweets = humor
tweets_tokenizados = [tokenizacion.tokenizar(tweet.texto) for tweet in tweets]

tweets_tokenizados[0]
