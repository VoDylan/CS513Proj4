import sys
from routing import routing

def process_line(graph, line):
    try:
        x, y, cost = line.split()
    except:
        print("Invalid input")
        return
    
    if cost == '-':  # remove edge
        try:
            del graph.graph[x][y]
        except:
            pass
        try:
            del graph.graph[y][x]
        except:
            pass
        return
    
    cost = int(cost)

    if x not in graph.graph:
        graph.graph[x] = {y: cost}
    else:
        graph.graph[x][y] = cost

    if y not in graph.graph:
        graph.graph[y] = {x: cost}
    else:
        graph.graph[y][x] = cost

# Run
graph = routing({})
try:
    graph_file = sys.argv[1]

    with open(graph_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            process_line(graph, line)

    print("Graph loaded successfully:\n")
    for key, value in graph.graph.items():
        
        print(f"{key}: {value}")

except:
    pass

print("Enter nodes in the format 'X Y cost', pressing enter after each. A cost of '-' will delete the edge") 
print("To view your graph, type 'view'")
print("To clear your graph, type 'clear'")
print("To run linkstate, type 'ls X' to generate all paths from node X to all other nodes")
print("To run an iteration of distance vector, type 'dv X' to print the routing table for node X, or just 'dv' to run an iteration and print all routing tables")
print("To exit, type 'done' or 'exit'")


graph.init_distance_vectors()

while True:
    user_in = input('>>> ')

    if user_in.lower() in ["done", "d", "exit", "e"]:
        break

    if user_in.lower() in ["view", "v"]:
        for key, value in graph.graph.items():
            print(f"{key}: {value}")
        continue
    
    if user_in.lower() in ["clear", "c"]:
        graph.graph.clear()
        continue
    
    if user_in.lower() in ["dv"]:
        graph.distance_vector_iteration()
        graph.print_dv()
        continue

    # Handle ls X or dv X
    try:
        cmd, node = user_in.split()
        if cmd.lower() == "ls":
            graph.dijkstra(node)
            continue
        elif cmd.lower() == "dv":
            graph.distance_vector_iteration()
            graph.print_dv_node(node)
            continue
    except:
        pass

    # Handle X Y cost
    try:
        process_line(graph, user_in)
    except:
        print("Please enter a valid input.")