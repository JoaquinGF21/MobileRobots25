import time
import os
import heapq

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        # Walls in each direction (North, West, East, South)
        # True means there is a wall, False means there is no wall
        self.walls = {'N': True, 'W': True, 'E': True, 'S': True}
        # For Dijkstra's algorithm, we'll need these properties
        self.distance = float('inf')
        self.visited = False
        self.previous = None
        
    def __repr__(self):
        return f"Cell({self.row}, {self.col})"
        
class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # Create the grid of cells
        self.grid = [[Cell(i, j) for j in range(width)] for i in range(height)]
        # Graph representation as adjacency list
        self.graph = {}
        
    def remove_wall(self, row, col, direction):
        # Remove a wall between two cells
        if direction not in ['N', 'W', 'E', 'S']:
            raise ValueError("Direction must be 'N', 'W', 'E', or 'S'")
            
        # Remove the wall from the current cell
        self.grid[row][col].walls[direction] = False
        
        # Remove the opposite wall from the adjacent cell
        if direction == 'N' and row > 0:
            self.grid[row-1][col].walls['S'] = False
        elif direction == 'S' and row < self.height - 1:
            self.grid[row+1][col].walls['N'] = False
        elif direction == 'E' and col < self.width - 1:
            self.grid[row][col+1].walls['W'] = False
        elif direction == 'W' and col > 0:
            self.grid[row][col-1].walls['E'] = False
            
    def build_graph(self):
        # Convert the maze into a graph (adjacency list)
        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row][col]
                self.graph[(row, col)] = []
                
                # Check all four directions
                # North
                if not cell.walls['N'] and row > 0:
                    self.graph[(row, col)].append((row-1, col))
                # South
                if not cell.walls['S'] and row < self.height - 1:
                    self.graph[(row, col)].append((row+1, col))
                # East
                if not cell.walls['E'] and col < self.width - 1:
                    self.graph[(row, col)].append((row, col+1))
                # West
                if not cell.walls['W'] and col > 0:
                    self.graph[(row, col)].append((row, col-1))
    
    def print_maze(self, current_pos=None, visited=None, frontier=None, path=None):
        """
        Print the maze in the console with various markers and larger cells:
        - 🤖: Current position
        - 📍: Visited cells
        - ⭐: Cells in frontier (next to consider)
        - 🚩: Final path
        """
        # Convert None to empty sets for easier checking
        if visited is None:
            visited = set()
        if frontier is None:
            frontier = set()
        if path is None:
            path = set()
            
        # Clear the console for animation effect
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Cell width (adjust for larger cells)
        cell_width = 3
        
        # Print the top border
        print(' ' + '_' * (self.width * (cell_width + 1) - 1))
        
        for row in range(self.height):
            # First line of the cell row (contains North walls and cell content)
            print('|', end='')
            
            for col in range(self.width):
                # Choose symbol for cell based on priorities
                cell_symbol = ' ' * cell_width
                if (row, col) == current_pos:
                    # Center the emoji in the cell
                    cell_symbol = ' 🤖 '
                elif (row, col) in path:
                    cell_symbol = ' 🚩 '
                elif (row, col) in frontier:
                    cell_symbol = ' ⭐ '
                elif (row, col) in visited:
                    cell_symbol = ' 📍 '
                
                # Print south wall (if present)
                if self.grid[row][col].walls['S']:
                    print(f'{cell_symbol}', end='')
                    print('_' * cell_width, end='')
                else:
                    print(f'{cell_symbol}', end='')
                    print(' ' * cell_width, end='')
                
                # Print east wall (if present and not at the east edge)
                if col < self.width - 1:
                    if self.grid[row][col].walls['E']:
                        print('|', end='')
                    else:
                        print(' ', end='')
                else:
                    print('|', end='')  # East border
            
            print()  # New line at the end of the row
        
        # Print legend
        print("\nLegend:")
        print("🤖 = Current position")
        print("📍 = Visited cell")
        print("⭐ = Frontier cell (to be visited)")
        print("🚩 = Final path")
    
    def dijkstra_visualized(self, start_pos, end_pos, delay=0.5):
        """
        Run Dijkstra's algorithm with visualization at each step
        """
        # Reset all cells
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].distance = float('inf')
                self.grid[row][col].visited = False
                self.grid[row][col].previous = None
                
        # Set the start cell's distance to 0
        start_row, start_col = start_pos
        self.grid[start_row][start_col].distance = 0
        
        # Priority queue for Dijkstra's algorithm
        queue = [(0, start_pos)]
        
        # Keep track of visited cells and the frontier
        visited = set()
        
        print("\nStarting Dijkstra's algorithm...")
        time.sleep(1)
        
        while queue:
            current_distance, current_pos = heapq.heappop(queue)
            current_row, current_col = current_pos
            
            # Skip if already visited
            if current_pos in visited:
                continue
                
            # Mark as visited
            visited.add(current_pos)
            self.grid[current_row][current_col].visited = True
            
            # Get the current frontier (cells in the queue)
            frontier = set([pos for _, pos in queue])
            
            # Visualize the current state
            self.print_maze(current_pos, visited, frontier)
            print(f"\nCurrent position: {current_pos}")
            print(f"Distance from start: {current_distance}")
            
            # If we've reached the end, we're done
            if current_pos == end_pos:
                print("\nReached the destination!")
                time.sleep(delay)
                break
            
            # Check all neighbors
            for neighbor_pos in self.graph[current_pos]:
                neighbor_row, neighbor_col = neighbor_pos
                
                # The weight is 1 for all connections in a simple maze
                weight = 1
                
                # Calculate new distance
                new_distance = current_distance + weight
                
                # If we've found a shorter path, update it
                if new_distance < self.grid[neighbor_row][neighbor_col].distance:
                    self.grid[neighbor_row][neighbor_col].distance = new_distance
                    self.grid[neighbor_row][neighbor_col].previous = current_pos
                    heapq.heappush(queue, (new_distance, neighbor_pos))
            
            time.sleep(delay)  # Pause to see the visualization
        
        # Reconstruct the path
        path = []
        current = end_pos
        while current != start_pos:
            path.append(current)
            current_row, current_col = current
            current = self.grid[current_row][current_col].previous
            if current is None:
                print("\nNo path exists!")
                return None  # No path exists
        path.append(start_pos)
        path.reverse()
        
        # Visualize the final path
        print("\nFinal path found!")
        self.print_maze(None, visited, None, set(path))
        print(f"\nPath from {start_pos} to {end_pos}:")
        for i, pos in enumerate(path):
            if i < len(path) - 1:
                print(pos, end=" → ")
            else:
                print(pos)
        print(f"Total distance: {self.grid[end_pos[0]][end_pos[1]].distance}")
        
        return path


