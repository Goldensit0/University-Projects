//
// Created by golden on 12/19/24.
//

#ifndef ASTAR_HPP
#define ASTAR_HPP
#include <utility>
#include <vector>
#include <algorithm>
#include <set>

#include "structures/states.hpp"

// Clase que implementa el algorithmo A* para resolver el problema. Contiene una lista de estados abiertos y cerrados.
// También contiene un grafo, representando el mapa del problema. La clase se inicializa con un estado inicial.
// La lista de abiertos es una cola de prioridad, ordenada por la f de los estados para facilitar su manejo.
// La lista de cerrados es un vector, ya que no necesitamos buscar en ella, solo comprobar si un estado está en ella.
// La clase se inicializa con un estado inicial, que se añade a la lista de abiertos como dice el algoritmo de A*.
using namespace std;
class ASTAR {
public:
    vector<shared_ptr<State>> open_list; // Lista de estados abiertos, ordenados por su f.
    vector<shared_ptr<State>> closed_list; // Lista de estados cerrados
    Graph &graph; // Grafo que representa el mapa

    explicit ASTAR(const shared_ptr<State> &estado_inicial, Graph &graph): graph(graph) {open_list.push_back(estado_inicial);}

    // Función que ejecuta el algoritmo A*. Devolverá el estado final, el cual contiene la solución gracias a los punteros
    // que referencian a los padres de cada estado y a las operaciones que llevaron a cada estado.

    pair<shared_ptr<State>, pair<size_t,size_t>> run() {
        size_t nodos_expandidos = 0;
        size_t h_inicial = open_list.front()->f_total; // Guardamos la f del estado inicial
        while (!open_list.empty()) {
            sort(open_list.begin(), open_list.end(),
                [](const shared_ptr<State>& a, const shared_ptr<State>&b) {return *a < *b;}); // Ordenamos la lista abierta

            // Sacamos el estado con menor f y lo eliminamos de la lista abierta
            auto current = open_list.front();
            open_list.erase(open_list.begin());

            if (current->is_goal()) { // Comprobamos si es el estado final y lo devolvemos
                return make_pair(current, make_pair(nodos_expandidos, h_inicial));
            }

            closed_list.push_back(current); // Lo añadimos a la lista de cerrados

            // Calculamos el nodo en el que está el avión que vamos a mover
            auto posicion_actual = current->aviones[current->next_plane].posicion;
            Node nodo_actual(posicion_actual.first, posicion_actual.second, false);
            auto vecinos = graph.get_neighbors(nodo_actual); // Obtenemos los vecinos del nodo

            auto sucesores = current->expand(vecinos); // Generamos los sucesores
            nodos_expandidos++;
            for (auto &sucesor : sucesores) {
                // Comprobamos si el sucesor está en la lista de cerrados
                if (find_if(closed_list.begin(), closed_list.end(),
                    [&sucesor](const shared_ptr<State>& s) { return *s == *sucesor; }) != closed_list.end()) {
                    continue; // Si está en cerrados, lo ignoramos
                }
                // Comprobamos si el sucesor está en la lista de abiertos
                auto encontrado = find_if(open_list.begin(), open_list.end(),
                    [&sucesor](const shared_ptr<State>& s) { return *s == *sucesor; });
                if (encontrado != open_list.end()) {
                    // Si está en abiertos, comprobamos si su f es menor que la que ya teníamos
                    if (*sucesor < **encontrado) {
                        open_list.erase(encontrado); // Si es menor, lo eliminamos de abiertos
                        open_list.push_back(sucesor); // Y añadimos el nuevo sucesor
                    }
                    continue;
                }

                open_list.push_back(sucesor); // Añadimos el nuevo sucesor
            }
        }
        throw runtime_error("No se ha encontrado solución"); // Si no hay solución, lanzamos una excepción
    }

};

#endif //ASTAR_HPP
