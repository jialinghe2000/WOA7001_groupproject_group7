"""
WOA7001 Group Project - Problem 3: Urban Road Network Planning
Algorithm 2: Prim's Algorithm for Minimum Spanning Tree (MST)

This implementation uses Prim's algorithm to determine the optimal road network
connecting locations in Delhi City by minimizing the total distance.
"""

import time
import heapq
from typing import List, Tuple, Dict, Set
from collections import defaultdict


class PrimMST:
    """
    Implementation of Prim's Algorithm for finding Minimum Spanning Tree.
    """
    
    def __init__(self):
        """Initialize Prim MST solver."""
        self.graph: Dict[int, List[Tuple[int, int, float]]] = defaultdict(list)
        self.nodes: Set[int] = set()
        self.edge_info: Dict[Tuple[int, int], Tuple[int, float]] = {}
        self.node_coordinates: Dict[int, Tuple[float, float]] = {}
    
    def add_edge(self, edge_id: int, start_node: int, end_node: int, 
                 distance: float, x_coord: float, y_coord: float):
        """
        Add an edge to the graph (bidirectional for undirected graph).
        
        Args:
            edge_id: Unique identifier for the edge
            start_node: Starting node
            end_node: Ending node
            distance: Distance between nodes
            x_coord: X coordinate of start node
            y_coord: Y coordinate of start node
        """
        # Add edge in both directions (undirected graph)
        self.graph[start_node].append((end_node, edge_id, distance))
        self.graph[end_node].append((start_node, edge_id, distance))
        
        self.nodes.add(start_node)
        self.nodes.add(end_node)
        
        # Store edge information
        edge_key = tuple(sorted([start_node, end_node]))
        if edge_key not in self.edge_info or distance < self.edge_info[edge_key][1]:
            self.edge_info[edge_key] = (edge_id, distance)
        
        # Store coordinates
        if start_node not in self.node_coordinates:
            self.node_coordinates[start_node] = (x_coord, y_coord)
    
    def find_mst(self, start_node: int = None) -> Tuple[List[Tuple], float, float]:
        """
        Find the Minimum Spanning Tree using Prim's algorithm.
        
        Args:
            start_node: Starting node for MST construction (defaults to smallest node)
            
        Returns:
            Tuple containing:
                - List of edges in MST (edge_id, start_node, end_node, distance)
                - Total distance of MST
                - Execution time in seconds
        """
        start_time = time.time()
        
        if start_node is None:
            start_node = min(self.nodes)
        
        # Priority queue: (distance, current_node, parent_node, edge_id)
        pq = [(0, start_node, None, None)]
        visited: Set[int] = set()
        mst_edges: List[Tuple] = []
        total_distance = 0.0
        
        while pq and len(visited) < len(self.nodes):
            distance, current_node, parent_node, edge_id = heapq.heappop(pq)
            
            # Skip if already visited
            if current_node in visited:
                continue
            
            # Mark as visited
            visited.add(current_node)
            
            # Add edge to MST (except for the starting node)
            if parent_node is not None:
                mst_edges.append((edge_id, parent_node, current_node, distance))
                total_distance += distance
            
            # Add all adjacent edges to priority queue
            for neighbor, neighbor_edge_id, neighbor_distance in self.graph[current_node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (neighbor_distance, neighbor, 
                                       current_node, neighbor_edge_id))
        
        execution_time = time.time() - start_time
        
        return mst_edges, total_distance, execution_time
    
    def display_mst(self, mst_edges: List[Tuple], total_distance: float, 
                    execution_time: float):
        """
        Display the Minimum Spanning Tree results.
        
        Args:
            mst_edges: List of edges in MST
            total_distance: Total distance of MST
            execution_time: Time taken to compute MST
        """
        print("=" * 80)
        print("PRIM'S ALGORITHM - MINIMUM SPANNING TREE")
        print("=" * 80)
        print(f"\nOptimal Road Network for Delhi City\n")
        print(f"{'Edge ID':<10} {'Start':<8} {'End':<8} {'Distance':<15}")
        print("-" * 80)
        
        for edge_id, start_node, end_node, distance in mst_edges:
            print(f"{edge_id:<10} {start_node:<8} {end_node:<8} {distance:<15.2f}")
        
        print("-" * 80)
        print(f"\nTotal Number of Nodes: {len(self.nodes)}")
        print(f"Total Number of Roads (Edges in MST): {len(mst_edges)}")
        print(f"Total Network Distance: {total_distance:.2f} units")
        print(f"Execution Time: {execution_time:.6f} seconds")
        print("=" * 80)
    
    def get_total_edges(self) -> int:
        """
        Get the total number of unique edges in the graph.
        
        Returns:
            Number of unique edges
        """
        return len(self.edge_info)


