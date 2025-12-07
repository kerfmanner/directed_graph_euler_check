#include <iostream>
#include <vector>
#include <chrono>
#include "../include/euler.hpp"

int main() {
    // read input from stdin
    size_t n, num_edges;
    std::cin >> n >> num_edges;
    
    std::vector<std::pair<size_t, size_t>> edges;
    edges.reserve(num_edges);
    
    for (size_t i = 0; i < num_edges; ++i) {
        size_t from, to;
        std::cin >> from >> to;
        edges.push_back({from, to});
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    auto result = euler_check_graph(n, edges);
    auto end = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double, std::milli> duration = end - start;
    
    // in ms
    std::cout << "Time: " << duration.count() << " ms" << std::endl;
    
    return 0;
}
