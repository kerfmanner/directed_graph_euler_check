cmake_minimum_required(VERSION 3.20)
project(euler_graph_check)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

set(SOURCES
    src/euler.cpp
    src/utils.cpp
)

add_executable(euler_main ${SOURCES} src/main.cpp)

add_executable(benchmark ${SOURCES} src/graph_generator.cpp src/benchmark.cpp)

add_executable(euler_benchmark_wrapper ${SOURCES} src/euler_benchmark_wrapper.cpp)
