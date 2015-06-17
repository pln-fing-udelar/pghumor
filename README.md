# Instalación

Se precisa python 2.7, MySQL, las librerías python aquí utilizadas, Freeling (revisión 2588 del SVN) y el corpus WordNet en NLTK.

Se deben cargar los dumps corpus.sql y chistesdotcom.sql 

# Configuración

En el archivo `clasificador/config/environment.py` poner las credenciales de la API de Twitter y los datos para las bases de datos. Un ejemplo de este archivo es el siguiente:

```python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os

# Twitter API credentials
os.environ['CONSUMER_KEY'] = '--CONSUMER KEY--'
os.environ['CONSUMER_SECRET'] = '--CONSUMER SECRET--'
os.environ['ACCESS_KEY'] = '--ACCESS KEY--'
os.environ['ACCESS_SECRET'] = '--ACCESS SECRET--'

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_USER'] = 'pghumor'
os.environ['DB_PASS'] = '--PASSWORD--'
os.environ['DB_NAME'] = 'corpus'
os.environ['DB_NAME_CHISTES_DOT_COM'] = 'chistesdotcom'
```

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
