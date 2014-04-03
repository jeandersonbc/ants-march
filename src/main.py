# -*- coding: utf-8 -*-
"""
Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).

Usage: python ./main.py numCities numAnts maxTime

Contributors:
    Jeanderson Candido <http://jeandersonbc.github.io>
"""
import time
from model import AntColony
from sys import argv

__EXTRA_ARGS = 1
__MIN_ARGS = 4

def __experiment(numCities, numAnts, maxTime, detailsEnabled=False):
    if detailsEnabled:
        print "Beginning Ant Colony Optimization demo\n"
        print "Number of cities: %d" %(numCities)
        print "Number of ants: %d" %(numAnts)
        print "Maximum time: %d\n" %(maxTime)
    colony = AntColony(numCities, numAnts)
    if detailsEnabled:
        colony.show_properties()

    t1 = time.time()

    if detailsEnabled:
        print "Initializing dummy graph distances"
    dists = colony.make_graph_distances()

    ants = colony.init_ants()
    if detailsEnabled:
        print "Initializing ants at random trails"
        colony.show_ants(ants, dists)

    bestTrail = colony.best_trail(ants, dists)
    bestLength = colony.length(bestTrail, dists)

    if detailsEnabled:
        print "Initializing pheromone on trails"
    pheromones = colony.init_pheromones()

    if detailsEnabled:
        print "Starting...\n"
        print "Length\tTime\tGain"
        print "----------------------"
        print "%3d\t-\t-" %(bestLength)

    for i in range(maxTime):
        colony.update_ants(ants, pheromones, dists)
        colony.update_pheromones(pheromones, ants, dists)
        currentBestTrail = colony.best_trail(ants, dists)
        currentBestLength = colony.length(currentBestTrail, dists)
        if currentBestLength < bestLength:
            gain = bestLength - currentBestLength
            bestLength = currentBestLength
            bestTrail = currentBestTrail
            if detailsEnabled:
                print "%3d\t%d\t%d" %(bestLength, i, gain)

    if detailsEnabled:
        print "\nBest trail found:"
        colony.display_trail(bestTrail)
        print "Ant Colony Optimization demo finished!"

    # length + time in seconds
    print "%d\t%.2f" %(bestLength, (time.time() - t1))


if __name__ == "__main__":
    if len(argv) <= __MIN_ARGS + __EXTRA_ARGS \
            and len(argv) >= __MIN_ARGS:

        PARAMS = (int(argv[1]), int(argv[2]), int(argv[3]))
        numCities, numAnts, maxTime = PARAMS
        showDetails = len(argv) == __MIN_ARGS + __EXTRA_ARGS

        __experiment(numCities, numAnts, maxTime, showDetails)

    else:
        print "Usage: python ./main.py numCities numAnts maxTime [details]"
        print "       details   -> Print details if specified (false by default)."
        print "       numCities -> Number of nodes in the graph."
        print "       numAnts   -> Population."
        print "       maxTime   -> Max number of iterations."

