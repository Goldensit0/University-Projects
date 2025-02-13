//
// Created by golden on 12/16/24.
//

#include "read_map.hpp"

#include <cstring>
#include <iostream>
#include <sstream>

using namespace std;
pair<vector<pair<size_t,size_t>>, vector<pair<size_t, size_t>>> get_positions(ifstream &file, const size_t &num_aviones){
    vector<pair<size_t,size_t>> posiciones_iniciales, posicion_finales;
    string line;
    for (size_t i = 0; i < num_aviones; i++) {
        if (not getline(file, line)) {
            cerr << "Error: No se pudo leer el número de aviones" << "\n";
            exit(1);
        }

        // Sacar las posiciones fila objetivos del avion
        istringstream ss(line);
        string pos_inicial_i, pos_final_i;
        if (not getline(ss, pos_inicial_i, ')')) {
            cerr << "Error: No se pudo leer la posicion inicial" << "\n";
            exit(1);
        }
        if (not getline(ss, pos_final_i, ')')) {
            cerr << "Error: No se pudo leer la posicion final" << "\n";
            exit(1);
        }

        // Elimina los espacios/tabulaciones
        pos_inicial_i.erase(0, pos_inicial_i.find_first_not_of(" \t"));
        pos_final_i.erase(0, pos_final_i.find_first_not_of(" \t"));
        // Eliminar los paréntesis iniciales
        pos_inicial_i = pos_inicial_i.substr(1);
        pos_final_i = pos_final_i.substr(1);

        // Crear dos streams para leer las posiciones
        istringstream ss1(pos_inicial_i), ss2(pos_final_i);
        string x1, y1, x2, y2;

        // Leer las posiciones
        getline(ss1, x1, ',');
        getline(ss1, y1);
        getline(ss2, x2, ',');
        getline(ss2, y2);

        // Convertir los valores a enteros fila añadir a las posiciones iniciales
        posiciones_iniciales.emplace_back(stoi(x1), stoi(y1));
        posicion_finales.emplace_back(stoi(x2), stoi(y2));
    }
    return make_pair(posiciones_iniciales, posicion_finales);
}

// Función que conecta el nodo actual (en la posicion fila, columna) con el de inmediatamente a la izquierda en el mapa
bool connect_with_previous(Graph &mapa, size_t fila, size_t columna) {
    try { // Añade la arista con el nodo anterior, si era transitable
        auto prev_node = mapa.get_node(fila, columna-1);
        auto this_node = mapa.get_node(fila,columna);
        mapa.add_edge(prev_node, this_node);
        mapa.add_edge(this_node, prev_node);
    } catch (exception &e){
        return true;
    }
    return false;
}

// Función que conecta el nodo actual (en la posicion columna,fila) con el de inmediatamente encima en el mapa
bool connect_with_upper(Graph &mapa, size_t fila, size_t columna) {
    try { // Añade la arista con el nodo de encima, si era transitable
        auto prev_node = mapa.get_node(fila-1,columna);
        auto this_node = mapa.get_node(fila,columna);
        mapa.add_edge(prev_node, this_node);
        mapa.add_edge(this_node, prev_node);
    } catch (exception &e){
        return true;
    }
    return false;
}

// Función que recibe el archivo abierto fila genera el grafo de nodos fila aristas
Graph generate_map(ifstream &file) {
    Graph mapa;
    string line;
    vector characters = {';', 'B', 'A'};

    // Variables de control
    size_t columna = 0, fila = 0;
    // Leemos la línea (fila) del archivo
    while (getline(file, line)) {
        // Caracter a caracter, comprobamos las casillas
        for (char c : line) {
            // Siguiente columna
            if (c == characters[0]) {
                columna++;
            // Casilla normal
            } else if (c == characters[1]) {
                mapa.add_node(Node(fila, columna, false));
                if (columna > 0) {
                    connect_with_previous(mapa, fila, columna);
                }
                if (fila >0) {
                    connect_with_upper(mapa, fila, columna);
                }
            // Casilla amarilla
            } else if (c == characters[2]) {
                mapa.add_node(Node(fila, columna, true));
                if (columna > 0) {
                    connect_with_previous(mapa, fila, columna);
                }
                if (fila >0) {
                    connect_with_upper(mapa, fila, columna);
                }
            // Casilla no transitable u otro caso
            } else { continue; }
        }
        // Siguiente fila
        fila++;
        columna=0;
    }

    // No quedan más líneas en el fichero, revolvemos el mapa
    return mapa;
}