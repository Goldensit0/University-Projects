#!/bin/bash

# Compilacion
if [ ! -d "build" ]; then
    mkdir build
    cmake . -DCMAKE_BUILD_TYPE=Release -B build
fi
make -C build -j8

# Caso base aportado por el enunciado:
echo "Caso base del enunciado"
echo "Heuristica 1: Manhattan"
build/ASTARRodaje ASTAR-tests/mapa1.csv 1
echo "Heuristica 2: Floyd-Warshall"
build/ASTARRodaje ASTAR-tests/mapa1.csv 2
