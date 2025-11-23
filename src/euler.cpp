#include "../include/euler.hpp"

std::vector<size_t> euler_check_graph(const size_t n, const std::vector<std::pair<size_t, size_t>>& edges){
    // create adjacency list from edges list
    std::vector<std::vector<size_t>> adj(n);
    for (const auto& e : edges){
        adj[e.first].push_back(e.second);
    }
}