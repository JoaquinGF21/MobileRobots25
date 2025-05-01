import heapq
from motion import Movement, Chris_R
import pickle

def dijkstra_path_directions(adjacency_list, start, end):
    """
    Finds the shortest path between start and end using Dijkstra's algorithm
    and returns directions to move between cells.
    
    Parameters:
    adjacency_list: dict - where adjacency_list[node] gives a list of (neighbor, weight) tuples
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
        for neighbor, weight in adjacency_list[current]:
            # Use the weight from the adjacency list
            new_distance = current_distance + weight
            
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
        
        # Convert 1D index to 2D position (assuming 3x3 grid)
        current_row, current_col = divmod(current_cell, 3)
        next_row, next_col = divmod(next_cell, 3)
        
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


def test_path(adjacency_list, start, end):
    """
    Test function to visualize path without moving the robot.
    Prints the direction list and visualizes the maze path.
    
    Parameters:
    adjacency_list: dict - The maze structure with weights
    start: int - Starting position (0-8)
    end: int - Ending position (0-8)
    """
    directions = dijkstra_path_directions(adjacency_list, start, end)
    
    if directions:
        print("\n=== PATH TEST ===")
        print(f"Start position: {start}")
        print(f"End position: {end}")
        print(f"Direction list: {directions}")
        print(f"Path: {' → '.join(directions)}")
        print(f"Number of steps: {len(directions)}")
        
        # Visualize the maze (3x3 grid)
        grid = [['□' for _ in range(3)] for _ in range(3)]
        
        # Mark the start position
        start_row, start_col = divmod(start, 3)
        grid[start_row][start_col] = 'S'
        
        # Mark the end position
        end_row, end_col = divmod(end, 3)
        grid[end_row][end_col] = 'E'
        
        # Reconstruct the path for visualization
        current_pos = start
        for direction in directions:
            current_row, current_col = divmod(current_pos, 3)
            
            # Move to next position
            if direction == 'N':
                current_row -= 1
            elif direction == 'S':
                current_row += 1
            elif direction == 'E':
                current_col += 1
            elif direction == 'W':
                current_col -= 1
                
            current_pos = current_row * 3 + current_col
            
            # Mark the path (but don't overwrite start or end)
            if grid[current_row][current_col] not in ['S', 'E']:
                grid[current_row][current_col] = '■'
        
        # Print the maze visualization
        print("\nMaze path visualization:")
        print("  0 1 2")
        for i, row in enumerate(grid):
            print(f"{i} {' '.join(row)}")
            
        print("\nReady to execute this path! Run navigate_maze() to move the robot.")
    else:
        print(f"No path exists from {start} to {end}")


def navigate_maze(adjacency_list, start, end):
    """
    Calculates the path and directly controls the robot to navigate from start to end.
    
    Parameters:
    adjacency_list: dict - The maze structure
    start: int - Starting position (0-8)
    end: int - Ending position (0-8)
    
    Returns:
    True if navigation was successful, False otherwise
    """
    directions = dijkstra_path_directions(adjacency_list, start, end)
    
    if directions:
        print(f"Path found from {start} to {end}:")
        print(" → ".join(directions))
        print(f"Number of steps: {len(directions)}")
        
        # Execute movement along the path
        Movement.follow_path(directions)
        return True
    else:
        print(f"No path exists from {start} to {end}")
        return False

def readPickle(pickle_file):
    with open(pickle_file, 'rb') as f:
        # Use pickle.load to deserialize the adjacency list
        adjacency_list = pickle.load(f)
    return adjacency_list
    
def get_user_input():
    """
    Gets the start and end positions from the user.
    
    Returns:
    start, end - tuple of integers representing start and end positions
    """
    print("\n=== MAZE NAVIGATION ===")
    print("The maze is a 3x3 grid numbered 0-8 as follows:")
    print("  0 1 2")
    print("  3 4 5")
    print("  6 7 8")
    
    while True:
        try:
            start = int(input("\nEnter the starting position (0-8): "))
            if not 0 <= start <= 8:
                print("Invalid position. Please enter a number between 0 and 8.")
                continue
                
            end = int(input("Enter the destination position (0-8): "))
            if not 0 <= end <= 8:
                print("Invalid position. Please enter a number between 0 and 8.")
                continue
                
            return start, end
        except ValueError:
            print("Invalid input. Please enter integers.")

def main():
    # Load the adjacency list from the pickle file
    try:
        pickle_file = "MazeFile.pkl"
        print(f"Loading maze data from {pickle_file}...")
        adjacency_list = readPickle(pickle_file)
        print("Maze loaded successfully!")
        
        # Display adjacency list structure (optional)
        print("\nMaze structure:")
        for node, neighbors in adjacency_list.items():
            print(f"Node {node}: {neighbors}")
        
        # Get user input for start and end positions
        start, end = get_user_input()
        
        # First test the path without moving the robot
        print("\nSimulating path before robot movement...")
        test_path(adjacency_list, start, end)
        
        # Ask the user if they want to navigate with the robot
        while True:
            choice = input("\nNavigate with the robot? (y/n): ").lower()
            if choice in ('y', 'yes'):
                print("\nNavigating maze with robot...")
                navigate_maze(adjacency_list, start, end)
                break
            elif choice in ('n', 'no'):
                print("Robot navigation cancelled.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        # Ask if they want to try another path
        while True:
            another = input("\nWould you like to try another path? (y/n): ").lower()
            if another in ('y', 'yes'):
                start, end = get_user_input()
                test_path(adjacency_list, start, end)
                
                while True:
                    choice = input("\nNavigate with the robot? (y/n): ").lower()
                    if choice in ('y', 'yes'):
                        navigate_maze(adjacency_list, start, end)
                        break
                    elif choice in ('n', 'no'):
                        print("Robot navigation cancelled.")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            elif another in ('n', 'no'):
                print("Goodbye!")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                
    except FileNotFoundError:
        print(f"Error: Could not find the pickle file '{pickle_file}'")
        print("Please run the maze scanning program first to generate the maze data.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()