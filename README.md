# Instalación

Se precisa python 2.7, MySQL, las librerías python aquí utilizadas, Freeling (revisión 2588 del SVN) y el corpus WordNet en NLTK.

Se deben cargar los dumps corpus.sql y chistesdotcom.sql 

# Configuración

En el archivo `clasificador/config/environment.py` poner las credenciales de la API de Twitter y los datos para las bases de datos.

Poner la variable de entorno a donde se encuentre el entorno de Freeling y dejarla puesta siempre:

```bash
FREELINGSHARE=/usr/local/share/freeling
echo "export FREELINGSHARE=$FREELINGSHARE" >> ~/.bashrc
```

# Ejecución

Levantar antes los servidores de Freeling (para poder calcular las características):

```bash
./freeling.sh start
```

Luego para correr:

```bash
clasificador/main.py
```

Para bajar los servidores de Freeling:

```bash
./freeling.sh stop
```

## Ayuda

```bash
clasificador/main.py --help
```

# Tests

```bash
./tests.sh
```
