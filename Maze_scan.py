from motion import Movement
from motion import Chris_R
import math
import time
time.sleep(2)

def get_lidar(dir,rL,rU):
    directions= {
        "W" : 90,
        "E" : 270,
        "N" : 180,
        "S" : 0
    }
    temp = []
    sight = Chris_R.get_range_image()
    orientation = Movement.currentDirection
    robot_dir_angle = directions.get(dir)
    center = (orientation - 90 + robot_dir_angle) % 360
    
    #sets initial prev to be an array
    for i in range(rL,rU):
        idx = (center + i) % 360
        if sight[idx] != -1:
            temp.append(sight[idx])
        
    if temp:
        return min(temp)
    else:
        return -1
    
def add_wall(graph, a, b):
    graph[a] = [n for n in graph[a] if n[0] != b]
    graph[b] = [n for n in graph[b] if n[0] != a]

def pmaze(maze):
    for n,m in maze.items():
        print(n,m)
def get_direction(from_node, to_node, size=3):
    r1, c1 = divmod(from_node, size)
    r2, c2 = divmod(to_node, size)

    if r2 == r1 - 1 and c2 == c1:
        return "N"
    elif r2 == r1 + 1 and c2 == c1:
        return "S"
    elif r2 == r1 and c2 == c1 - 1:
        return "W"
    elif r2 == r1 and c2 == c1 + 1:
        return "E"
    else:
        return None
def moveto(frm,to):
    direction = get_direction(frm,to)
    if direction:
        Movement.face(direction,1.59)
    
def create_adj_list(size):
    width = height = size
    graph = {}

    def node(row, col):
        return row * width + col

    for row in range(height):
        for col in range(width):
            current = node(row, col)
            neighbors = []

            # Up
            if row > 0:
                neighbors.append((node(row - 1, col), 1))
            # Down
            if row < height - 1:
                neighbors.append((node(row + 1, col), 1))
            # Left
            if col > 0:
                neighbors.append((node(row, col - 1), 1))
            # Right
            if col < width - 1:
                neighbors.append((node(row, col + 1), 1))

            graph[current] = neighbors

    return graph
    
def scan(maze, current):
    # Maze is 3x3, so determine row and col
    size = 3
    row, col = divmod(current, size)

    # Neighbor directions with (row offset, col offset)
    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1)
    }

    for dir, (dr, dc) in directions.items():
        r, c = row + dr, col + dc
        if 0 <= r < size and 0 <= c < size:
            neighbor = r * size + c
            dist = get_lidar(dir, -10, 10)

            if dist >= 0 and dist < 500:
                add_wall(maze, current, neighbor)
                print(f"({dir},{current},{neighbor})")
    
    
    
def dfs(graph, current, visited, path):
    visited.add(current)
    path.append(current)  # robot enters the cell
    print(f"In cell: {current} Visited : {visited}")

    scan(graph,current)
    
    for neighbor, _ in graph[current]:
        if neighbor not in visited:
            moveto(current,neighbor)
            dfs(graph, neighbor, visited, path)
            moveto(neighbor,current)
            path.append(current)  # robot returns (backtracks)
            print(f"Back to cell: {current}")
def main():
    global blank_maze
    blank_maze = create_adj_list(3)
    visited = set()
    path = list()
    dfs(blank_maze,0,visited,path)
    pmaze(blank_maze)
    
main()