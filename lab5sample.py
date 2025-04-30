from motion import Movement
from robot_systems.robot import HamBot
import math
import time

Chris_R = HamBot()
time.sleep(2)
Movement = Movement()
import heapq

def dijkstra_path_directions(adjacency_list, start, end):
    """
    Finds the shortest path between start and end using Dijkstra's algorithm
    and returns directions to move between cells.
    
    Parameters:
    adjacency_list: dict - where adjacency_list[node] gives neighbors of node
    start: int - starting position (0-8)
    end: int - ending position (0-8)
    
    Returns:
    A list of directions ('N', 'S', 'E', 'W') to follow
    """
    # Initialize distances and previous nodes
    distances = {node: float('inf') for node in adjacency_list}
    distances[start] = 0
    previous = {node: None for node in adjacency_list}
    
    # Priority queue
    queue = [(0, start)]
    visited = set()
    
    # Dijkstra's algorithm
    while queue:
        current_distance, current = heapq.heappop(queue)
        
        # If we've reached the end, we're done
        if current == end:
            break
            
        # Skip if already visited
        if current in visited:
            continue
            
        # Mark as visited
        visited.add(current)
        
        # Check all neighbors
        for neighbor in adjacency_list[current]:
            # Weight is 1 for all connections in a simple maze
            new_distance = current_distance + 1
            
            # If we've found a shorter path, update it
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))
    
    # If we couldn't reach the end
    if previous[end] is None:
        return None
    
    # Reconstruct the path (cell positions)
    cell_path = []
    current = end
    
    while current != start:
        cell_path.append(current)
        current = previous[current]
    
    cell_path.append(start)
    cell_path.reverse()
    
    # Convert cell path to directions
    directions = []
    for i in range(len(cell_path) - 1):
        current_cell = cell_path[i]
        next_cell = cell_path[i + 1]
        
        # Convert 1D index to 2D position
        current_row, current_col = current_cell // 3, current_cell % 3
        next_row, next_col = next_cell // 3, next_cell % 3
        
        # Determine direction
        if next_row > current_row:   # Moving South
            directions.append('S')
        elif next_row < current_row: # Moving North
            directions.append('N')
        elif next_col > current_col: # Moving East
            directions.append('E')
        elif next_col < current_col: # Moving West
            directions.append('W')
    
    return directions


# Example usage with the discovered maze
def test_discovered_maze():
    # This is what your partner's discovery code would provide
    # Using grid numbering:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    adjacency_list = {
        0: [1, 3],        # Top-left can go right or down
        1: [0, 4],     # Top-middle 
        2: [5],           # Top-right
        3: [0, 6],        # Middle-left
        4: [1, 5],  # Middle-center
        5: [2, 8],        # Middle-right
        6: [3, 7],           # Bottom-left
        7: [6, 8],     # Bottom-middle
        8: [5 ,7]         # Bottom-right
    }
    
    # Find path from start to end
    start = 0  # Top-left
    end = 8    # Bottom-right
    
    directions = dijkstra_path_directions(adjacency_list, start, end)
    
    if directions:
        print(f"Directions from {start} to {end}:")
        print(" → ".join(directions))
        print(f"Number of steps: {len(directions)}")
    else:
        print(f"No path exists from {start} to {end}")

    # Let's try another example with different start/end
    start2 = 2  # Top-right
    end2 = 6    # Bottom-left
    
    directions2 = dijkstra_path_directions(adjacency_list, start2, end2)
    
    if directions2:
        print(f"\nDirections from {start2} to {end2}:")
        print(" → ".join(directions2))
        print(f"Number of steps: {len(directions2)}")
    else:
        print(f"\nNo path exists from {start2} to {end2}")


if __name__ == "__main__":
    test_discovered_maze()