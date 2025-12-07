#!/usr/bin/env python3
"""
Python implementation of euler_check_graph using NetworkX.
Implements the same interface as the C++ version for direct comparison.
"""

import networkx as nx
from typing import List, Tuple


def euler_check_graph(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Check if a directed graph has an Eulerian cycle or path and return it.
    
    Args:
        n: Number of vertices (0 to n-1)
        edges: List of directed edges as (from, to) tuples
    
    Returns:
        List of vertices forming Eulerian cycle/path, or empty list if none exists
    """
    if n == 0 or not edges:
        return []

    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    
    if nx.has_eulerian_path(G) and nx.is_eulerian(G):
        circuit = list(nx.eulerian_circuit(G))
        path = [circuit[0][0]]
        for edge in circuit:
            path.append(edge[1])
        return path
    
    elif nx.has_eulerian_path(G):
        path_edges = list(nx.eulerian_path(G))
        path = [path_edges[0][0]]
        for edge in path_edges:
            path.append(edge[1])
        return path
    
    else:
        return []


if __name__ == '__main__':
    # example
    n = 5
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    
    result = euler_check_graph(n, edges)
    
    if result:
        print(f"Euler cycle/path found: {result}")
    else:
        print("No Euler cycle or path found or no edges in graph")
