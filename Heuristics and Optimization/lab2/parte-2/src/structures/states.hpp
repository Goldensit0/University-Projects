//
// Created by golden on 12/18/24.
//

#ifndef STATE_HPP
#define STATE_HPP
#include <memory>
#include <unistd.h>
#include <utility>
#include <vector>

#include "aviones.hpp"

using namespace std;
// Clase que representa un estado de nuestro problema de búsqueda.
// Se forma por un conjunto de aviones, que contienen cada uno un coste y una heuristica parcial.
// La f total se calcula a partir del máximo de las sumas de g y h.
// La varible next_plane se usa para saber que avión se moverá a continuación (posición en el vector de aviones).
// Además, tiene un puntero al estado padre y la acción que llevó a este estado, para reconstruir la ruta.

// La clase tiene una funcion expand que devuelve los estados sucesores, generados a partir de mover el avión actual
// a las posiciones validas, comprobadas antes de crear el estado resultante.
class State : public enable_shared_from_this<State>{
public:
    vector<Avion> aviones;
    size_t next_plane;
    shared_ptr<State> padre; // Puntero al estado padre
    string accion; // Acción que llevó a este estado
    FloydWarshall & tabla_distancias; // Referencia a la tabla de distancias
    size_t f_total; // f total del estado

    // Constructor
    State(vector<Avion> aviones, size_t next_plane, shared_ptr<State> padre, string accion, FloydWarshall &tabla_distancias) :
    aviones(move(aviones)), next_plane(next_plane), padre(move(padre)), accion(move(accion)), tabla_distancias(tabla_distancias) {
        f_total = f_calcular();
    }

    State(const State& otro) : enable_shared_from_this<State>(),
        aviones(otro.aviones), next_plane(otro.next_plane), padre(otro.padre),
        accion(otro.accion), tabla_distancias(otro.tabla_distancias), f_total(otro.f_total) {}

    State(State&& otro) noexcept : aviones(move(otro.aviones)), next_plane(otro.next_plane), padre(move(otro.padre)),
        accion(move(otro.accion)), tabla_distancias(otro.tabla_distancias), f_total(otro.f_total) {}

    State& operator=(const State& otro) {
        if (this != &otro) { // Protección contra asignacion a si mismo
            aviones = otro.aviones;
            next_plane = otro.next_plane;
            padre = otro.padre;
            accion = otro.accion;
            tabla_distancias = otro.tabla_distancias;
            f_total = otro.f_total;
        }
        return *this;
    }

    State& operator=(State&& otro) noexcept {
        if (this != &otro) { // Protección contra asignacion a si mismo
            aviones = move(otro.aviones);
            next_plane = otro.next_plane;
            padre = move(otro.padre);
            accion = move(otro.accion);
            tabla_distancias = otro.tabla_distancias;
            f_total = otro.f_total;
        }
        return *this;
    }



    // Operadores de comparación para la cola de prioridad
    bool operator<(const State &otro) const {
        return f_total < otro.f_total;
    }
    bool operator>(const State &otro) const {
        return f_total > otro.f_total;
    }
    bool operator==(const State &otro) const {
        return (aviones==otro.aviones && next_plane == otro.next_plane  && accion == otro.accion);
    }

    // Comprobación de si un estado es el estado final
    [[nodiscard]] bool is_goal() const {
        if (next_plane != 0){ return false; } // Si no hemos movido todos los aviones, no es el estado final
        for (const auto &avion : aviones) { // Comprobamos posición de todos los aviones
            if (avion.posicion != avion.destino) {
                return false;
            }
        }
        return true;
    }

    // Calcula la f de este estado (suma de g y h)
    [[nodiscard]] size_t f_calcular() const {
        size_t max = 0;
        for (auto &avion : aviones) {
            size_t new_f = avion.g_coste + avion.heuristica(tabla_distancias);
            if (new_f > max) {
                max = new_f;
            }
        }
        return max;
    }

