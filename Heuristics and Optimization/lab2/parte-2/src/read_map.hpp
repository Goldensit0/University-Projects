//
// Created by golden on 12/16/24.
//

#ifndef READ_MAP_HPP
#define READ_MAP_HPP

#include <string>
#include <vector>
#include <fstream>
#include <utility>

#include "structures/graph.hpp"

// Recibe un path y devuelve un vector de strings con las lineas del archivo
using namespace std;
pair<vector<pair<size_t,size_t>>, vector<pair<size_t, size_t>>> get_positions(ifstream &file, const size_t &num_aviones);
Graph generate_map(ifstream &file);
#endif //READ_MAP_HPP
