cmake_minimum_required(VERSION 3.20)
project(euler_graph_check)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)

# Source files
set(SOURCES
    src/euler.cpp
    src/utils.cpp
)

# Main executable
add_executable(euler_main ${SOURCES} src/main.cpp)

# Benchmark executable for Python comparison
add_executable(euler_benchmark ${SOURCES} src/benchmark.cpp)
