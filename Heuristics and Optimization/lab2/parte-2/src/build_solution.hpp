//
// Created by golden on 12/19/24.
//

#ifndef BUILD_SOLUTION_HPP
#define BUILD_SOLUTION_HPP
#include <string>
#include <vector>

#include "structures/states.hpp"

using namespace std;
pair<vector<vector<string>>,size_t> get_solution_path(const shared_ptr<State>& estado);

void build_and_save(const vector<vector<string>> &solucion, const string &filename);

void guardar_stats(const string& path, const vector<size_t>& datos, long long tiempo);

#endif //BUILD_SOLUTION_HPP
