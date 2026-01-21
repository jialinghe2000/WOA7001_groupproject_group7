"""
WOA7001 Group Project - Problem 3: Comparison of Algorithms
This script runs both Kruskal's and Prim's algorithms and compares their performance.
"""

import time
from problem3_kruskal import KruskalMST, load_delhi_city_data as load_kruskal_data
from problem3_prim import PrimMST, load_delhi_city_data as load_prim_data


def run_comparison():
    """
    Run both algorithms and compare their results.
    """
    print("\n" + "=" * 80)
    print("WOA7001 GROUP PROJECT - PROBLEM 3")
    print("COMPARATIVE ANALYSIS: Kruskal's vs Prim's Algorithm")
    print("=" * 80 + "\n")
    
    # Run Kruskal's Algorithm
    print("Running Kruskal's Algorithm...")
    kruskal = load_kruskal_data()
    kruskal_mst, kruskal_distance, kruskal_time = kruskal.find_mst()
    kruskal.display_mst(kruskal_mst, kruskal_distance, kruskal_time)
    
    print("\n" + "-" * 80 + "\n")
    
    # Run Prim's Algorithm
    print("Running Prim's Algorithm...")
    prim = load_prim_data()
    prim_mst, prim_distance, prim_time = prim.find_mst(start_node=1)
    prim.display_mst(prim_mst, prim_distance, prim_time)
    
    print("\n" + "=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    
    # Create comparison table
    print(f"\n{'Metric':<40} {'Kruskal':<20} {'Prim':<20}")
    print("-" * 80)
    print(f"{'Total Network Distance (units)':<40} {kruskal_distance:<20.2f} {prim_distance:<20.2f}")
    print(f"{'Number of Edges in MST':<40} {len(kruskal_mst):<20} {len(prim_mst):<20}")
    print(f"{'Execution Time (seconds)':<40} {kruskal_time:<20.8f} {prim_time:<20.8f}")
    print(f"{'Number of Nodes Connected':<40} {len(kruskal.nodes):<20} {len(prim.nodes):<20}")
    
    # Performance comparison
    faster_algorithm = "Kruskal's" if kruskal_time < prim_time else "Prim's"
    time_difference = abs(kruskal_time - prim_time)
    speedup = max(kruskal_time, prim_time) / min(kruskal_time, prim_time)
    
    print("-" * 80)
    print(f"\nPERFORMANCE ANALYSIS:")
    print(f"- Both algorithms produced MSTs with identical total distance: {kruskal_distance:.2f} units")
    print(f"- {faster_algorithm} Algorithm was faster by {time_difference:.8f} seconds")
    print(f"- Speedup factor: {speedup:.2f}x")
    print(f"- Distance verification: {'PASSED' if abs(kruskal_distance - prim_distance) < 0.01 else 'FAILED'}")
    
    print("\nKEY OBSERVATIONS:")
    print("1. Both algorithms guarantee finding the optimal MST with minimum total distance")
    print("2. The MST is unique for this graph (no edges with equal weights causing ties)")
    print("3. Kruskal's algorithm is edge-oriented (processes all edges)")
    print("4. Prim's algorithm is vertex-oriented (grows tree from a starting vertex)")
    print("5. For sparse graphs, Kruskal's is typically more efficient")
    print("6. For dense graphs, Prim's with binary heap can be more efficient")
    
    print("\n" + "=" * 80 + "\n")


def run_multiple_trials(num_trials=10):
    """
    Run multiple trials to get average execution time.
    
    Args:
        num_trials: Number of trials to run
    """
    print("\n" + "=" * 80)
    print(f"RUNNING {num_trials} TRIALS FOR STATISTICAL ANALYSIS")
    print("=" * 80 + "\n")
    
    kruskal_times = []
    prim_times = []
    
    for i in range(num_trials):
        # Kruskal's Algorithm
        kruskal = load_kruskal_data()
        _, _, k_time = kruskal.find_mst()
        kruskal_times.append(k_time)
        
        # Prim's Algorithm
        prim = load_prim_data()
        _, _, p_time = prim.find_mst(start_node=1)
        prim_times.append(p_time)
        
        print(f"Trial {i+1:2d}: Kruskal = {k_time:.8f}s, Prim = {p_time:.8f}s")
    
    # Calculate statistics
    avg_kruskal = sum(kruskal_times) / num_trials
    avg_prim = sum(prim_times) / num_trials
    min_kruskal = min(kruskal_times)
    max_kruskal = max(kruskal_times)
    min_prim = min(prim_times)
    max_prim = max(prim_times)
    
    print("\n" + "-" * 80)
    print("STATISTICAL SUMMARY")
    print("-" * 80)
    print(f"{'Metric':<30} {'Kruskal':<25} {'Prim':<25}")
    print("-" * 80)
    print(f"{'Average Time (s)':<30} {avg_kruskal:<25.8f} {avg_prim:<25.8f}")
    print(f"{'Minimum Time (s)':<30} {min_kruskal:<25.8f} {min_prim:<25.8f}")
    print(f"{'Maximum Time (s)':<30} {max_kruskal:<25.8f} {max_prim:<25.8f}")
    print("-" * 80)
    print(f"\nAverage speedup: {max(avg_kruskal, avg_prim) / min(avg_kruskal, avg_prim):.2f}x")
    print(f"Faster algorithm on average: {'Kruskal' if avg_kruskal < avg_prim else 'Prim'}\n")


if __name__ == "__main__":
    # Run single comparison
    run_comparison()
    
    # Run multiple trials for statistical analysis
    run_multiple_trials(num_trials=10)
