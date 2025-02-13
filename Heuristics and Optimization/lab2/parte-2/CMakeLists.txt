cmake_minimum_required(VERSION 3.22)
project(parte-2 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_compile_options(-Wall -Wextra -pedantic -pedantic-errors
        -Wconversion -Wsign-conversion)

add_executable(ASTARRodaje main.cpp
        src/read_map.hpp
        src/read_map.cpp
        src/structures/graph.hpp
        src/structures/aviones.hpp
        src/structures/states.hpp
        src/structures/floyd-warshall.hpp
        src/ASTAR.hpp
        src/build_solution.hpp
        src/build_solution.cpp)