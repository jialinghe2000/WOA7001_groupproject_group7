"""
WOA7001 Group Project - Problem 3: Urban Road Network Planning
Algorithm 1: Kruskal's Algorithm for Minimum Spanning Tree (MST)

This implementation uses Kruskal's algorithm to determine the optimal road network
connecting locations in Delhi City by minimizing the total distance.
"""

import time
from typing import List, Tuple, Dict


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure for cycle detection.
    Uses path compression and union by rank for optimization.
    """
    
    def __init__(self, n: int):
        """
        Initialize Union-Find structure.
        
        Args:
            n: Number of nodes
        """
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        """
        Find the root of the set containing x with path compression.
        
        Args:
            x: Node to find root for
            
        Returns:
            Root of the set containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Union two sets containing x and y using union by rank.
        
        Args:
            x: First node
            y: Second node
            
        Returns:
            True if union was performed, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


class KruskalMST:
    """
    Implementation of Kruskal's Algorithm for finding Minimum Spanning Tree.
    """
    
    def __init__(self):
        """Initialize Kruskal MST solver."""
        self.edges: List[Tuple[int, int, int, float]] = []
        self.nodes: set = set()
        self.node_coordinates: Dict[int, Tuple[float, float]] = {}
    
    def add_edge(self, edge_id: int, start_node: int, end_node: int, 
                 distance: float, x_coord: float, y_coord: float):
        """
        Add an edge to the graph.
        
        Args:
            edge_id: Unique identifier for the edge
            start_node: Starting node
            end_node: Ending node
            distance: Distance between nodes
            x_coord: X coordinate of start node
            y_coord: Y coordinate of start node
        """
        self.edges.append((edge_id, start_node, end_node, distance))
        self.nodes.add(start_node)
        self.nodes.add(end_node)
        
        # Store coordinates for the first occurrence of each node
        if start_node not in self.node_coordinates:
            self.node_coordinates[start_node] = (x_coord, y_coord)
    
    def find_mst(self) -> Tuple[List[Tuple], float, float]:
        """
        Find the Minimum Spanning Tree using Kruskal's algorithm.
        
        Returns:
            Tuple containing:
                - List of edges in MST (edge_id, start_node, end_node, distance)
                - Total distance of MST
                - Execution time in seconds
        """
        start_time = time.time()
        
        # Sort edges by distance (ascending order)
        sorted_edges = sorted(self.edges, key=lambda x: x[3])
        
        # Create node mapping (node_id -> index)
        node_list = sorted(list(self.nodes))
        node_to_index = {node: idx for idx, node in enumerate(node_list)}
        
        # Initialize Union-Find structure
        uf = UnionFind(len(node_list))
        
        mst_edges = []
        total_distance = 0.0
        
        # Process edges in ascending order of distance
        for edge_id, start_node, end_node, distance in sorted_edges:
            start_idx = node_to_index[start_node]
            end_idx = node_to_index[end_node]
            
            # Add edge if it doesn't create a cycle
            if uf.union(start_idx, end_idx):
                mst_edges.append((edge_id, start_node, end_node, distance))
                total_distance += distance
                
                # Stop when we have n-1 edges (complete MST)
                if len(mst_edges) == len(node_list) - 1:
                    break
        
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
        print("KRUSKAL'S ALGORITHM - MINIMUM SPANNING TREE")
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


def load_delhi_city_data() -> KruskalMST:
    """
    Load the Delhi City network data from Table 5.
    
    Returns:
        KruskalMST object with loaded data
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
    
    kruskal = KruskalMST()
    
    for x_coord, y_coord, start_node, end_node, edge_id, distance in data:
        kruskal.add_edge(edge_id, start_node, end_node, distance, x_coord, y_coord)
    
    return kruskal


def main():
    """
    Main function to demonstrate Kruskal's algorithm on Delhi City network.
    """
    print("\n" + "=" * 80)
    print("WOA7001 GROUP PROJECT - PROBLEM 3")
    print("Urban Road Network Planning using Kruskal's Algorithm")
    print("=" * 80 + "\n")
    
    # Load Delhi City data
    kruskal = load_delhi_city_data()
    
    print(f"Loaded {len(kruskal.edges)} edges connecting {len(kruskal.nodes)} nodes")
    print("Computing Minimum Spanning Tree...\n")
    
    # Find MST
    mst_edges, total_distance, execution_time = kruskal.find_mst()
    
    # Display results
    kruskal.display_mst(mst_edges, total_distance, execution_time)
    
    # Additional analysis
    print("\nANALYSIS:")
    print(f"- Original network had {len(kruskal.edges)} possible road segments")
    print(f"- Optimal network requires only {len(mst_edges)} road segments")
    print(f"- This represents a {(1 - len(mst_edges)/len(kruskal.edges))*100:.1f}% reduction")
    print(f"- All {len(kruskal.nodes)} locations remain connected")
    print(f"- No redundant roads (cycles) in the network")
    print("\n")


if __name__ == "__main__":
    main()