    // Devuelve un vector de estados, resultado de expandir los posibles.
    // Se generan los estados resultantes de mover el avión actual en las 4 direcciones posibles y esperar.
    [[nodiscard]] vector<shared_ptr<State>> expand(const vector<Node>& vecinos) {
        vector<shared_ptr<State>> sucesores;
        // Precondicion para mover arriba
        if (aviones[next_plane].posicion.first > 0){ // No estamos pegados al borde
            auto nueva_pos = make_pair(aviones[next_plane].posicion.first-1, aviones[next_plane].posicion.second);
            auto existe_amarillo = exists_y_amarillo(Node(nueva_pos.first, nueva_pos.second, false), vecinos);
            if (existe_amarillo.first) { // Si la casilla existe (transitable)
                bool colision = false;
                for (const auto &avion : aviones) { // Comprobación de colisión
                    if (avion.posicion == nueva_pos) {
                        colision = true;
                    }
                }
                if (!colision) { // Si no hay colision, lo podemos mover
                    sucesores.push_back(move_up(existe_amarillo.second));
                }
            }
        }
        // Precondicion para mover abajo (no necesitamos comprobar el borde, sirve con comprobar que la casilla existe)
        auto nueva_pos_abajo = make_pair(aviones[next_plane].posicion.first+1, aviones[next_plane].posicion.second);
        auto abajo = exists_y_amarillo(Node(nueva_pos_abajo.first, nueva_pos_abajo.second, false), vecinos);
        if (abajo.first) { // Si la casilla existe (transitable)
            bool colision = false;
            for (const auto &avion : aviones) { // Comprobación de colisión
                if (avion.posicion == nueva_pos_abajo) {
                    colision = true;
                }
            }
            if (!colision) { // Si no hay colision, lo podemos mover
                sucesores.push_back(move_down(abajo.second));
            }
        }
        // Precondicion para mover izquierda
        if (aviones[next_plane].posicion.second > 0){ // No estamos pegados al borde
            auto nueva_pos = make_pair(aviones[next_plane].posicion.first, aviones[next_plane].posicion.second-1);
            auto existe_amarillo = exists_y_amarillo(Node(nueva_pos.first, nueva_pos.second, false), vecinos);
            if (existe_amarillo.first) { // Si la casilla existe (transitable)
                bool colision = false;
                for (const auto &avion : aviones) { // Comprobación de colisión
                    if (avion.posicion == nueva_pos) {
                        colision = true;
                    }
                }
                if (!colision) { // Si no hay colision, lo podemos mover
                    sucesores.push_back(move_left(existe_amarillo.second));
                }
            }
        }
        // Precondicion para mover derecha (no necesitamos comprobar el borde, sirve con comprobar que la casilla existe)
        auto nueva_pos_derecha = make_pair(aviones[next_plane].posicion.first, aviones[next_plane].posicion.second+1);
        auto derecha = exists_y_amarillo(Node(nueva_pos_derecha.first, nueva_pos_derecha.second, false), vecinos);
        if (derecha.first) { // Si la casilla existe (transitable)
            bool colision = false;
            for (const auto &avion : aviones) { // Comprobación de colisión
                if (avion.posicion == nueva_pos_derecha) {
                    colision = true;
                }
            }
            if (!colision) { // Si no hay colision, lo podemos mover
                sucesores.push_back(move_right(derecha.second));
            }
        }
        // Precondicion para esperar
        if (!aviones[next_plane].en_amarillo) {
            // Si estamos en una casilla amarilla, no podemos esperar
            sucesores.push_back(wait());
        }
        return sucesores;
    }

private:
    // Posibles operadores de movimiento
    // Cada uno de ellos crea un nuevo estado con el avión movido y actualiza la heurística