def create_sample_maze():
    """
    Create a sample 5x5 maze with a specific path from (0,0) to (4,4)
    """
    maze = Maze(5, 5)
    
    # Create a winding path from top-left to bottom-right
    # Starting from (0,0), remove walls to create a path
    
    # Row 0: move right
    maze.remove_wall(0, 0, 'E')
    maze.remove_wall(0, 1, 'E')
    maze.remove_wall(0, 2, 'S')
    
    # Row 1: move down then right
    maze.remove_wall(1, 2, 'E')
    maze.remove_wall(1, 3, 'S')
    
    # Row 2: move down then left
    maze.remove_wall(2, 3, 'W')
    maze.remove_wall(2, 2, 'W')
    maze.remove_wall(2, 1, 'S')
    
    # Row 3: move right then down
    maze.remove_wall(3, 1, 'E')
    maze.remove_wall(3, 2, 'E')
    maze.remove_wall(3, 3, 'E')
    maze.remove_wall(3, 4, 'S')
    
    # Add some additional paths to make it more interesting
    # These create loops/alternative paths
    maze.remove_wall(1, 0, 'S')
    maze.remove_wall(2, 0, 'E')
    maze.remove_wall(0, 4, 'S')
    maze.remove_wall(1, 4, 'S')
    
    # Build the graph based on the walls we've removed
    maze.build_graph()
    
    return maze


def main():
    # Create our sample maze
    maze = create_sample_maze()
    
    # Print the initial maze
    print("Original Maze:")
    maze.print_maze()
    time.sleep(2)  # Give time to see the initial maze
    
    # Find the shortest path from top-left to bottom-right
    start_pos = (0, 0)
    end_pos = (4, 4)
    
    # Run Dijkstra's algorithm with visualization
    path = maze.dijkstra_visualized(start_pos, end_pos, delay=0.8)
    
    # Wait for user to press Enter before exiting
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()