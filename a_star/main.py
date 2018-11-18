import sys
from PIL import Image
import copy
import math
import operator
import time

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)    # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = "" # a string reference to the original import file

'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
parents = {}
closed = {}   # a dictionary of (x,y) tuples, representing nodes that have been closed
open = {}   # a dictionary of (x,y) tuples, representing nodes to expand to in the future

pixel_wall_value = 1

def search(map):
    """
    This function is meant to use the global variables [start, end, path, closed, open] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """

    goal_cost = float("inf")
    open[start] = h(start)
    while True:
        open_sorted = sorted(open.items(), key = operator.itemgetter(1))
        current_point = open_sorted[0][0]
        current_cost = open_sorted[0][1]
        if check_for_goal(current_point):
            if new_cost < goal_cost:
                goal_cost = new_cost
            break
        neighbors = check_neighbors(current_point, map)
        if len(neighbors) == 0:
            print "stuck, no neighbors"
            break
        for neighbor in neighbors:
            new_cost = g(current_point) + 1
            if neighbor in open:
                if g(neighbor) <= new_cost:
                    continue
            elif neighbor in closed:
                if g(neighbor) <= new_cost:
                    continue
                open[neighbor] = closed[neighbor]
                del closed[neighbor]
            else:
                open[neighbor] = new_cost + h(neighbor)
                parents[neighbor] = current_point
        del open[current_point]
        closed[current_point] = current_cost

    current_point = end
    while current_point != start:
        path.append(current_point)
        current_point = parents[current_point]
    visualize_search("out.png") # see what your search has wrought (and maybe save your results)

def check_neighbors(current_point, map):
    neighbors = []

    #down
    try:
        if map[current_point[0], current_point[1] + 1] != pixel_wall_value:
            neighbors.append((current_point[0], current_point[1] + 1))
    except:
        pass
    #up
    try:
        if map[current_point[0], current_point[1] - 1] != pixel_wall_value:
            neighbors.append((current_point[0], current_point[1] - 1))
    except:
        pass
    #left
    try:
        if map[current_point[0 ] - 1, current_point[1]] != pixel_wall_value:
            neighbors.append((current_point[0] - 1, current_point[1]))
    except:
        pass
    #right
    try:
        if map[current_point[0] + 1, current_point[1]] != pixel_wall_value:
            neighbors.append((current_point[0] + 1, current_point[1]))
    except:
        pass
    return neighbors

def check_for_goal(point):
    if point == end:
        return True
    return False

def g(point):
    total_cost = 0
    current_point = point
    while current_point != start:
        current_point = parents[current_point]
        total_cost += 1
    return total_cost

def h(point):
    return math.sqrt((point[0] - end[0]) ** 2 + (point[1] - end[1]) ** 2)




def visualize_search(save_file="do_not_save.png"):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(difficulty).convert("RGB")
    pixel_access = im.load()

    # draw start and end pixels
    pixel_access[start[0], start[1]] = NEON_GREEN
    pixel_access[end[0], end[1]] = NEON_GREEN

    # draw open pixels
    for pixel in open.keys():
        pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

    # draw closed pixels
    for pixel in closed.keys():
        pixel_access[pixel[0], pixel[1]] = DARK_GRAY

    # draw path pixels
    for pixel in path:
        pixel_access[pixel[0], pixel[1]] = PURPLE

    # display and (maybe) save results
    #im.show()
    if(save_file != "do_not_save.png"):
        im.save(save_file)

    im.close()


if __name__ == "__main__":
    # Throw Errors && Such
    # global difficulty, start, end
    assert sys.version_info[0] == 2                                 # require python 2 (instead of python 3)
    assert len(sys.argv) == 2, "Incorrect Number of arguments"      # require difficulty input

    # Parse input arguments
    function_name = str(sys.argv[0])
    difficulty = str(sys.argv[1])
    print "running " + function_name + " with " + difficulty + " difficulty."

    # Hard code start and end positions of search for each difficulty level
    if difficulty == "trivial.gif":
        start = (8, 1)
        end = (20, 1)
    elif difficulty == "medium.gif":
        start = (8, 201)
        end = (110, 1)
    elif difficulty == "hard.gif":
        start = (10, 1)
        end = (401, 220)
    elif difficulty == "very_hard.gif":
        start = (1, 324)
        end = (580, 1)
    elif difficulty == "easy_maze.gif":
        pixel_wall_value = 0
        start = (530, 164)
        end = (532, 509)
    elif difficulty == "medium_maze.gif":
        pixel_wall_value = 0
        start = (225, 532)
        end = (530, 514)
    else:
        assert False, "Incorrect difficulty level provided"

    start_time = time.time()
    # Perform search on given image
    im = Image.open(difficulty)
    search(im.load())
    end_time = time.time()
    planning_time = end_time - start_time
    print("Planning Time: {}s".format(planning_time))
    print("Total Cost: {}".format(len(path)))

