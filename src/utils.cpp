#include "../include/utils.hpp"
#include <stack>


bool hasEulerCycle(const GraphInfo& graph_info){
    return graph_info.connected && graph_info.degree_ok &&
           graph_info.start_nodes == 0 && graph_info.end_nodes == 0;
}

bool hasEulerPath(const GraphInfo& graph_info){
    return graph_info.connected && graph_info.degree_ok &&
           graph_info.start_nodes <= 1 && graph_info.end_nodes <= 1;
}

// Алгоритм Ієрхольцера для пошуку Ейлерового циклу/шляху
std::vector<size_t> hierholzer(std::vector<std::vector<size_t>> adj, size_t start) {
    std::stack<size_t> curr_path;
    std::vector<size_t> result;
    
    curr_path.push(start);
    size_t curr = start;
    
    while (!curr_path.empty()) {
        if (!adj[curr].empty()) {
            // Є невідвідане ребро - йдемо по ньому
            curr_path.push(curr);
            size_t next = adj[curr].back();
            adj[curr].pop_back();
            curr = next;
        } else {
            // Застрягли - додаємо вершину в результат
            result.push_back(curr);
            curr = curr_path.top();
            curr_path.pop();
        }
    }
    
    // Результат в зворотному порядку
    std::reverse(result.begin(), result.end());
    return result;
}

std::vector<size_t> getEulerCycle(std::vector<std::vector<size_t>> adj){
    size_t n = adj.size();
    if (n == 0) return {};
    
    // Знаходимо стартову вершину (будь-яку з ребрами)
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
    
    // Використовуємо вже обчислені степені з GraphInfo
    // Для Ейлерового шляху: вершина де out_degree > in_degree
    size_t start = 0;
    
    for (size_t i = 0; i < n; ++i) {
        if (graph_info.out_deg[i] > graph_info.in_deg[i]) {
            start = i;
            break;
        }
        if (!adj[i].empty()) {
            start = i;
        }
    }
    
    return hierholzer(std::move(adj), start);
}

void dfs(size_t start, const std::vector<std::vector<size_t>>& adj, std::vector<bool>& visited) {
    std::stack<size_t> stack;
    stack.push(start);
    
    while (!stack.empty()) {
        size_t v = stack.top();
        stack.pop();
        
        if (visited[v]) continue;
        
        visited[v] = true;
        for (size_t u : adj[v]) {
            if (!visited[u]) {
                stack.push(u);
            }
        }
    }
}

bool isStronglyConnected(const std::vector<std::vector<size_t>>& adj, size_t n) {
    if (n == 0) return true;
    
    size_t start = 0;
    bool found = false;
    for (size_t i = 0; i < n; ++i) {
        if (!adj[i].empty()) {
            start = i;
            found = true;
            break;
        }
    }
    
    if (!found) return true;
    
    std::vector<bool> visited(n, false);
    dfs(start, adj, visited);
    
    for (size_t i = 0; i < n; ++i) {
        if (!adj[i].empty() && !visited[i]) {
            return false;
        }
    }
    
    std::vector<std::vector<size_t>> reversed_adj(n);
    for (size_t u = 0; u < n; ++u) {
        for (size_t v : adj[u]) {
            reversed_adj[v].push_back(u);
        }
    }
    
    std::fill(visited.begin(), visited.end(), false);
    dfs(start, reversed_adj, visited);
    
    for (size_t i = 0; i < n; ++i) {
        if (!adj[i].empty() && !visited[i]) {
            return false;
        }
    }
    
    return true;
}