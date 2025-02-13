//
// Created by golden on 12/18/24.
//

#ifndef GRAPH_HPP
#define GRAPH_HPP
#include <iostream>
#include <map>
#include <utility>
#include <vector>

using namespace std;

// Implementación de un nodo (posicion fila,columna del mapa).
class Node {
public:
    size_t fila, columna;
    bool amarillo;
    Node(size_t fila, size_t columna, bool amarillo) : fila(fila), columna(columna), amarillo(amarillo) {}

    // Implementación de operadores de comparación para poder comparar nodos y usarlos en std::map
    bool operator==(const Node &n) const {
        return fila == n.fila && columna == n.columna;
    }
    bool operator!=(const Node &n) const {
        return fila != n.fila || columna != n.columna;
    }
    bool operator<(const Node &n) const {
        return fila < n.fila || (fila == n.fila && columna < n.columna);
    }
    bool operator>(const Node &n) const {
        return fila > n.fila || (fila == n.fila && columna > n.columna);
    }
};

// Implementación de un grafo con un mapa ordenado (posicion->nodo)
// columna una lista de aristas, siendo estas listas de nodos asociadas al nodo desde el que se accede a ellas.
class Graph {
public:
    map<pair<size_t,size_t>, Node> nodes;
    map<Node, vector<Node>> edges;

    // Añade un nodo al grafo.
    void add_node(Node n) {
        nodes.insert(make_pair(make_pair(n.fila,n.columna), n));
    }

    // Añade una arista al grafo. Comprueba si el nodo ya tiene alguna arista, sino lo añade como una nueva lista de aristas
    void add_edge(Node a, Node b) {
        for (auto &p : edges) {
            if (p.first == a) {
                p.second.emplace_back(b);
                return;
            }
        }
        edges.insert(make_pair(a, vector<Node>{b}));
    }

    // Devuelve el nodo en la posición fila,columna.
    Node get_node(size_t fila, size_t columna) {
        auto it = nodes.find(std::make_pair(fila, columna));
        if (it != nodes.end()) { // Comprueba que exista el nodo
            return it->second;
        } else {
            throw std::runtime_error("El nodo no existe en (" + to_string(fila) + ", " + to_string(columna) + ")");
        }
    }

    // Devuelve los vecinos de un nodo concreto
    vector<Node> &get_neighbors(const Node &n) {
        return edges[n];
    }

    // Devuelve el mapa de nodos y sus conexiones
    map<Node, vector<Node>> &get_edges() {
        return edges;
    }

    // Metodo auxiliar para imprimir las conexiones y verificar que son correctas
    void print_edges() {
        for (auto &p : edges) {
            cout << "Nodo: (" << p.first.fila << ", " << p.first.columna << ")\n";
            cout << "Vecinos: ";
            for (auto &n : p.second) {
                cout << "(" << n.fila << ", " << n.columna << ") ";
            }
            cout << "\n";
        }
    }
};



#endif //GRAPH_HPP
