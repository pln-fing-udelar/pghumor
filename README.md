# Para Ejecutar
```
    
Poner la variable de entorno a donde se encuentre el entorno de Freeling y dejarla puesta siempre:

```bash
FREELINGSHARE=/usr/local/share/freeling
echo "export FREELINGSHARE=/usr/local/share/freeling" >> ~/.bashrc
```

Levantar los servidores de Freeling:

```bash
analyze -f $FREELINGSHARE/config/es.cfg --noprob --outf morfo --server --workers 4 --queue 50 --port 11111 --flush
```

```bash
analyze -f $FREELINGSHARE/config/es.cfg --server --workers 4 --queue 50 --port 55555 --flush

# Para correr todos los tests

```bash
python -m unittest discover clasificador/test/
```
