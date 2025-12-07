#include <vector>
#include <random>
#include <algorithm>
#include <utility>

// generate a directed Euler cycle graph
// creates a simple cycle: 0->1->2->...->n-1->0
std::vector<std::pair<size_t, size_t>> generateEulerCycle(size_t n) {
    std::vector<std::pair<size_t, size_t>> edges;
    if (n == 0) return edges;
    
    for (size_t i = 0; i < n; ++i) {
        edges.push_back({i, (i + 1) % n});
    }
    return edges;
}

// generate a directed Euler path graph (has path but not cycle)
// creates: 0->1->2->...->n-1
std::vector<std::pair<size_t, size_t>> generateEulerPath(size_t n) {
    std::vector<std::pair<size_t, size_t>> edges;
    if (n <= 1) return edges;
    
    for (size_t i = 0; i < n - 1; ++i) {
        edges.push_back({i, i + 1});
    }
    return edges;
}

// Generate a dense Euler cycle graph with multiple edges
std::vector<std::pair<size_t, size_t>> generateDenseEulerCycle(size_t n, size_t extra_edges) {
    std::vector<std::pair<size_t, size_t>> edges;
    if (n == 0) return edges;
    
    // Base cycle
    for (size_t i = 0; i < n; ++i) {
        edges.push_back({i, (i + 1) % n});
    }
    
    // extra edges in pairs to maintain balance
    std::mt19937 rng(42);
    std::uniform_int_distribution<size_t> dist(0, n - 1);
    
    for (size_t i = 0; i < extra_edges / 2; ++i) {
        size_t u = dist(rng);
        size_t v = dist(rng);

        edges.push_back({u, v});
        edges.push_back({v, u});
    }
    
    return edges;
}

// Generate a random directed graph
std::vector<std::pair<size_t, size_t>> generateRandomGraph(size_t n, size_t num_edges) {
    std::vector<std::pair<size_t, size_t>> edges;
    if (n == 0 || num_edges == 0) return edges;
    
    std::mt19937 rng(123);
    std::uniform_int_distribution<size_t> dist(0, n - 1);
    
    for (size_t i = 0; i < num_edges; ++i) {
        size_t from = dist(rng);
        size_t to = dist(rng);
        edges.push_back({from, to});
    }
    
    return edges;
}

// Generate complete directed graph
std::vector<std::pair<size_t, size_t>> generateCompleteGraph(size_t n) {
    std::vector<std::pair<size_t, size_t>> edges;
    if (n <= 1) return edges;
    
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            if (i != j) {
                edges.push_back({i, j});
            }
        }
    }
    
    return edges;
}