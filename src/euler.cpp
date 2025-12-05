#include "../include/euler.hpp"
#include "../include/utils.hpp"

std::vector<size_t> euler_check_graph(const size_t n, const std::vector<std::pair<size_t, size_t>>& edges){
    // create adjacency list from edges list
    if (n == 0 || edges.empty()){
        return {};
    }

    GraphInfo graph_info;
    graph_info.in_deg.resize(n);
    graph_info.out_deg.resize(n);
    
    std::vector<std::vector<size_t>> adj(n);
    for (const auto& e : edges){
        adj[e.first].push_back(e.second);
        graph_info.out_deg[e.first]++;
        graph_info.in_deg[e.second]++;
    }

    // calculate in-degrees and out-degrees
    for (size_t i = 0; i < n; ++i){
        if (graph_info.out_deg[i] - graph_info.in_deg[i] == 1){
            graph_info.start_nodes++;
        } else if (graph_info.in_deg[i] - graph_info.out_deg[i] == 1){
            graph_info.end_nodes++;
        } else if (graph_info.in_deg[i] != graph_info.out_deg[i]){
            graph_info.degree_ok = false;
        }
    }

    graph_info.connected = isStronglyConnected(adj, n);

    if (hasEulerCycle(graph_info)){
        return getEulerCycle(adj);
    } else if (hasEulerPath(graph_info)){
        return getEulerPath(adj, graph_info);
    } else {
        return {};
    }
}