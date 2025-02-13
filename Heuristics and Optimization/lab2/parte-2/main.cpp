//
// Created by golden on 12/16/24.
//


#include <chrono>
#include <fstream>
#include <iostream>
#include <span>

#include "src/ASTAR.hpp"
#include "src/build_solution.hpp"
#include "src/read_map.hpp"
#include "src/structures/floyd-warshall.hpp"
#include "src/structures/graph.hpp"
#include "src/structures/states.hpp"

// Recibe un csv con el mapa y un numero (1 o 2) para seleccionar la heurística
int main(int argc, const char *argv[]) {
    std::span args(argv, static_cast<size_t>(argc)); // Acceso seguro a los argumentos
    // Comprobación de argumentos
    if (args.size() != 3) {
        std::cerr << "Uso: " << args[0] << " <path-al-mapa.csv> <num-heuristica>\n";
        exit(1);
    }

    // Abre el archivo
    std::ifstream file(args[1]);
    if (not file.is_open()) {
        std::cerr << "Error: No se pudo abrir el archivo " << "\n";
        exit(1);
    }

    // Comprueba la heurística (para confirmar que el comando es válido)
    std::string heu = args[2];
    if (heu != "1" && heu != "2") {
        std::cerr << "Error: La heurística debe ser 1 o 2" << "\n";
        exit(1);
    }
    size_t heuristica = static_cast<size_t>(std::stoi(args[2]));

    // Leemos el número de aviones
    std::string line;
    if (not std::getline(file, line)) {
        std::cerr << "Error: No se pudo leer el número de aviones" << "\n";
        exit(1);
    }
    auto num_aviones = static_cast<size_t>(std::stoi(line));

    // Leemos las posiciones iniciales y finales de los aviones
    auto [posiciones_iniciales, posiciones_finales] = get_positions(file, num_aviones);

    // Generamos el mapa
    auto mapa = generate_map(file);

    // Comprobamos que las posiciones son alcanzables (están conectadas a algo) para tratar de descartar casos base.
    auto edges = mapa.get_edges();
    for (auto &pos : posiciones_iniciales) {
        if (edges.find(Node(pos.first, pos.second, false)) == edges.end()) {
            std::cerr << "Error: La posición inicial (" << pos.first << "," << pos.second << ") no es accesible" << "\n";
            exit(1);
        }
    }
    for (auto &pos : posiciones_finales) {
        if (edges.find(Node(pos.first, pos.second, false)) == edges.end()) {
            std::cerr << "Error: La posición final (" << pos.first << "," << pos.second << ") no es accesible" << "\n";
            exit(1);
        }
    }

    FloydWarshall distancias(edges);
    // Si la heurística es 2, generamos la tabla de distancias de Floyd-Warshall
    if (heuristica == 2) {
        distancias.build(edges);
    // Si la heuristica es 1, no necesitamos generar la tabla. Usamos distancia de Manhattan.
    } else {
        distancias.is_FloydWarshall = false;
    }

    // Creamos el vector de aviones
    std::vector<Avion> aviones;
    for (size_t i = 0; i < num_aviones; i++) {
        auto posicion_inicial = posiciones_iniciales[i];
        auto posicion_final = posiciones_finales[i];
        auto nodo = mapa.get_node(posicion_inicial.first, posicion_inicial.second);
        aviones.emplace_back(posicion_inicial, posicion_final, nodo.amarillo, 0);
    }

    // Creamos el estado inicial
    auto estado_inicial = std::make_shared<State>(aviones, 0, nullptr, "S", distancias);

    // Creamos el objeto A* y ejecutamos el algoritmo
    ASTAR astar(estado_inicial, mapa);
    try {
        auto start = std::chrono::high_resolution_clock::now();
        auto solucion = astar.run();
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start);

        std::cout << "Solución encontrada, guardando..." << "\n";
        // Construimos la ruta de la solución de cada avión
        auto path = get_solution_path(solucion.first);
        auto camino = path.first;
        // Lo guardamos en un archivo
        size_t nodos_expandidos = solucion.second.first;
        size_t f_total = solucion.second.second;
        size_t makespan = camino[0].size();

        std::string mapname = args[1];
        std::string filename = mapname + "-" + heu;
        build_and_save(camino, filename);
        guardar_stats(filename, {makespan, f_total, nodos_expandidos}, duration.count());

    } catch (std::exception &e) { // No se encontró solución.
        std::cerr << "Error: " << e.what() << "\n";
        exit(1);
    }
    return 0;
}
