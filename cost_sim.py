from network import Network
from network import Vertex
from agent import Agent
import matplotlib.pyplot as plt
import numpy as np

# simulate agents finding equilibrium on a network
def main():
    route1Flow  = []
    route3Flow = []
    totalCostWithHighway = []
    totalCostWithoutHighway = []
    totalCostWithHighwayFixedDemand = []
    optimalCost = []
    highwayCostAtConvergence = []
   
    highwayCost = list(range(1, 21))
    demand = list(range(1, 601))

    for i in range(1, 1001):
        # Record Optimal cost for different demands
        flow1_, flow3_, cost_ = run_simulation(i, False)
        totalCostWithoutHighway.append(cost_)

        # Record Total Cost and Flow on Routes w Highway for different demands
        flow1, flow3, cost = run_simulation(i, True, 7.5)
        route1Flow.append(flow1)
        route3Flow.append(flow3)
        totalCostWithHighway.append(cost)
    
    # Convergence of total cost to optimal, can change hard coded demand 
    for i in highwayCost: 
        flow1_, flow3_, cost_ = run_simulation(50, True, i)
        totalCostWithHighwayFixedDemand.append(cost_)
        flow1, flow3, cost = run_simulation(50)
        optimalCost.append(cost)

    # For a particular demand value, at what highway cost does the total cost of the 5-link network
    # converge with the optimal cost 

    for d in demand:
        seen = False
        for i in highwayCost:
            flow_1, flow_3, cost_ = run_simulation(d, True, i)
            flow1, flow3, cost = run_simulation(d)
            if cost == cost_ and not seen:
                highwayCostAtConvergence.append(i)
                seen = True

    
    x = list(range(1, 1001))
    plot2(0, "Flow on Different Paths for 5-Link Network", "Demand", "Flow On Path", x, route1Flow, x, route3Flow, "Flow on routes 1 and 2", "Flow on route 3")
    plot2(1, "Total Cost with and without Highway", "Demand", "Total Cost", x, totalCostWithHighway, x, totalCostWithoutHighway, "Total cost with highway", "Total cost without highway")
    plot2(2, "Total cost with and without highway", "Highway Cost", "Total Cost", highwayCost, totalCostWithHighwayFixedDemand, highwayCost, optimalCost, "Total cost of 5-link network for demand = 50", "Optimal cost for demand = 50")
    plot(3, "Highway cost and Convergence towards Optimal cost", "Demand", "Cost of Highway", demand, highwayCostAtConvergence, "Cost of Highway where Total cost of 5-link first converges with Optimal cost")
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

def run_simulation(demand, highway = False, highwayCost = 7.5):
    max_iters = 20 # should turn into command line argument
    num_agents = demand

    network = Network()
    a = Vertex('a')
    b = Vertex('b')

    network.addEdge(network.source, a, 0, 0.01) # 
    network.addEdge(network.source, b, 15, 0) # 
    network.addEdge(a,network.sink, 15, 0) # 
    network.addEdge(b,network.sink, 0, 0.01) # 
    if highway:
        network.addEdge(a,b,highwayCost,0) # cost 0

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