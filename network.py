# import dictionary for graph
from collections import defaultdict

######## NOTE: idk if we need a vertex class or can just represent them as strings
class Vertex:
    def __init__(self,string,source=False,sink=False):
        self.string = string # for display purposes
        self.source = source # is this vertex a source?, default false
        self.sink = sink # is this vertex a sink?, default false


class Network:

    def __init__(self):
        self.graph = defaultdict(list) # Array list of all edges, edge (u,v) is a string pair
        self.source = Vertex('sr',True,False) # network source
        self.sink = Vertex('sk',False,True) # network sink
        self.vertices = [self.source,self.sink] # list of existing vertices
        self.paths = []

        self.costs = dict() # Cost along edge, stored (alpha,beta) pairs where cost is calculated alpha*x+beta
        self.flows = dict() # Flow along any edge, i.e. the number of agents taking that edge


    # Create new edge with cost, cost=0 by default and flow starts at 0
    def addEdge(self,u,v,alpha=0,beta=0):
        if u.sink:
            print("Cannot add edge from the sink")
            return
        if v.source:
            print("Cannot add an edge to the source")
            return
        if u not in self.vertices:
            self.vertices.append(u)
        if v not in self.vertices:
            self.vertices.append(v)
        self.graph[u].append(v)
        self.costs[(u,v)]=(alpha,beta)
        self.flows[(u,v)]=0

    # Return a list of all vertices that are on directed edge from vertex u
    def getNextVertices(self,u):
        return self.graph[u]

    # get all edges in the network
    def generate_edges(self):
        edges = []
        # for each node in graph
        for node in self.graph:
            # for each neighbour node of a single node
            for neighbour in self.graph[node]:
                # if edge exists then append
                edges.append((node, neighbour))
        return edges

    # Set the cost for an edge
    def setCost(self,u,v,alpha,beta):
        if v in self.graph[u]:
            self.costs[(u,v)]=(alpha,beta)
        else:
            print("No edge",(u,v))

    # Set the flow along an edge
    def setFlow(self,u,v,x):
        if v in self.graph[u]:
            self.flows[(u,v)]=x
        else:
            print("No edge",(u,v))

    # Increments flow on an edge by 1
    def incrementFlow(self,u,v):
        self.setFlow(u,v,self.flows[(u,v)]+1)

    # Decrements flow on an edge by 1
    def decrementFlow(self,u,v):
        self.setFlow(u,v,self.flows[(u,v)]-1)

    # Calculate the cost to a single agent from edge (u,v)
    def getEdgeCost(self,u,v):
        # return alpha * x + beta
        return self.costs[(u,v)][0] * self.flows[(u,v)] + self.costs[(u,v)][1]

    # Calculate total cost of current congestion
    def calcTotalCost(self):
        # return sum over edges (edge cost * flow along edge)
        cost = 0
        edges = self.generate_edges()
        for (u,v) in edges:
            cost += self.getEdgeCost(u,v) * self.flows[(u,v)]
        return cost
    
    def convertVerticesToEdges(self, path):
        edgesPath = []
        for i in range(len(path)):
            if i < len(path) - 1:
                edgesPath.append((path[i], path[i+1]))
        return edgesPath


    def getAllPathsUtil(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)
 
        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            self.paths.append(self.convertVerticesToEdges(path))
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i] == False:
                    self.getAllPathsUtil(i, d, visited, path)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False
  

    # paths in the form [(src,a),(a,b),(b,c),(c,sink)]
    #   returns a list of paths
    def getAllPaths(self, s, d):
 
        # Mark all the vertices as not visited
        visited = {}
        for vertex in self.vertices:
            visited[vertex] = False

        # Create an array to store paths
        path = []
 
        # Call the recursive helper function to print all paths
        self.getAllPathsUtil(s, d, visited, path)
    

    # helper function
    def getCostAlongPath(self,path):
        cost = 0
        for edge in path:
            cost += self.getEdgeCost(edge[0], edge[1])
        return cost
    

    # add an agent taking this path
    def addOneToPath(self,path):
        for edge in path:
            self.incrementFlow(edge[0], edge[1])


    # subtract an agent taking this path
    def subtractOneFromPath(self,path):
        for edge in path:
            self.decrementFlow(edge[0], edge[1])


    def displayNetwork(self):
        # check network is valid
        if self.checkNetwork()==False:
            print("Invalid network, cannot display")
        
        # display edges
        edges = self.generate_edges()
        print("Network state:")
        for (u,v) in edges:
            print("\t"+u.string+" --> "+v.string,
            "\tagents: "+str(self.flows[(u,v)]),
            "\tcost/agent: "+str(self.getEdgeCost(u,v)))
        

        # display paths
        print("\nPaths from src to sink:")
        for p in self.paths:
            for e in p:
                print(e[0].string + " -> ",end="")
                if e[1]==self.sink:
                    print(e[1].string)
        print()


    # Use BFS to make sure this is a valid network
    #   i.e. all vertices should point to the sink
    # idk if this actually works, from geeksforgeeks
    def checkNetwork(self,debug=False):

        # Check source and sink are actually a source and sink
        for v in self.vertices:
            if self.source in self.getNextVertices(v):
                if debug:
                    print("Invalid network")
                    print("Cannot have vertex pointing to source")
                return False
        if self.getNextVertices(self.sink):
            if debug:
                print("Invalid network")
                print("Cannot have the sink point to another vertex")
            return False


        # Mark all the vertices as not visited
        visited = dict.fromkeys(self.vertices,False)
       
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as
        # visited and enqueue it
        queue.append(self.source)
        visited[self.source] = True
 
        while queue:
 
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)

            # if this vertex has no more edges, check it's a sink
            if len(self.getNextVertices(s))==0:
                if not s.sink:
                    if debug:
                        print("Invalid network")
                        print("Cannot end on non-sink")
                    return False
 
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.getNextVertices(s):
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True

        for v in self.vertices:
            if not visited[v]:
                if debug:
                    print("Invalid network")
                    print("Cannot have unreachable vertex from source")
                return False

        if debug:
            print("Network passed!")
        return True