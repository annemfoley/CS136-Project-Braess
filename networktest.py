from network import Network
from network import Vertex

# create and test a network
def main():
    network = Network()
    a = Vertex('a')
    b = Vertex('b')
    network.addEdge(network.source,a)
    network.addEdge(network.source,b)
    network.addEdge(a,network.sink)
    network.addEdge(b,network.sink)
    network.getAllPaths(network.source, network.sink)

    #print(network.generate_edges())
    network.checkNetwork()
    network.displayNetwork()

main()