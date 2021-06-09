class Graph():
    """
    The Graph class creates an an graph object of the form of adjacency matrix
    The rows & columns of the matrix are mapped to the vertices of the input graph
    Each vertex represents the junction in Harsh's locality.
    Each edge represents the path between two junctions.
    The values in the matrix indicate the weight of the edges of the graph i.e number of containment zones
    """

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def minDistance(self, dist, sptSet):
        """
        Method to find the vertex with minimum distance value, from the set of vertices not yet included in shortest
        path tree
        :param dist: dynamically updated list containing shortest distances of vertices from the source
        :param sptSet: list containing vertices part of the shortest path
        :return: Index of the vertex having minimum distance
        """
        # Initilaize minimum distance for next node
        minim = float('inf')

        # Search not nearest vertex not in the shortest path tree
        for v in range(self.V):
            if dist[v] < minim and sptSet[v] == False:
                minim = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, src, dest1, dest2):
        """
        Function that implements Dijkstra's single source shortest path algorithm for a graph represented using
        adjacency matrix representation
        :param src: Harsh's house
        :param dest1: Pharmacy 1
        :param dest2: Pharmacy 2
        :return: dist : updated list of shortest distances of vertices from the source
                 prev : list of predecessors of the vertices as per the shortest path tree.
        """

        dist = [float('inf')] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        prev = [''] * self.V
        for cout in range(self.V):
            # Pick the minimum distance vertex from the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices of the picked vertex only if the current distance is greater
            # than new distance and the vertex in not in the shotest path tree
            for v in range(self.V):
                if ((self.graph[u][v] > 0) and (sptSet[v] == False) and (dist[v] > dist[u] + self.graph[u][v])):
                    dist[v] = dist[u] + self.graph[u][v]
                    prev[v] = u

        # Trace shortest path to pharmacy 1
        path1 = [dest1]
        pred1 = ''
        cost1 = dist[dest1]
        while (pred1 != src):
            pred1 = prev[dest1]
            path1.append(pred1)
            dest1 = pred1
        path1.reverse()
        # Trace shortest path to pharmacy 2
        path2 = [dest2]
        pred2 = ''
        cost2 = dist[dest2]
        while (pred2 != src):
            pred2 = prev[dest2]
            path2.append(pred2)
            dest2 = pred2
        path2.reverse()

        # Compare the no. of containment zones in the paths towards the 2 pharmacies
        if cost1 > cost2:
            path = path2
            cost = cost2
            pharm = 'Pharmacy 2'
        else:
            path = path1
            cost = cost1
            pharm = 'Pharmacy 1'
        return pharm, path, cost

class Preprocess():
    """
    Class to read input file and preprocess data in the format of adjacency matrix
    """
    def __init__(self, infile):
        self.infile = infile

    def read_file(self):
        """
        Read the input file and obtain below key information
        -Junctions of Harsh's locality (Graph vertices)
        -Path between two junctions (Graph edges)
        -No. of containment zones in the particular path (Edge weight)
        -Harsh's house  (Starting point of the path to pharmacy)
        -Pharmacy 1 junction (Destination 1 of the path)
        -Pharmacy 2 junction (Destination 2 of the path)
        The input data is stored in python lists and later used for processing
        """
        with open(self.infile, "r") as fp:
            lines = fp.readlines()
            vertex_lst = []
            edge_wt_lst = []
            house = []
            pharm_lst = []
            for line in lines:
                if (line.find("/") > -1):
                    u = line.strip().split("/")[0].strip()  # Start vertex
                    v = line.strip().split("/")[1].strip()  # End vertex
                    w = line.strip().split("/")[2].strip()  # Weight of the edge
                    # Update the edge weight list with the information provided in each line of the input file
                    edge_wt_lst.append([u, v, w])

                    # Update the master vertex list with the vertices from the input file
                    if (u not in vertex_lst):
                        vertex_lst.append(u)
                    else:
                        continue
                    if (v not in vertex_lst):
                        vertex_lst.append(v)
                    else:
                        continue
                elif (line.find("House:") > -1):
                    house.append(line.strip().split(":")[1].strip())
                else:
                    pharm_lst.append(line.strip().split(":")[1].strip())
        vertex_lst.sort()
        return vertex_lst, edge_wt_lst, house[0], pharm_lst[0], pharm_lst[1]

if __name__ == '__main__':
    # Define input/output file variables
    infile = 'inputPS8.txt'
    outfile = 'outputPS8.txt'

    # Read input file and preprocess data
    processor = Preprocess(infile)
    vertex_lst, edge_wt_lst, house, pharm1, pharm2 = processor.read_file()

    # Build graph
    graph_size = len(vertex_lst)
    # Create numeric index list equivalent from the input vertices to use in building adjacency matrix
    mtx_idx_lst = list(range(0, graph_size))
    src = mtx_idx_lst[vertex_lst.index(house)]
    dest1 = mtx_idx_lst[vertex_lst.index(pharm1)]
    dest2 = mtx_idx_lst[vertex_lst.index(pharm2)]

    # Re-Format the input graph data in the form of adjacency matrix
    gdata = [[0 for column in range(graph_size)] for row in range(graph_size)]
    for i in range(len(edge_wt_lst)):
        u = mtx_idx_lst[vertex_lst.index(edge_wt_lst[i][0])]  # Get numeric index for the vertex from the edge_wt_lst
        v = mtx_idx_lst[vertex_lst.index(edge_wt_lst[i][1])]
        gdata[u][v] = int(edge_wt_lst[i][2])
        gdata[v][u] = int(edge_wt_lst[i][2])

    # Create a graph data structure object in the form of  Adjacency Matrix and update the input graph information
    g = Graph(graph_size)
    g.graph = gdata
    pharm, path, cost = g.dijkstra(src, dest1, dest2)
    textpath = ' '
    for num_vertex in path:
        txt_vertex = vertex_lst[num_vertex]
        textpath = textpath + txt_vertex + ' '

    # Write output to output file
    outF = open(outfile, "w")
    outF.write("Safer Pharmacy is: {0}\n".format(pharm))
    outF.write("Path to follow:{0}\n".format(textpath))
    outF.write("Containment zones on this path: {0}".format(cost))