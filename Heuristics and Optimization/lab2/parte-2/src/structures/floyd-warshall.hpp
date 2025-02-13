//
// Created by golden on 12/19/24.
//

#ifndef FLOYD_WARSHALL_HPP
#define FLOYD_WARSHALL_HPP
#include <limits>
#include <map>
#include <vector>

#include "graph.hpp"

using namespace std;

// Implementación del algoritmo de Floyd-Warshall. Contiene una tabla de distancias entre nodos
// y una correlación de nodos para poder acceder a la tabla de distancias de forma eficiente.
class FloydWarshall {
public:
    vector<vector<size_t>> tabla_distancias;
    map<Node,size_t> correlacion_nodos; // Usado para saber en que posición de la tabla está cada nodo
    size_t num_nodos;
    bool is_FloydWarshall; // Variable de control para heuristica de manhattan

    explicit FloydWarshall(const map<Node, vector<Node>>& edges, bool ifFloyd=true) : num_nodos(edges.size()), is_FloydWarshall(ifFloyd) {};

    void build(const map<Node, vector<Node>>& edges) {
        if (!is_FloydWarshall) { return; } // Si no se quiere usar Floyd-Warshall, no se calcula

        // Inicializamos la tabla de distancias al máximo valor posible
        tabla_distancias = vector<vector<size_t>>(num_nodos, vector<size_t>(num_nodos, numeric_limits<size_t>::max() -num_nodos));

        // Inicializamos la correlación de nodos y aprovechamos para inicializar la diagonal de la tabla de distancias
        size_t i = 0;
        for (auto &p : edges) {
            correlacion_nodos.insert(make_pair(p.first, i));
            tabla_distancias[i][i] = 0;
            i++;
        }

        // Rellenamos la tabla de distancias con los costes (unitarios) de las aristas
        for (const auto &p : edges) {
            size_t it = correlacion_nodos[p.first];
            for (const auto &n : p.second) {
                if (correlacion_nodos.find(n) != correlacion_nodos.end()) { // Aseguramos que el nodo existe en el mapa
                    size_t j = correlacion_nodos[n];
                    tabla_distancias[it][j] = 1; // Coste unitario
                }
            }
        }

        // Aplicamos el algoritmo de Floyd-Warshall
        for (size_t k = 0; k < num_nodos; k++) {
            for (size_t it = 0; it < num_nodos; it++) {
                for (size_t j = 0; j < num_nodos; j++) {
                    if (tabla_distancias[it][j] > tabla_distancias[it][k] + tabla_distancias[k][j]) {
                        tabla_distancias[it][j] = tabla_distancias[it][k] + tabla_distancias[k][j];
                    }
                }
            }
        }
    }

    // Devuelve la distancia entre dos nodos
    [[nodiscard]] size_t get_distance(Node a, Node b) {
        return tabla_distancias[correlacion_nodos[a]][correlacion_nodos[b]];
    }

    // Imprime la tabla de distancias para facilitar el debugging
    void print_distances() const {
        if (!is_FloydWarshall) { return; } // Si no se ha calculado la tabla, no se imprime
        for (size_t i = 0; i < num_nodos; i++) {
            for (size_t j = 0; j < num_nodos; j++) {
                cout << tabla_distancias[i][j] << " ";
            }
            cout << "\n";
        }
    }
};

#endif //FLOYD_WARSHALL_HPP
