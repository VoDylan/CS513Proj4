import sys
from linkstate import GraphLS

graph = {'A' : {'B' : 2, 'E' : 6, 'D' : 5}, 'B' : {'A' : 2, 'C' : 1}, 'C' : {'B' : 1, 'E' : 3, 'H' : 1}, 'D' : {'A' : 5, 'E' : 4, 'F' : 2}, 'E' : {'A' : 6, 'D' : 4, 'F' : 1, 'C' : 3}, 'F' : {'D' : 2, 'E' : 1, 'G' : 3}, 'G' : {'F' : 7, 'H' : 3}, 'H' : {'G' : 3, 'C' : 1}}



# Get the first argument (python3 main.py <graph_file>)
try:
    # File given as input
    graph_file = sys.argv[1]
except: 
    # Prompt user for input
    print("Enter nodes in the format 'X Y cost', pressing enter after each. \nTo finish, type 'done'. \nTo view your graph, type 'view'.\nTo clear your graph, type 'clear'.")
    
    while (1):
        user_in = input('>>> ')
        if (user_in.lower() == "done" or user_in.lower() == "d"): break
        if (user_in.lower() == "view" or user_in.lower() == "v"): 
            for key, value in graph.items():
                print(f"{key}: {value}")
            continue
        if (user_in.lower() == "clear" or user_in.lower() == "c"): 
            graph.clear()
            continue
        
        try:
            [x, y, cost] = user_in.split()
            
            # Remove an edge
            if cost == '-':
                try:
                    del graph[x][y]
                except:
                    print("Edge" + x + "->" + y + " doesn't exist")
                try:
                    del graph[y][x]
                except:
                    print("Edge" + y + "->" + x + " doesn't exist")
            else: 
                if x not in graph: 
                    graph[x] = {y : int(cost)}
                else:
                    graph[x][y] = int(cost)
                    
                if y not in graph:
                    graph[y] = {x : int(cost)}
                else: 
                    graph[y][x] = int(cost)
        except:
            print("Please enter a valid input.")


graphLS = GraphLS(graph)
graphLS.dijkstra("A")
graphLS.dijkstra("X")