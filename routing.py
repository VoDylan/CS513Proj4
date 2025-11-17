import heapq

class routing:
    def __init__(self, graph_dict):
        self.graph = graph_dict

    def dist_vect(self, start):
        pass

    def dijkstra(self, start):
        if start not in self.graph:
            print(f"Error: Node {start} does not exist.")
            return
        
        # Distance table
        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0

        # Previous-hop table
        prev = {node: None for node in self.graph}

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
        """Return the FIRST hop from the start along the shortest path."""
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
        return path[-2]  # the FIRST hop from the start (obtained with second to last item in list)


    def print_table(self, start, dist, prev):
        print(f"Link-State Routing Table for {start}")
        print("--------------------------------")

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
