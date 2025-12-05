#include <iostream>
#include <vector>
#include "../include/euler.hpp"

int main() {
    // Приклад використання
    size_t n = 5;
    std::vector<std::pair<size_t, size_t>> edges = {
        {0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}
    };
    
    auto result = euler_check_graph(n, edges);
    
    if (result.empty()) {
        std::cout << "No Euler cycle or path found" << std::endl;
    } else {
        std::cout << "Euler cycle/path: ";
        for (size_t v : result) {
            std::cout << v << " ";
        }
        std::cout << std::endl;
    }
    
    return 0;
}
