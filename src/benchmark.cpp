#include <iostream>
#include <chrono>
#include <vector>
#include <iomanip>
#include <fstream>
#include <ctime>
#include "../include/euler.hpp"

// graph generate functions
std::vector<std::pair<size_t, size_t>> generateEulerCycle(size_t n);
std::vector<std::pair<size_t, size_t>> generateEulerPath(size_t n);
std::vector<std::pair<size_t, size_t>> generateDenseEulerCycle(size_t n, size_t extra_edges);
std::vector<std::pair<size_t, size_t>> generateRandomGraph(size_t n, size_t num_edges);
std::vector<std::pair<size_t, size_t>> generateCompleteGraph(size_t n);

// benchmark func
template<typename Func>
double measureTime(Func&& func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> duration = end - start;
    return duration.count();
}

struct BenchmarkResult {
    std::string test_name;
    std::string graph_type;
    size_t vertices;
    size_t edges;
    double time_ms;
};

void benchmarkGraph(const std::string& test_name, const std::string& graph_type, 
                   size_t n, const std::vector<std::pair<size_t, size_t>>& edges,
                   std::vector<BenchmarkResult>& results) {
    double time_ms = measureTime([&]() {
        auto result = euler_check_graph(n, edges);
    });
    
    results.push_back({test_name, graph_type, n, edges.size(), time_ms});
    
    std::cout << std::setw(30) << std::left << test_name 
              << " | n=" << std::setw(6) << n 
              << " | edges=" << std::setw(8) << edges.size()
              << " | time=" << std::fixed << std::setprecision(3) << std::setw(10) << time_ms << " ms" 
              << std::endl;
}

void writeCSV(const std::vector<BenchmarkResult>& results, const std::string& filename) {
    const std::string results_dir = "../results";
    
    std::string full_path = results_dir + "/" + filename;
    
    std::ofstream file(full_path);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << full_path << " for writing" << std::endl;
        return;
    }
    
    // header
    file << "test_name,graph_type,vertices,edges,time_ms\n";
    
    //data
    for (const auto& result : results) {
        file << result.test_name << ","
             << result.graph_type << ","
             << result.vertices << ","
             << result.edges << ","
             << std::fixed << std::setprecision(6) << result.time_ms << "\n";
    }
    
    file.close();
    std::cout << "\nResults written to: " << full_path << std::endl;
}

int main() {
    std::vector<BenchmarkResult> results;
    
    // common test sizes(except complete graphs)
    std::vector<size_t> test_sizes = {100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000};
    
    std::cout << "=== Euler Graph Benchmark ===" << std::endl;
    std::cout << std::string(80, '-') << std::endl;
    
    // simple Euler cycles
    std::cout << "\n[1] Simple Euler Cycles:" << std::endl;
    for (size_t n : test_sizes) {
        auto edges = generateEulerCycle(n);
        benchmarkGraph("Simple Cycle", "euler_cycle", n, edges, results);
    }
    
    // simple euler paths
    std::cout << "\n[2] Simple Euler Paths:" << std::endl;
    for (size_t n : test_sizes) {
        auto edges = generateEulerPath(n);
        benchmarkGraph("Simple Path", "euler_path", n, edges, results);
    }
    
    // dense Euler cycles (with extra edges)
    std::cout << "\n[3] Dense Euler Cycles:" << std::endl;
    for (size_t n : test_sizes) {
        auto edges = generateDenseEulerCycle(n, n * 4);  // 4x more edges
        benchmarkGraph("Dense Cycle", "dense_euler_cycle", n, edges, results);
    }
    
    // random graphs
    std::cout << "\n[4] Random Graphs:" << std::endl;
    for (size_t n : test_sizes) {
        auto edges = generateRandomGraph(n, n * 2);
        benchmarkGraph("Random Graph", "random", n, edges, results);
    }
    
    // complete graphs
    std::cout << "\n[5] Complete Graphs:" << std::endl;
    for (size_t n : {100, 500, 1000, 2000, 5000}) {
        auto edges = generateCompleteGraph(n);
        benchmarkGraph("Complete Graph", "complete", n, edges, results);
    }
    
    std::cout << std::string(80, '-') << std::endl;
    
    writeCSV(results, "benchmark_results.csv");
    
    std::cout << "Benchmark completed!" << std::endl;
    
    return 0;
}
