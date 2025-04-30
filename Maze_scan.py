from robot_systems.robot import HamBot
from motion import Movement
import math
import time

move = Movement()
Chris_R = HamBot()
time.sleep(2)

def get_lidar(dir,rL,rU):
    directions= {
        "left" : 90,
        "right": 270,
        "forw" : 180,
        "back" : 0
    }
    center = directions.get(dir)
    temp = []
    sight = Chris_R.get_range_image()
    
    #sets initial prev to be an array
    for i in range(rL,rU):
        idx = center + i
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
    
def scan(maze):
    W,N,E,S = 180,90,0,270
    
def dfs(graph, current, visited, path):
    visited.add(current)
    path.append(current)  # robot enters the cell
    print(f"In cell: {current}")

    for neighbor, _ in graph[current]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, path)
            path.append(current)  # robot returns (backtracks)
            print(f"Back to cell: {current}")
def main():
    blank_maze = create_adj_list(3)
    visited = set()
    path = list()
    add_wall(blank_maze,1,2)
    add_wall(blank_maze,3,4)
    add_wall(blank_maze,4,7)
    dfs(blank_maze,0,visited,path)
    
    
main()