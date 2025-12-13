import heapq
import copy
import math

class routing:
    def __init__(self, graph_dict):
        self.graph = graph_dict

        self.DV = {}
        self.init_distance_vectors()


    def init_distance_vectors(self):
        self.DV = {}

        for node in self.graph:
            self.DV[node] = {}
            for dest in self.graph:
                if node == dest:
                    self.DV[node][dest] = 0
                elif dest in self.graph[node]:
                    self.DV[node][dest] = self.graph[node][dest]
                else:
                    self.DV[node][dest] = math.inf


    def distance_vector_iteration(self):
        old_DV = copy.deepcopy(self.DV)

        # Loop through nodes
        for x in self.graph:
            
            new_distances = copy.deepcopy(self.graph[x])
            
            # Loop through node neighbours
            for v, cost_xv in self.graph[x].items():

                # Loop through nodes
                for d in old_DV[v]:
                    if d == x:
                        continue
                    
                    new_cost = cost_xv + old_DV[v][d]
                    
                    if d not in new_distances or new_cost < new_distances[d]:
                        new_distances[d] = new_cost
            self.DV[x] = new_distances

    def print_dv_node(self, node):
        print(f"Distance Vector for {node}")
        print("--------------------------------")
        for dest in sorted(self.DV[node]):
            cost = self.DV[node][dest]
            if cost == math.inf:
                print(f"{dest} unreachable")
            else:
                print(f"{dest} {cost}")
       
    def print_dv(self):
        # Get all nodes
        nodes = sorted(self.DV.keys())
        
        if not nodes:
            print("No nodes in distance vector table")
            return
        
        # Print header
        print("\nRouting Table for each Node (routing table is below node header)")
        print("=" * (8 + 6 * len(nodes)))
        
        # Column headers (sources)
        header = "Routers:".ljust(8)
        for src in nodes:
            header += src.center(6)
        print(header)
        print("-" * (8 + 6 * len(nodes)))
        
        # Each row is a destination
        for dest in nodes:
            row = dest.ljust(8)
            for src in nodes:
                # Access cost from src → dest
                if dest in self.DV[src]:
                    cost = self.DV[src][dest]
                    if cost == math.inf:
                        row += "inf".center(6)
                    else:
                        row += str(cost).center(6)
                else:
                    row += "0".center(6)
            print(row)
        
        print()

    def dijkstra(self, start):
        if start not in self.graph:
            print(f"Error: Node {start} does not exist.")
            return
        
        # init Distance table
        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0

        # init Previous-hop table
        prev = {node: None for node in self.graph}

        # init Priority queue
        pq = [(0, start)]

        while pq:
            current_cost, u = heapq.heappop(pq)

            if current_cost > dist[u]:
                continue

            for v, weight in self.graph[u].items():
                new_cost = current_cost + weight

                if new_cost < dist[v]:
                    dist[v] = new_cost

                    prev[v] = u
                    heapq.heappush(pq, (new_cost, v))

        self.print_table(start, dist, prev)


    def get_first_hop(self, start, node, prev):
        # Return the first hop from the start along the shortest path
        if node == start:
            return "-"

        # reconstruct full path
        path = []
        cur = node
        while cur is not None:
            path.append(cur)
            cur = prev[cur]

        path.reverse()  # now path[0] = start

        if len(path) < 2:
            return None
        return path[-2]  # the last hop to the end (obtained with second to last item in list)


    def print_table(self, start, dist, prev):
        print(f"Link-State Routing Table for {start}")
        print("------------------------------")

        # sort by cost
        nodes = sorted(dist.keys(), key=lambda x: (dist[x], x))

        for node in nodes:
            if dist[node] == float('inf'):
                continue

            via = self.get_first_hop(start, node, prev)

            if node == start:
                print(f"{node} - 0")
            else:
                print(f"{node} {via} {dist[node]}")
