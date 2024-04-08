import time
import random
import math

#Heuristic used to detect a near impassible. In this case, a stop sign to slow the speed down
def improved_manhatten(current_node,car,end_node,impassable,stop_sign,manhatten,maze,estimate = .7):
    '''
    Manhatten distance using a combination of pythagorean and manhatten distance formulas
    Given also a list of coordiantes that are impassable to check an approzimate where they may be close to one
    '''
    #set a pentaly if an impassable is near
    penalty = 0.9
    
    pythagorean = math.sqrt(((current_node.position[0] - end_node.position[0])**2) 
                            + (current_node.position[1] - end_node.position[1])**2)

    # combination of pythagorean and manhatten with estimate 
    combination = manhatten + estimate*pythagorean


    if not car.stopped:
        for stop in stop_sign:
            
            if near_stop(current_node,stop):
                car.speed = car.speed - 10
                current_node.speed = car.speed
                #if at the stop sign area
                if maze[current_node.position[0]][current_node.position[1]] == 0:
                    car.speed = 0
                    car.stopped = True
                #bug fix
                break
    print(car.speed, current_node.position)


    for obstacle in impassable:
        if near_impassable(current_node,obstacle):
            combination += penalty
    return int(combination)

def near_impassable(node,obstacle):
    """
    helper function to check if the current node is near an impassable location
    """
    #set a proximity view if impassable is near detection
    proximity = 10
    return abs(node.position[0] - obstacle[0]) <= proximity and abs(node.position[1] - obstacle[1]) <= proximity

def near_stop(node,stop):
    """
    helper function to check if the current node is near an impassable location
    """
    #set a proximity view if impassable is near detection
    proximity = 3
    return abs(node.position[0] - stop[0]) <= proximity and abs(node.position[1] - stop[1]) <= proximity

class Car():
    def __init__(self,distance=0, speed=0, stopped = False, obstacle_visted = set()):
        self.distance = distance
        self.speed = speed
        self.stopped = stopped
        self.obstacle_visted = obstacle_visted



class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, cost = 0, distance=0, speed=0):
        self.parent = parent
        self.position = position
        self.cost = cost
        self.distance = distance
        self.speed = speed

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    car = Car()
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    #list of impassibles to keep in check - used for H3
    impassable = []

    #list of location where stop sign present
    stop_sign = []

    open_list.append(start_node)
    
    start_time = time.time()

    if maze[end[0]][end[1]] == -1:
        print("End node is not reachable.")
        return ''

    visited = set()

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append((current.position,'{0} feet'.format(current.distance), '{0} X/X'.format(current.speed)))
                current = current.parent
            end_time = time.time()
            for p in path[::-1]:
                print("Path: {0}\n".format(p))
            print("Number of nodes created: ", len(closed_list))
            print("Total Distance Car Traveled: {0}".format(path[0]))
            print("Runtime(ms): ", (end_time - start_time) * 1000)
            return ''

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] == -1:
                impassable += [[int(node_position[0]),int(node_position[1])]]
                continue

            if maze[node_position[0]][node_position[1]] == 0:
                stop_sign += [[int(node_position[0]),int(node_position[1])]]
                car.obstacle_visted.add(maze[node_position[0]][node_position[1]])

            new_node = Node(current_node, node_position, maze[node_position[0]][node_position[1]])
            # print(maze[node_position[0]][node_position[1]])
       
            if any(node.position == new_node.position for node in closed_list) or new_node.position in visited:
                continue


            visited.add(new_node.position)

            children.append(new_node)

        for child in children:

            child.g = current_node.g + child.cost
            #keep track of car distance where 1 cost is 10 feet
            child.distance = child.g*60
            if(maze[child.position[0]][child.position[1]]== 1):
                car.speed = 20
                child.speed = car.speed
                #if a stop sign was already visited, keep speed the same (according to driving rules)
                if maze[child.position[0]][child.position[1]] in car.obstacle_visted:
                    car.speed = 20
            # child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            manhatten = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.h = improved_manhatten(child,car,end_node,impassable,stop_sign, manhatten, maze)
            child.f = child.g + child.h

            open_list.append(child)
            
    print("Path not found.")
    print("Number of nodes created:", len(closed_list))
    end_time = time.time()
    print("Runtime (ms):", (end_time - start_time) * 1000)
    print("Runtime (ms):", (end_time - start_time) * 1000)

def main():

    file_path = input("Enter the path to the maze text file: ")
    with open(file_path, 'r') as file:
        maze = []
        for line in file:
            row = [int(x) for x in line.strip().split()]
            maze.append(row)
    
    start = tuple(int(x) for x in input("Enter the start coordinates (row, col): ").split())
    goal = tuple(int(x) for x in input("Enter the goal coordinates (row, col): ").split())
    
    path = astar(maze, start, goal)
    print(path)

if __name__ == '__main__':
    main()
