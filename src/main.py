# -*- coding: utf-8 -*-
"""
Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).

Run "python main.py" to see its usage.

Contributors:
    Jeanderson Candido <http://jeandersonbc.github.io>
"""
import time
from model import AntColony
from sys import argv

__EXTRA_ARGS = 1
__MIN_ARGS = 5

def __experiment(expId, numCities, numAnts, maxTime, detailsEnabled=False):
    colony = AntColony(numCities, numAnts)
    if detailsEnabled:
        colony.show_properties()
        print "Initializing dummy graph distances"

    dists = colony.make_graph_distances()
    ants = colony.init_ants()
    if detailsEnabled:
        print "Initializing ants at random trails"
        colony.show_ants(ants, dists)

    bestTrail = colony.best_trail(ants, dists)
    bestLength = colony.length(bestTrail, dists)
    pheromones = colony.init_pheromones()

    t1 = time.time()
    print "Exp #,Population,Nodes,Best Length,Iteration,Gain,Elapsed Time"
    print "%d,%d,%d,%d,%d,%d,%.3f" %(expId,numAnts,numCities,bestLength,0,0,0)
    for i in range(maxTime):
        colony.update_ants(ants, pheromones, dists)
        colony.update_pheromones(pheromones, ants, dists)
        currentBestTrail = colony.best_trail(ants, dists)
        currentBestLength = colony.length(currentBestTrail, dists)
        if currentBestLength < bestLength:
            gain = bestLength - currentBestLength
            bestLength = currentBestLength
            bestTrail = currentBestTrail
            t2 = time.time()

            print "%d,%d,%d,%d,%d,%d,%.3f" \
               %(expId,numAnts,numCities,bestLength,i,gain,t2-t1)

            t1 = time.time()

    if detailsEnabled:
        print "\nBest trail found:"
        colony.display_trail(bestTrail)
        print "Ant Colony Optimization demo finished!"

if __name__ == "__main__":
    if len(argv) <= __MIN_ARGS + __EXTRA_ARGS \
            and len(argv) >= __MIN_ARGS:

        PARAMS = int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4])
        expId, numCities, numAnts, maxTime = PARAMS
        showDetails = len(argv) == __MIN_ARGS + __EXTRA_ARGS

        __experiment(expId, numCities, numAnts, maxTime, showDetails)

    else:
        print "Usage: python ./main.py expId numCities numAnts maxTime [details]"
        print "       expId     -> Experiment Id"
        print "       details   -> Print details if specified (false by default)."
        print "       numCities -> Number of nodes in the graph."
        print "       numAnts   -> Population."
        print "       maxTime   -> Max number of iterations."

