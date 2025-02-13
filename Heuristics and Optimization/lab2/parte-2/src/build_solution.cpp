//
// Created by golden on 12/19/24.
//

#include "build_solution.hpp"

#include <algorithm>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;
// Función que reconstruye el camino de la solución a partir del estado final.
pair<vector<vector<string>>,size_t> get_solution_path(const shared_ptr<State>& estado) {
    vector<vector<string>> solucion;
    // Recorremos los padres de cada estado, añadiendo la acción que llevó a ese estado a la solución.
    auto current = estado;

    // Añadimos las posiciones en las que han quedado los aviones
    for (auto avion : current->aviones) {
        string posicion = "(" + to_string(avion.posicion.first) + "," + to_string(avion.posicion.second) + ")";
        solucion.emplace_back(vector{posicion});
    }

    size_t numero_aviones = current->aviones.size();
    while (current->padre != nullptr) { // Iteramos hasta llegar al estado inicial
        size_t avion = current->next_plane; // Calculamos el avión que se movió en este estado
        if (avion == 0) {
            avion = numero_aviones - 1; // Caso en el que se movió el último avión.
        } else {
            avion--; // Si no, cogemos el anterior
        }
        string accion = current->accion;
        string posicion_y_accion; // Calculamos la posición anterior en función de la acción
        size_t fila = current->aviones[avion].posicion.first;
        size_t columna = current->aviones[avion].posicion.second;
        if (accion == "↑") {
            fila++;
        } else if (accion == "↓") {
            fila--;
        } else if (accion == "→") {
            columna--;
        } else if (accion == "←") {
            columna++;
        }

        // Construimos la cadena con la posición y la acción y la insertamos en la solución del avión n.
        posicion_y_accion = "(" + to_string(fila) + "," + to_string(columna) + ") " + accion + " ";
        solucion[avion].emplace_back(posicion_y_accion);

        // Pasamos al estado anterior
        current = current->padre;
    }

    // Invertimos las rutas para que la solución esté en el orden correcto.
    for (auto &ruta : solucion) {
        reverse(ruta.begin(), ruta.end());
    }
    return make_pair(solucion, current->f_calcular()); // Devolvemos la solución y la f del estado inicial
}


void build_and_save(const vector<vector<string>> &solucion, const string &fullpath) {
    // Abrir archivo en la carpeta ASTAR-tests con el nombre filename.output
    string outputFilePath = fullpath + ".output";
    ofstream outputFile(outputFilePath);
    if (!outputFile.is_open()) {
        cerr << "Error: No se pudo abrir el archivo " << fullpath << "\n";
        return;
    }
    // Guardamos las soluciones de los n aviones en el archivo
    for (const auto &fila : solucion) {
        ostringstream concatenated;
        for (const auto &substr : fila) { // Concatenamos cada string de la solucion del avion n.
            concatenated << substr; // Concatenamos cada string del avion n.
        }
        outputFile << concatenated.str() << "\n";
    }
    outputFile.close(); // Cerramos el archivo
}

void guardar_stats(const string& path, const vector<size_t>& datos, long long tiempo) {
    // Abrimos el archivo en modo de escritura (si no existe, lo crea)
    string outputFilePath = path + ".stat";
    ofstream archivo(outputFilePath);

    // Verificamos si el archivo se ha abierto correctamente
    if (!archivo) {
        cerr << "No se pudo abrir el archivo para escribir." << endl;
        return;
    }

    // Escribimos los datos en el archivo con el formato deseado
    archivo << "Tiempo total: " << tiempo << "s\n";      // El primer valor es el tiempo total
    archivo << "Makespan: " << datos[1] << "\n";            // El segundo valor es el makespan
    archivo << "h inicial: " << datos[2] << "\n";          // El tercer valor es h inicial
    archivo << "Nodos expandidos: " << datos[3] << "\n";   // El cuarto valor es el número de nodos expandidos

    archivo.close(); // Cerramos el archivo
}

