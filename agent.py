from network import Network

class Agent:
    def __init__(self,network,id=''):
        self.id = id
        self.path = []
        self.cost = float('inf')
        self.network = network

    # find the path that would result in lowest cost and take it
    def setBestPath(self):

        # "reset" ourself to the source
        #   i.e. if we are currently on a path, take ourself off
        if len(self.path) > 0:
            self.network.subtractOneFromPath(self.path)

        best_path = self.network.paths[0]
        best_cost = float('inf')
        # find the best path to add self to
        for p in self.network.paths:
            self.network.addOneToPath(p) # simulate going along that path
            cost = self.network.getCostAlongPath(p)
            if  cost < best_cost:
                best_path = p
                best_cost = cost
            self.network.subtractOneFromPath(p)  # reset at the source again

        # now add ourselves to the best path
        self.network.addOneToPath(best_path)

        self.path = best_path
        self.cost = best_cost
    

    # set agent on best path and check if their path choice changed
    def updateAndCheckChanged(self,debug=False):
        old_path = self.path
        self.setBestPath()
        if old_path == self.path:
            return False
        return True
        