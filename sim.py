from network import Network
from network import Vertex
from agent import Agent

# simulate agents finding equilibrium on a network
def main():
    max_iters = 100 # should turn into command line argument

    # create the network
    network = Network()
    a = Vertex('a')
    b = Vertex('b')
    network.addEdge(network.source,a,1,0) # cost x
    network.addEdge(network.source,b,0,1) # cost 1
    network.addEdge(a,network.sink,0,1) # cost 1
    network.addEdge(b,network.sink,1,0) # cost x


    # test validity of network and display
    network.checkNetwork(debug=True)
    network.displayNetwork()

    
    # make sure to generate paths from source to sink
    network.getAllPaths(network.source,network.sink)


    # initialize agents on this network
    agents = []
    for i in range(10):
        agents.append(Agent(network,id=str(i)))

    # run the simulation
    for i in range(max_iters):
        equilibrium = True # whether current round is in equilibrium
        for agent in agents:
            if agent.updateAndCheckChanged(): # if returns true, then we are not in equilibrium
                equilibrium = False
        if equilibrium: # no need to continue if we're in equilibrium
            print("Reached Equilibrium!")
            break
        if i==max_iters-1:
            print("Reached max iters, not equilibrium.")

    # display the new state of the network:
    network.displayNetwork()
    print("Total Cost:"+str(network.calcTotalCost())+"\n")

        

main()