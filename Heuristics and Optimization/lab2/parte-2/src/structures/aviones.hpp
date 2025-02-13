//
// Created by golden on 12/18/24.
//

#ifndef AVIONES_HPP
#define AVIONES_HPP
#include <cmath>
#include <utility>

#include "floyd-warshall.hpp"

using namespace std;
// Clase que usaremos para almacenar los aviones y sus posiciones
class Avion {
public:
    pair<size_t,size_t> posicion, destino; // Posicion actual y destino, en coordenadas x,y
    bool en_amarillo; // Indica si el avión está en una casilla amarilla
    size_t g_coste; // Coste para llegar a esta posición
    Avion(pair<size_t,size_t> pos, pair<size_t,size_t> dest, bool amarillo, size_t coste) :
            posicion(move(pos)), destino(move(dest)), en_amarillo(amarillo), g_coste(coste){}

    // Calcula la heurística de este avión, dependiendo de si se ha calculado la tabla de distancias de Floyd Warshall
    // o se usa distancia de Manhattan.
    [[nodiscard]] size_t heuristica(FloydWarshall &tabla_distancias) const {
        if (tabla_distancias.is_FloydWarshall) {
            // Selección de heurística
            return heuristica_floyd_warshall(tabla_distancias);
        }
        return heuristica_mahattan();
    }

    bool operator==(const Avion & otro) const {
        return posicion == otro.posicion && destino == otro.destino;
    }

private:
    // Calcula la heurística de Manhattan entre la posición actual y el destino
    [[nodiscard]] size_t heuristica_mahattan() const {
        size_t a, b;
        if (posicion.first > destino.first) {a = posicion.first - destino.first;}
        else {a = destino.first - posicion.first;}
        if (posicion.second > destino.second) {b = posicion.second - destino.second;}
        else {b = destino.second - posicion.second;}
        return a + b;
    }

    // Accede a tabla de Floyd Warshall y devuelve la distancia entre la posición actual y el destino
    [[nodiscard]] size_t heuristica_floyd_warshall(FloydWarshall &tabla_distancias) const {
        return tabla_distancias.get_distance(Node(posicion.first, posicion.second, true),
                                            Node(destino.first, destino.second, true));
    }
};



#endif //AVIONES_HPP
