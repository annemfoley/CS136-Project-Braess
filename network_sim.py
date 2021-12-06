from network import Network
from network import Vertex
from agent import Agent
import matplotlib.pyplot as plt
import numpy as np

# simulate agents finding equilibrium on a network
def main():
    # compare optimal cost with parallel road
    routeAlongNormal = []
    routeAlongParallel = []

    parallel_edge_costs = list(range(0,20))
    parallel_edge_costs = [c/100 for c in parallel_edge_costs]

    maxOptimalCost = []
    totalCostParallel = []


    for c in parallel_edge_costs:
        maxOptimalCost.append(simulate_parallel(2000))

        normalRouteFlow, parallelRouteFlow, parallelCost = simulate_parallel(2000,True,c)
        routeAlongNormal.append(normalRouteFlow)
        routeAlongParallel.append(routeAlongParallel)
        totalCostParallel.append(parallelCost)
    
    plot2(0,"Flow Along Normal Routes vs. Parallel Edge", "Parallel Edge Cost (beta*x)", "Flow Along Path",parallel_edge_costs,routeAlongNormal,parallel_edge_costs,routeAlongParallel,"Flow per for each normal routes","Flow along parallel edge")
    plot2(1,"Total Cost With Parallel Road vs. Max Optimal Cost","Parallel Edge Cost (beta*x)","Cost",parallel_edge_costs,totalCostParallel,parallel_edge_costs,maxOptimalCost,"Cost with parallel edge","Max optimal cost")

        


    # compare optimal cost with series road






def plot(figure, title, xlabel, ylabel, xdata, ydata, label):
    plt.figure(figure)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(xdata, ydata, label = label)
    plt.legend()

def plot2(figure, title, xlabel, ylabel, xdata, ydata, x2data, y2data, label, label2):
    plt.figure(figure)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(xdata, ydata, label = label)
    plt.plot(x2data, y2data, label = label2)
    plt.legend()

def simulate_parallel(demand,parallel_road=False,parallel_edge_cost=0):
    max_iters = 20 # should turn into command line argument
    num_agents = demand

    network = Network()
    a = Vertex('a')
    b = Vertex('b')

    network.addEdge(network.source, a, 0, 0.01) # x/100
    network.addEdge(network.source, b, 15, 0) # 15
    network.addEdge(a,network.sink, 15, 0) # 15
    network.addEdge(b,network.sink, 0, 0.01) # x/100 
    if parallel_road:
        network.addEdge(network.source,network.sink,0,parallel_edge_cost) # cost*x

    # test validity of network and display
    #network.checkNetwork(debug=True)

    # make sure to generate paths from source to sink
    network.getAllPaths(network.source,network.sink)


    # initialize agents on this network
    agents = []
    for i in range(num_agents):
        agents.append(Agent(network,id=str(i)))

    # run the simulation if parallel road
    if parallel_road:
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
        # network.displayNetwork()
        # print("Total Cost: "+str(network.calcTotalCost())+"\n")
        return (network.pathFlows[0], network.pathFlows[2], network.calcTotalCost())


    # otherwise we know that optimal is at most pushing 50% through top road and 50% through bottom
    else:
        for i in range(10):
            if i<demand/2:
                network.addOneToPath(network.paths[0])
            else:
                network.addOneToPath(network.paths[1])
        # display the new state of the network:
        # network.displayNetwork()
        # print("Total Cost: "+str(network.calcTotalCost())+"\n")
        return network.calcTotalCost()


    
        
main()