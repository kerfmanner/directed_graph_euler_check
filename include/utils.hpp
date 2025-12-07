//
// Created by konov on 11/23/2025.
//

#ifndef HMW_3_UTILS_HPP
#define HMW_3_UTILS_HPP

#include <vector>
#include <algorithm>
#include <stack>

struct GraphInfo {
    std::vector<size_t> in_deg, out_deg;
    bool connected = true;
    bool degree_ok = true;

    // euler trail conditions the amount of starting and ending nodes
    // both of them should be <= 1 for euler path to exist
    size_t start_nodes = 0;
    size_t end_nodes = 0;

    size_t starting_node = 0;
};

bool hasEulerCycle(const GraphInfo& graph_info);
bool hasEulerPath(const GraphInfo& graph_info);
std::vector<size_t> getEulerCycle(std::vector<std::vector<size_t>> adj);
std::vector<size_t> getEulerPath(std::vector<std::vector<size_t>> adj, const GraphInfo& graph_info);
std::pair<std::vector<size_t>, GraphInfo> get_graph_info(const size_t n, const std::vector<std::pair<size_t, size_t>>& edges);
bool isEulerConnected(const std::vector<std::vector<size_t>>& adj);
#endif //HMW_3_UTILS_HPP