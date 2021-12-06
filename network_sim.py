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

    parallel_edge_costs = list(range(0,50))
    parallel_edge_costs = [c/100 for c in parallel_edge_costs]

    maxOptimalCosts = []
    totalCostsParallel = []


    for c in parallel_edge_costs:
        maxOptimalCosts.append(simulate_parallel(2000))

        normalRouteFlow, parallelRouteFlow, parallelCost = simulate_parallel(2000,True,c)
        routeAlongNormal.append(normalRouteFlow)
        routeAlongParallel.append(parallelRouteFlow)
        totalCostsParallel.append(parallelCost)
    
    plot2(0,"Flow Along Parallel Edge vs. Normal Routes", "Parallel Edge Cost (beta*x)", "Flow Along Path",parallel_edge_costs,routeAlongParallel,parallel_edge_costs,routeAlongNormal,"Flow along parallel edge","Flow for each normal routes")
    plot2(1,"Total Cost With Parallel Road vs. Max Optimal Cost","Parallel Edge Cost (beta*x)","Cost",parallel_edge_costs,totalCostsParallel,parallel_edge_costs,maxOptimalCosts,"Cost with parallel edge","Max optimal cost")

    
    # compare optimal cost with series road
    routeAlongNormal = []
    routeAlongSeries = []

    series_edge_costs = list(range(0,20))
    series_edge_costs = [c/100 for c in parallel_edge_costs]

    optimalCosts = []
    totalCostsSeries = []

    for c in series_edge_costs:
        optimalCosts.append(simulate_series(2000,False,c))

        normalRouteFlow, seriesRouteFlow, seriesCost = simulate_series(2000,True,c)
        routeAlongNormal.append(normalRouteFlow)
        routeAlongSeries.append(seriesRouteFlow)
        totalCostsSeries.append(seriesCost)
    
    plot2(2,"Flow Series Edge vs. Along Normal Routes", "Series Edge Cost (beta*x)", "Flow Along Path",series_edge_costs,routeAlongSeries,series_edge_costs,routeAlongNormal,"Flow along series edge","Flow for each normal routes")
    plot2(3,"Total Cost With Series Road vs. Optimal Cost","Series Edge Cost (beta*x)","Cost",series_edge_costs,totalCostsSeries,series_edge_costs,optimalCosts,"Cost with series edge","Optimal cost")


    plt.show()





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

    # run the simulation of parallel road
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
        for i in range(num_agents):
            if i<num_agents/2:
                network.addOneToPath(network.paths[0])
            else:
                network.addOneToPath(network.paths[1])
        # display the new state of the network:
        # network.displayNetwork()
        # print("Total Cost: "+str(network.calcTotalCost())+"\n")
        return network.calcTotalCost()


def simulate_series(demand,series_road=False,series_edge_cost=0):
    max_iters = 20 # should turn into command line argument
    num_agents = demand

    network = Network()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')

    network.addEdge(network.source, a, 0, 0.01) # x/100
    network.addEdge(network.source, b, 15, 0) # 15
    network.addEdge(a,c, 15, 0) # 15
    network.addEdge(b,c, 0, 0.01) # x/100 
    network.addEdge(c,network.sink,0,series_edge_cost) # cost*x

    # test validity of network and display
    #network.checkNetwork(debug=True)

    # make sure to generate paths from source to sink
    network.getAllPaths(network.source,network.sink)


    # initialize agents on this network
    agents = []
    for i in range(num_agents):
        agents.append(Agent(network,id=str(i)))

    # run the simulation of series road
    if series_road:
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
        return (network.flows[(network.source,a)],network.flows[(c,network.sink)],network.calcTotalCost())



    # otherwise we know that optimal is at most pushing 50% through top road and 50% through bottom
    else:
        for i in range(num_agents):
            if i<num_agents/2:
                network.addOneToPath(network.paths[0])
            else:
                network.addOneToPath(network.paths[1])
        # display the new state of the network:
        network.displayNetwork()
        # print("Total Cost: "+str(network.calcTotalCost())+"\n")
        # return network.calcTotalCost()
    
        
main()