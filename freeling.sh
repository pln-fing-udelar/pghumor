#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Número de parámetros incorrecto"
fi

if [ $1 = "start" ]; then
    killall analyzer > /dev/null 2> /dev/null
    analyze -f $FREELINGSHARE/config/es.cfg --noprob --outf morfo --server --workers 4 --queue 50 --port 11111 --flush > /dev/null 2> /dev/null &
    analyze -f $FREELINGSHARE/config/es.cfg --server --workers 4 --queue 50 --port 55555 --flush > /dev/null 2> /dev/null &
elif [ $1 = "stop" ]; then
    killall analyzer
else
    echo "Opción no reconocida: $1"
fi