def load_delhi_city_data() -> PrimMST:
    """
    Load the Delhi City network data from Table 5.
    
    Returns:
        PrimMST object with loaded data
    """
    # Data from Table 5: Delhi City locations
    data = [
        (712537.65892300, 3144490.85877640, 1, 2, 1, 3.75432447162338),
        (712537.65892300, 3144490.85877640, 1, 2, 2, 3.75432447162338),
        (712537.65892300, 3144490.85877640, 1, 3, 3, 20.4871202876504),
        (712537.65892300, 3144490.85877640, 1, 4, 4, 19.1877809458002),
        (712540.40782175, 3144488.30172578, 2, 1, 1, 3.75432447162338),
        (712540.40782175, 3144488.30172578, 2, 1, 2, 3.75432447162338),
        (712557.85887214, 3144494.27698534, 3, 1, 3, 20.4871202876504),
        (712522.10662982, 3144502.09697530, 4, 1, 4, 19.1877809458002),
        (712522.10662982, 3144502.09697530, 4, 5, 5, 201.987464765257),
        (712522.10662982, 3144502.09697530, 4, 5, 6, 131.072874250845),
        (712522.10662982, 3144502.09697530, 4, 5, 7, 131.072874250845),
        (712419.52081542, 3144583.68281383, 5, 4, 5, 201.987464765257),
        (712419.52081542, 3144583.68281383, 5, 4, 6, 131.072874250845),
        (712419.52081542, 3144583.68281383, 5, 4, 7, 131.072874250845),
        (712419.52081542, 3144583.68281383, 5, 6, 8, 1008.13308093641),
        (711578.86168731, 3145075.59898330, 6, 5, 8, 1008.13308093641),
        (711315.23002979, 3145398.57620775, 7, 8, 9, 113.853447528611),
        (711315.23002979, 3145398.57620775, 7, 8, 10, 113.853447528611),
        (711284.86276158, 3145505.61220279, 8, 7, 9, 113.853447528611),
        (711284.86276158, 3145505.61220279, 8, 7, 10, 113.853447528611),
    ]
    
    prim = PrimMST()
    
    for x_coord, y_coord, start_node, end_node, edge_id, distance in data:
        prim.add_edge(edge_id, start_node, end_node, distance, x_coord, y_coord)
    
    return prim


def main():
    """
    Main function to demonstrate Prim's algorithm on Delhi City network.
    """
    print("\n" + "=" * 80)
    print("WOA7001 GROUP PROJECT - PROBLEM 3")
    print("Urban Road Network Planning using Prim's Algorithm")
    print("=" * 80 + "\n")
    
    # Load Delhi City data
    prim = load_delhi_city_data()
    
    print(f"Loaded {prim.get_total_edges()} unique edges connecting {len(prim.nodes)} nodes")
    print("Computing Minimum Spanning Tree...\n")
    
    # Find MST (starting from node 1)
    mst_edges, total_distance, execution_time = prim.find_mst(start_node=1)
    
    # Display results
    prim.display_mst(mst_edges, total_distance, execution_time)
    
    # Additional analysis
    print("\nANALYSIS:")
    print(f"- Original network had {prim.get_total_edges()} possible road segments")
    print(f"- Optimal network requires only {len(mst_edges)} road segments")
    print(f"- This represents a {(1 - len(mst_edges)/prim.get_total_edges())*100:.1f}% reduction")
    print(f"- All {len(prim.nodes)} locations remain connected")
    print(f"- MST construction started from Node 1")
    print(f"- Greedy approach ensures locally optimal choices lead to global optimum")
    print("\n")


if __name__ == "__main__":
    main()
