from network import Network
from network import Vertex

# create and test a network
def main():
    network = Network()
    a = Vertex('a')
    b = Vertex('b')
    network.addEdge(network.source,a,1,0)
    network.addEdge(network.source,b)
    network.addEdge(a,network.sink,1,0)
    network.addEdge(b,network.sink)
    network.addEdge(a, b)
    network.getAllPaths(network.source, network.sink)
    print(network.getCostAlongPath(network.paths[0]))

    #print(network.generate_edges())
    network.addOneToPath(network.paths[0])
    network.checkNetwork()
    network.displayNetwork()

main()