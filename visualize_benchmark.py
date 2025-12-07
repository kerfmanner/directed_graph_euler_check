#!/usr/bin/env python3
"""
Visualization script for Euler graph benchmark results.
Reads benchmark_results.csv and comparison_results.csv and creates performance plots.

Usage:
    python3 visualize_benchmark.py [benchmark|comparison|all]

Modes:
    benchmark   - Visualize only benchmark_results.csv
    comparison  - Visualize only comparison_results.csv
    all         - Visualize both (default)
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def load_data(csv_path):
    """Load benchmark data from CSV file."""
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found!")
        sys.exit(1)
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} benchmark results from {csv_path}")
    return df

def plot_by_graph_type(df):
    """Create a plot showing performance by graph type."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for graph_type in df['graph_type'].unique():
        data = df[df['graph_type'] == graph_type]
        ax.plot(data['vertices'], data['time_ms'], 
                marker='o', label=graph_type, linewidth=2)
    
    ax.set_xlabel('Number of Vertices', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('Euler Graph Algorithm Performance by Graph Type', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    return fig

def plot_time_vs_edges(df):
    """Create a plot showing time vs number of edges."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for graph_type in df['graph_type'].unique():
        data = df[df['graph_type'] == graph_type]
        ax.scatter(data['edges'], data['time_ms'], 
                  label=graph_type, alpha=0.6, s=100)
    
    ax.set_xlabel('Number of Edges', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('Execution Time vs Number of Edges', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    return fig

def plot_cpp_vs_python_time(df_comp):
    """Create a plot comparing C++ and Python execution times."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for graph_type in df_comp['graph_type'].unique():
        data = df_comp[df_comp['graph_type'] == graph_type]
        ax.plot(data['vertices'], data['python_time_ms'], 
                marker='o', label=f'{graph_type} (Python)', linewidth=2, linestyle='--', alpha=0.7)
        ax.plot(data['vertices'], data['cpp_time_ms'], 
                marker='s', label=f'{graph_type} (C++)', linewidth=2)
    
    ax.set_xlabel('Number of Vertices', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('C++ vs Python: Execution Time Comparison', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    return fig

def plot_speedup_by_graph_type(df_comp):
    """Create a plot showing speedup by graph type."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for graph_type in df_comp['graph_type'].unique():
        data = df_comp[df_comp['graph_type'] == graph_type]
        ax.plot(data['vertices'], data['speedup'], 
                marker='o', label=graph_type, linewidth=2)
    
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1, alpha=0.5, label='No speedup')
    
    ax.set_xlabel('Number of Vertices', fontsize=12)
    ax.set_ylabel('Speedup (Python time / C++ time)', fontsize=12)
    ax.set_title('C++ Speedup over Python by Graph Type', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    return fig

def plot_speedup_vs_edges(df_comp):
    """Create a plot showing speedup vs number of edges."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for graph_type in df_comp['graph_type'].unique():
        data = df_comp[df_comp['graph_type'] == graph_type]
        ax.scatter(data['edges'], data['speedup'], 
                  label=graph_type, alpha=0.6, s=100)
    
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1, alpha=0.5, label='No speedup')
    
    ax.set_xlabel('Number of Edges', fontsize=12)
    ax.set_ylabel('Speedup (Python time / C++ time)', fontsize=12)
    ax.set_title('C++ Speedup vs Number of Edges', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    return fig

def print_statistics(df):
    """Print summary statistics."""
    print("\n" + "="*60)
    print("BENCHMARK STATISTICS")
    print("="*60)
    
    print(f"\nTotal benchmarks run: {len(df)}")
    print(f"Graph types tested: {df['graph_type'].nunique()}")
    print(f"Vertex range: {df['vertices'].min()} - {df['vertices'].max()}")
    print(f"Edge range: {df['edges'].min()} - {df['edges'].max()}")
    
    print("\n--- Performance by Graph Type ---")
    stats = df.groupby('graph_type')['time_ms'].agg(['mean', 'min', 'max', 'std'])
    print(stats.to_string())
    
    print("\n--- Slowest 5 Benchmarks ---")
    slowest = df.nlargest(5, 'time_ms')[['test_name', 'graph_type', 'vertices', 'edges', 'time_ms']]
    print(slowest.to_string(index=False))
    
    print("\n--- Fastest 5 Benchmarks ---")
    fastest = df.nsmallest(5, 'time_ms')[['test_name', 'graph_type', 'vertices', 'edges', 'time_ms']]
    print(fastest.to_string(index=False))
    print("="*60 + "\n")

def print_comparison_statistics(df_comp):
    """Print comparison statistics."""
    print("\n" + "="*60)
    print("COMPARISON STATISTICS (C++ vs Python)")
    print("="*60)
    
    print(f"\nTotal comparison benchmarks: {len(df_comp)}")
    print(f"Graph types tested: {df_comp['graph_type'].nunique()}")
    
    valid_speedups = df_comp[df_comp['speedup'].notna() & (df_comp['speedup'] > 0)]
    
    if len(valid_speedups) > 0:
        print(f"\n--- Overall Speedup Statistics ---")
        print(f"Average speedup: {valid_speedups['speedup'].mean():.2f}x")
        print(f"Median speedup: {valid_speedups['speedup'].median():.2f}x")
        print(f"Min speedup: {valid_speedups['speedup'].min():.2f}x")
        print(f"Max speedup: {valid_speedups['speedup'].max():.2f}x")
        
        print("\n--- Speedup by Graph Type ---")
        speedup_stats = valid_speedups.groupby('graph_type')['speedup'].agg(['mean', 'min', 'max'])
        print(speedup_stats.to_string())
        
        print("\n--- Top 5 Speedups ---")
        top_speedups = valid_speedups.nlargest(5, 'speedup')[['test_name', 'graph_type', 'vertices', 'speedup']]
        print(top_speedups.to_string(index=False))
        
        print("\n--- Cases where Python was faster (speedup < 1) ---")
        python_faster = valid_speedups[valid_speedups['speedup'] < 1]
        if len(python_faster) > 0:
            print(python_faster[['test_name', 'graph_type', 'vertices', 'speedup']].to_string(index=False))
        else:
            print("None - C++ was faster in all cases!")
    
    print("="*60 + "\n")

def visualize_benchmarks(output_dir='results'):
    """Visualize benchmark results."""
    csv_path = os.path.join(output_dir, 'benchmark_results.csv')
    
    if not os.path.exists(csv_path):
        print(f"Benchmark file not found: {csv_path}")
        return
    
    df = load_data(csv_path)
    print_statistics(df)
    
    print("Generating benchmark plots...")
    
    fig1 = plot_by_graph_type(df)
    output_path1 = os.path.join(output_dir, 'benchmark_by_type.png')
    fig1.savefig(output_path1, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path1}")
    plt.close(fig1)
    
    fig2 = plot_time_vs_edges(df)
    output_path2 = os.path.join(output_dir, 'benchmark_time_vs_edges.png')
    fig2.savefig(output_path2, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path2}")
    plt.close(fig2)

def visualize_comparison(output_dir='results'):
    """Visualize comparison results."""
    csv_path = os.path.join(output_dir, 'comparison_results.csv')
    
    if not os.path.exists(csv_path):
        print(f"Comparison file not found: {csv_path}")
        return
    
    df_comp = load_data(csv_path)
    print_comparison_statistics(df_comp)
    
    print("Generating comparison plots...")
    
    fig1 = plot_cpp_vs_python_time(df_comp)
    output_path1 = os.path.join(output_dir, 'comparison_cpp_vs_python.png')
    fig1.savefig(output_path1, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path1}")
    plt.close(fig1)
    
    fig2 = plot_speedup_by_graph_type(df_comp)
    output_path2 = os.path.join(output_dir, 'comparison_speedup_by_type.png')
    fig2.savefig(output_path2, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path2}")
    plt.close(fig2)
    
    fig3 = plot_speedup_vs_edges(df_comp)
    output_path3 = os.path.join(output_dir, 'comparison_speedup_vs_edges.png')
    fig3.savefig(output_path3, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path3}")
    plt.close(fig3)

def main():
    mode = 'all'
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    output_dir = 'results'
    
    if mode not in ['benchmark', 'comparison', 'all']:
        print(f"Unknown mode: {mode}")
        print("Usage: python3 visualize_benchmark.py [benchmark|comparison|all]")
        sys.exit(1)
    
    if mode in ['benchmark', 'all']:
        visualize_benchmarks(output_dir)
    
    if mode in ['comparison', 'all']:
        visualize_comparison(output_dir)
    
    print("\nVisualization complete!")

if __name__ == '__main__':
    main()
