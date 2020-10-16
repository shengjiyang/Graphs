from room import Room
from player import Player
from world import World
import os
import random
from ast import literal_eval
import time
from operator import attrgetter
from collections import deque
from data_structures import Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = os.path.join("projects", "adventure", "maps", "test_line.txt") # Passed
# map_file = os.path.join("projects", "adventure", "maps", "test_cross.txt") # Passed
# map_file = os.path.join("projects", "adventure", "maps", "test_loop.txt") # Passed
# map_file = os.path.join("projects", "adventure", "maps", "test_loop_fork.txt") # Passed
map_file = os.path.join("projects", "adventure", "maps", "main_maze.txt")

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Traversal Function

# First Pass Attempt

graph = {}

def traverse_map(random_seed):
    dft_start = time.time()

    random.seed(random_seed)
    fx = random.choice(player.current_room.get_exits()) 

    current_room = player.current_room

    graph = {}

    graph[current_room.id] = {}
    for direction in current_room.get_exits():
        graph[current_room.id][direction] = "?"

    opposites = {"n": "s", "s": "n", "w": "e", "e": "w"}

    while current_room and len(visited_rooms) < len(room_graph):
        if time.time() - dft_start > 0.5:
            break

        if current_room not in visited_rooms:
            graph[current_room.id] = {}

            for direction in current_room.get_exits():
                graph[current_room.id][direction] = "?"
           
            if attrgetter(f"{opposites[fx]}_to")(current_room) in visited_rooms:
                graph[current_room.id][f"{opposites[fx]}"] = attrgetter(f"{opposites[fx]}_to.id")(current_room)

            for room in visited_rooms:
                for direction in room.get_exits():
                    if attrgetter(f"{direction}_to")(current_room) in visited_rooms:
                        graph[room.id][f"{opposites[direction]}"] = attrgetter(f"{opposites[direction]}_to.id")(room)

            if len(current_room.get_exits()) == 1:
                graph[current_room.id][current_room.get_exits()[0]] = attrgetter(f"{current_room.get_exits()[0]}_to.id")(current_room)

                q = deque()
                q.append(current_room.get_exits())

                bfs_start = time.time()

                while "?" not in graph[current_room.id].values():
                    if time.time() - bfs_start > 0.5:
                        break

                    current_path = q.popleft()

                    for i in range(len(current_room.get_exits())):
                        path_copy = current_path
                        path_copy.append(list(graph[current_room.id].keys())[i])
                            
                        q.append(path_copy)

                    for dir_ in path_copy:
                        if attrgetter(f"{dir_}_to")(current_room):
                            traversal_path.append(dir_)
                            current_room = attrgetter(f"{dir_}_to")(current_room)

                if fx in current_room.get_exits():
                    possible_fx = current_room.get_exits()
                    possible_fx.pop(possible_fx.index(fx))
                    fx = random.choice(possible_fx)

            if fx not in current_room.get_exits():
                possible_fx = current_room.get_exits()
                fx = random.choice(possible_fx)

        if attrgetter(f"{fx}_to")(current_room):
            traversal_path.append(fx)
            current_room = attrgetter(f"{fx}_to")(current_room)

    # print(traversal_path)
    print(len(traversal_path))
    print(graph)

# traverse_map(84)

# Second Pass Attempt

# DFT requires a Stack
stack = Stack()

# Opposite Direction
opposites = {"n": "s", "s": "n", "w": "e", "e": "w"}

# Ensures that we don't have to restart Anaconda Prompt every time that something breaks.
dft_start = time.time()

while len(visited_rooms) < len(world.rooms):
    if time.time() - dft_start > 0.5:
            break

    # Check all neighboring rooms
    # if room not in visited rooms,
        # append to directions array
    neighbors = player.current_room.get_exits()
    directions = []
    for neighbor in neighbors:
        if neighbor and player.current_room.get_room_in_direction(neighbor) not in visited_rooms:
            directions.append(neighbor)

    # Initializes random direction to move in
    if len(directions) > 0:
        fx = random.choice(directions)
        stack.push(fx)
        traversal_path.append(fx)

    else:
        current = stack.pop()
        traversal_path.append(opposites[current])

print(directions)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
