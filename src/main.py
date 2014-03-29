# -*- coding: utf-8 -*-
#
# Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>
#
_alpha = 3
_beta = 2
_rho = 0.01
_Q = 2.0

def init_pheromones(numCities):
    pass

def update_ants(ants, pheromones, dists):
    pass

def update_pheromones(pheromones, ants, dists):
    pass

def best_trail(ants, dists):
    pass

def length(bestTrail, dists):
    pass

def init_ants(numAnts, numCities):
    pass

def show_ants(ants, dists):
    pass

def make_graph_distances(numCities):
    pass

if __name__ == "__main__":
    print "Beginning Ant Colony Optimization demo\n"

    numCities = 60
    numAnts = 4
    maxTime = 1000

    print "Number of cities: %d" %(numCities)
    print "Number of ants: %d" %(numAnts)
    print "Maximum time: %d\n" %(maxTime)

    print "Pheromone influence (Alpha): %d" %(_alpha)
    print "Local node influence (Beta): %d" %(_beta)
    print "Pheromone evaporation coef (Rho): %.2f" %(_rho)
    print "Pheromone deposit factor (Q): %.2f\n" %(_Q)

    print "Initializing dummy graph distances"
    dists = make_graph_distances(numCities)

    print "Initializing ants at random trails"
    ants = init_ants(numAnts, numCities)
    show_ants(ants, dists)

    bestTrail = best_trail(ants, dists)
    bestLength = length(bestTrail, dists)

    print "Best initial trail length: %.2f" %(bestLength)
    print "Initializing  pheromone on trails"
    pheromones = init_pheromones(numCities)

    print "Starting..."
    for i in range(maxTime):
        update_ants(ants, pheromones, dists)
        update_pheromones(pheromones, ants, dists)
        currentBestTrail = bestTrail(ants, dists)
        currentBestLength = bestLength(currentBestTrail, dists)
        if currentBestLength < bestLength:
            bestLength = currentBestLength
            bestTrail = currentBestTrail
            print "New best length of %.2f at time %d" %(bestLength, i)

    print "Best trail found:"
    print bestTrail
    print "Best length: %.2f\n" %(bestLength)

    print "Ant Colony Optimization demo done"
