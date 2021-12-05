from network import Network
from network import Vertex
from agent import Agent
import matplotlib.pyplot as plt
import numpy as np

# simulate agents finding equilibrium on a network
def main():
    flowWithoutHighway  = []
    flowWithHighway = []
    totalCostWithHighway = []
    totalCostWithoutHighway = []    
    for i in range(1, 2001):
        flow1, flow3, cost = run_simulation(i, False)
        totalCostWithoutHighway.append(cost)
    for i in range(1, 2001):
        flow1, flow3, cost = run_simulation(i)
        flowWithoutHighway.append(flow1)
        flowWithHighway.append(flow3)
        totalCostWithHighway.append(cost)
    x = list(range(1, 2001))
    plt.figure(0)
    plt.plot(x, flowWithoutHighway, label = "Flow on routes 1 and 2")
    plt.plot(x, flowWithHighway, label = "Flow on route 3")
    plt.legend()
    plt.figure(1)
    plt.plot(x, totalCostWithHighway, label = "Total cost with highway")
    plt.plot(x, totalCostWithoutHighway, label = "Total cost without highway")
    plt.legend()
    plt.show()

def run_simulation(demand, highway = True):
    max_iters = 20 # should turn into command line argument
    num_agents = demand

    network = Network()
    a = Vertex('a')
    b = Vertex('b')

    # network.addEdge(network.source,a,0,0.01) # cost x/100
    # network.addEdge(network.source,b,15,0) # cost 15
    # network.addEdge(a,network.sink,15,0) # cost 15
    # network.addEdge(b,network.sink,0,0.01) # cost x/100
    network.addEdge(network.source,a,0,0.01) # 
    network.addEdge(network.source,b,15, 0) # 
    network.addEdge(a,network.sink,15,0) # 
    network.addEdge(b,network.sink,0,0.01) # 
    if highway:
        network.addEdge(a,b,7.5,0) # cost 0
        # network.addEdge(a,b,0,0) # cost 0

    # test validity of network and display
    network.checkNetwork(debug=True)

    
    # make sure to generate paths from source to sink
    network.getAllPaths(network.source,network.sink)


    # initialize agents on this network
    agents = []
    for i in range(num_agents):
        agents.append(Agent(network,id=str(i)))

    # run the simulation
    for i in range(max_iters):
        equilibrium = True # whether current round is in equilibrium
        for agent in agents:
            if agent.updateAndCheckChanged(): # if returns true, then we are not in equilibrium
                equilibrium = False
        if equilibrium: # no need to continue if we're in equilibrium
            print("Reached Equilibrium! Iteration:",i)
            break
        if i==max_iters-1:
            print("Reached max iters, not equilibrium.")

    # display the new state of the network:
    network.displayNetwork()
    print("Total Cost: "+str(network.calcTotalCost())+"\n")
    return (network.pathFlows[0], network.pathFlows[1], network.calcTotalCost())
        

main()