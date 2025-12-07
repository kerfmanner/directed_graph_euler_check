#!/usr/bin/env python3
"""
Comparison benchmark between C++ and Python (NetworkX) implementations.
"""

import subprocess
import time
import json
import os
import sys
from typing import List, Tuple
import pandas as pd

from euler_networkx import euler_check_graph as euler_check_graph_nx


def generate_euler_cycle(n: int) -> List[Tuple[int, int]]:
    """Generate a simple Euler cycle graph."""
    if n == 0:
        return []
    return [(i, (i + 1) % n) for i in range(n)]


def generate_euler_path(n: int) -> List[Tuple[int, int]]:
    """Generate a simple Euler path graph."""
    if n <= 1:
        return []
    return [(i, i + 1) for i in range(n - 1)]


def generate_dense_euler_cycle(n: int, extra_edges: int) -> List[Tuple[int, int]]:
    """Generate a dense Euler cycle with extra edges."""
    if n == 0:
        return []
    
    edges = [(i, (i + 1) % n) for i in range(n)]
    
    # add extra edges in pairs to maintain balance
    import random
    random.seed(42)
    for _ in range(extra_edges // 2):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        edges.append((u, v))
        edges.append((v, u))
    
    return edges


def generate_random_graph(n: int, num_edges: int) -> List[Tuple[int, int]]:
    """Generate a random directed graph."""
    if n == 0 or num_edges == 0:
        return []
    
    import random
    random.seed(123)
    edges = []
    for _ in range(num_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        edges.append((u, v))
    
    return edges


def benchmark_python(n: int, edges: List[Tuple[int, int]]) -> float:
    """Benchmark the Python NetworkX implementation."""
    start = time.perf_counter()
    result = euler_check_graph_nx(n, edges)
    end = time.perf_counter()
    # convert to ms
    return (end - start) * 1000


def benchmark_cpp(n: int, edges: List[Tuple[int, int]], cpp_program: str = './build/euler_benchmark_wrapper') -> float:
    """
    Benchmark the C++ implementation via a wrapper program.
    Returns time in milliseconds.
    """
    # temp input file
    input_data = f"{n}\n{len(edges)}\n"
    for u, v in edges:
        input_data += f"{u} {v}\n"
    
    try:
        result = subprocess.run(
            [cpp_program],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"C++ program error: {result.stderr}")
            return -1
        
        # parse time from output
        output = result.stdout.strip()
        if "Time:" in output:
            time_str = output.split("Time:")[1].strip().split()[0]
            return float(time_str)
        else:
            print(f"Unexpected output: {output}")
            return -1
    except subprocess.TimeoutExpired:
        print("C++ program timed out")
        return -1
    except FileNotFoundError:
        print(f"C++ program not found: {cpp_program}")
        print("You need to compile the C++ benchmark wrapper first.")
        return -1


def main():
    # test_sizes
    test_sizes = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    
    results = []
    
    print("=" * 80)
    print("C++ vs Python (NetworkX) Comparison Benchmark")
    print("=" * 80)
    
    # check if C++ wrapper exists
    cpp_available = os.path.exists('./build/euler_benchmark_wrapper')
    if not cpp_available:
        print("\nWARNING: C++ benchmark wrapper not found.")
        print("Only Python benchmarks will be run.")
        print("To enable C++ comparison, compile the wrapper first.\n")
    
    # simple Euler cycles
    print("\n[1] Simple Euler Cycles:")
    print("-" * 80)
    for n in test_sizes:
        edges = generate_euler_cycle(n)
        
        py_time = benchmark_python(n, edges)
        cpp_time = benchmark_cpp(n, edges) if cpp_available else -1
        
        results.append({
            'test_name': 'Simple Cycle',
            'graph_type': 'euler_cycle',
            'vertices': n,
            'edges': len(edges),
            'python_time_ms': py_time,
            'cpp_time_ms': cpp_time,
            'speedup': py_time / cpp_time if cpp_time > 0 and py_time > 0 else None
        })
        
        if cpp_available and cpp_time > 0:
            speedup = py_time / cpp_time
            print(f"n={n:6d} | Python: {py_time:8.3f} ms | C++: {cpp_time:8.3f} ms | "
                  f"Speedup: {speedup:6.2f}x")
        else:
            print(f"n={n:6d} | Python: {py_time:8.3f} ms")
    
    # simple Euler paths
    print("\n[2] Simple Euler Paths:")
    print("-" * 80)
    for n in test_sizes:
        edges = generate_euler_path(n)
        
        py_time = benchmark_python(n, edges)
        cpp_time = benchmark_cpp(n, edges) if cpp_available else -1
        
        results.append({
            'test_name': 'Simple Path',
            'graph_type': 'euler_path',
            'vertices': n,
            'edges': len(edges),
            'python_time_ms': py_time,
            'cpp_time_ms': cpp_time,
            'speedup': py_time / cpp_time if cpp_time > 0 and py_time > 0 else None
        })
        
        if cpp_available and cpp_time > 0:
            speedup = py_time / cpp_time
            print(f"n={n:6d} | Python: {py_time:8.3f} ms | C++: {cpp_time:8.3f} ms | "
                  f"Speedup: {speedup:6.2f}x")
        else:
            print(f"n={n:6d} | Python: {py_time:8.3f} ms")
    
    # dense Euler cycles
    print("\n[3] Dense Euler Cycles:")
    print("-" * 80)
    for n in test_sizes:
        edges = generate_dense_euler_cycle(n, n * 4)
        
        py_time = benchmark_python(n, edges)
        cpp_time = benchmark_cpp(n, edges) if cpp_available else -1
        
        results.append({
            'test_name': 'Dense Cycle',
            'graph_type': 'dense_euler_cycle',
            'vertices': n,
            'edges': len(edges),
            'python_time_ms': py_time,
            'cpp_time_ms': cpp_time,
            'speedup': py_time / cpp_time if cpp_time > 0 and py_time > 0 else None
        })
        
        if cpp_available and cpp_time > 0:
            speedup = py_time / cpp_time
            print(f"n={n:6d} | Python: {py_time:8.3f} ms | C++: {cpp_time:8.3f} ms | "
                  f"Speedup: {speedup:6.2f}x")
        else:
            print(f"n={n:6d} | Python: {py_time:8.3f} ms")
    
    # random Graphs
    print("\n[4] Random Graphs:")
    print("-" * 80)
    for n in test_sizes:
        edges = generate_random_graph(n, n * 2)
        
        py_time = benchmark_python(n, edges)
        cpp_time = benchmark_cpp(n, edges) if cpp_available else -1
        
        results.append({
            'test_name': 'Random Graph',
            'graph_type': 'random',
            'vertices': n,
            'edges': len(edges),
            'python_time_ms': py_time,
            'cpp_time_ms': cpp_time,
            'speedup': py_time / cpp_time if cpp_time > 0 and py_time > 0 else None
        })
        
        if cpp_available and cpp_time > 0:
            speedup = py_time / cpp_time
            print(f"n={n:6d} | Python: {py_time:8.3f} ms | C++: {cpp_time:8.3f} ms | "
                  f"Speedup: {speedup:6.2f}x")
        else:
            print(f"n={n:6d} | Python: {py_time:8.3f} ms")
    
    # save
    df = pd.DataFrame(results)
    output_file = 'results/comparison_results.csv'
    df.to_csv(output_file, index=False)
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {output_file}")
    
    if cpp_available:
        print("\n--- Summary Statistics ---")
        speedups = [r['speedup'] for r in results if r['speedup'] is not None]
        if speedups:
            print(f"Average C++ speedup: {sum(speedups)/len(speedups):.2f}x")
            print(f"Min speedup: {min(speedups):.2f}x")
            print(f"Max speedup: {max(speedups):.2f}x")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
