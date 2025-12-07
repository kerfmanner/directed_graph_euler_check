#include "../include/utils.hpp"


bool hasEulerCycle(const GraphInfo& graph_info){
    return graph_info.connected && graph_info.degree_ok &&
           graph_info.start_nodes == 0 && graph_info.end_nodes == 0;
}

bool hasEulerPath(const GraphInfo& graph_info){
    return graph_info.connected && graph_info.degree_ok &&
           graph_info.start_nodes <= 1 && graph_info.end_nodes <= 1;
}

// algorithm hierholzer
std::vector<size_t> hierholzer(std::vector<std::vector<size_t>> adj, size_t start) {
    std::stack<size_t> curr_path;
    std::vector<size_t> result;
    
    curr_path.push(start);
    size_t curr = start;
    
    while (!curr_path.empty()) {
        if (!adj[curr].empty()) {
            // not visited edge exists take it
            curr_path.push(curr);
            size_t next = adj[curr].back();
            adj[curr].pop_back();
            curr = next;
        } else {
            // if stuck add node to result
            result.push_back(curr);
            curr = curr_path.top();
            curr_path.pop();
        }
    }
    
    // reverse the order
    std::reverse(result.begin(), result.end());
    return result;
}

std::vector<size_t> getEulerCycle(std::vector<std::vector<size_t>> adj){
    size_t n = adj.size();
    if (n == 0) return {};
    
    size_t start = 0;
    for (size_t i = 0; i < n; ++i) {
        if (!adj[i].empty()) {
            start = i;
            break;
        }
    }
    
    return hierholzer(std::move(adj), start);
}

std::vector<size_t> getEulerPath(std::vector<std::vector<size_t>> adj, const GraphInfo& graph_info){
    size_t n = adj.size();
    if (n == 0) return {};

    size_t start = graph_info.starting_node;
    
    return hierholzer(std::move(adj), start);
}

bool isEulerConnected(const std::vector<std::vector<size_t>>& adj)
{
    size_t n = adj.size();
    std::vector<std::vector<size_t>> reverse_adj(n);
    std::vector<bool> active(n, false);

    for (size_t i = 0; i < n; i++) {
        for (size_t v : adj[i]) {
            reverse_adj[v].push_back(i);
            active[i] = true;
            active[v] = true;
        }
    }

    size_t start = n;
    for (size_t i = 0; i < n; i++) {
        if (active[i]) {
            start = i;
            break;
        }
    }

    if (start == n)
        return true;

    auto dfs = [&](const std::vector<std::vector<size_t>>& g) {
        std::vector<bool> visited(n, false);
        std::stack<size_t> st;
        st.push(start);

        while (!st.empty()) {
            size_t curr = st.top();
            st.pop();

            if (visited[curr]) continue;
            visited[curr] = true;

            for (size_t v : g[curr])
                if (!visited[v])
                    st.push(v);
        }

        for (size_t i = 0; i < n; i++)
            if (active[i] && !visited[i])
                return false;

        return true;
    };

    return dfs(adj) && dfs(reverse_adj);
}

