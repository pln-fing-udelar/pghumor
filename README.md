# Configuración

Poner la variable de entorno a donde se encuentre el entorno de Freeling y dejarla puesta siempre:

```bash
FREELINGSHARE=/usr/local/share/freeling
echo "export FREELINGSHARE=$FREELINGSHARE" >> ~/.bashrc
```

# Ejecución

Levantar antes los servidores de Freeling:

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

# Tests

```bash
./tests.sh
```