    shared_ptr<State> move_up(bool amarillo) {
        // Movemos el avion hacia arriba
        auto new_aviones = aviones;
        new_aviones[next_plane].posicion.first -= 1;
        new_aviones[next_plane].en_amarillo = amarillo;
        new_aviones[next_plane].g_coste +=1;
        // Calculamos la nueva heurística, maximo entre la anterior y la nueva distancia del avión,
        // ya que el resto de distancias no se han modificado.
        size_t new_next_plane = next_plane+1;
        if (new_next_plane == aviones.size()) { // Si hemos movido el último avión, pasamos al primero
            new_next_plane = 0;
        }
        return make_shared<State>(new_aviones, new_next_plane, shared_from_this(), "↑", tabla_distancias);
    }

    shared_ptr<State> move_down(bool amarillo) {
        // Movemos el avion hacia abajo
        auto new_aviones = aviones;
        new_aviones[next_plane].posicion.first += 1;
        new_aviones[next_plane].en_amarillo = amarillo;
        new_aviones[next_plane].g_coste +=1;
        // Calculamos la nueva heurística, maximo entre la anterior y la nueva distancia del avión,
        // ya que el resto de distancias no se han modificado.
        size_t new_next_plane = next_plane+1;
        if (new_next_plane == aviones.size()) { // Si hemos movido el último avión, pasamos al primero
            new_next_plane = 0;
        }
        return make_shared<State>(new_aviones, new_next_plane, shared_from_this(), "↓", tabla_distancias);
    }

    shared_ptr<State> move_right(bool amarillo) {
        // Movemos el avion hacia la derecha
        auto new_aviones = aviones;
        new_aviones[next_plane].posicion.second += 1;
        new_aviones[next_plane].en_amarillo = amarillo;
        new_aviones[next_plane].g_coste +=1;
        // Calculamos la nueva heurística, maximo entre la anterior y la nueva distancia del avión,
        // ya que el resto de distancias no se han modificado.
        size_t new_next_plane = next_plane+1;
        if (new_next_plane == aviones.size()) { // Si hemos movido el último avión, pasamos al primero
            new_next_plane = 0;
        }
        return make_shared<State>(new_aviones, new_next_plane, shared_from_this(), "→", tabla_distancias);
    }

    shared_ptr<State> move_left(bool amarillo) {
        // Movemos el avion hacia la izquierda
        auto new_aviones = aviones;
        new_aviones[next_plane].posicion.second -= 1;
        new_aviones[next_plane].en_amarillo = amarillo;
        new_aviones[next_plane].g_coste +=1;
        // Calculamos la nueva heurística, maximo entre la anterior y la nueva distancia del avión,
        // ya que el resto de distancias no se han modificado.
        size_t new_next_plane = next_plane+1;
        if (new_next_plane == aviones.size()) { // Si hemos movido el último avión, pasamos al primero
            new_next_plane = 0;
        }
        return make_shared<State>(new_aviones, new_next_plane, shared_from_this(), "←", tabla_distancias);
    }

    shared_ptr<State> wait() {
        // No movemos el avión, pero gastamos tiempo
        auto new_aviones = aviones;
        size_t new_next_plane = next_plane+1;
        new_aviones[next_plane].g_coste += 1;
        if (new_next_plane == aviones.size()) { // Si hemos usado el último avión, pasamos al primero
            new_next_plane = 0;
        }
        return make_shared<State>(new_aviones, new_next_plane, shared_from_this(), "w", tabla_distancias);
    }

    // Comprobaciones de existencia de un nodo en un vector, para no generar estados invalidos
    static pair<bool,bool> exists_y_amarillo(const Node &n, const vector<Node> &vecinos) {
        // Comprobamos que exista la casilla a la que nos queremos mover
        for (const auto &v : vecinos) {
            if (v == n) {
                if (v.amarillo) {
                    return make_pair(true, true);
                }
                return make_pair(true, false);
            }
        }
        return make_pair(false, false);
    }
};
#endif //STATE_HPP
