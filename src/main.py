# -*- coding: utf-8 -*-
#
# Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>
#
import time
from model import AntColony
from sys import argv

__EXPECTED_ARGS = 4

def __experiment(numCities, numAnts, maxTime):
    print "Beginning Ant Colony Optimization demo\n"
    print "Number of cities: %d" %(numCities)
    print "Number of ants: %d" %(numAnts)
    print "Maximum time: %d\n" %(maxTime)
    colony = AntColony(numCities, numAnts)
    colony.show_properties()

    t1 = time.time()

    print "Initializing dummy graph distances"
    dists = colony.make_graph_distances()

    print "Initializing ants at random trails"
    ants = colony.init_ants(numAnts)
    colony.show_ants(ants, dists)

    bestTrail = colony.best_trail(ants, dists)
    bestLength = colony.length(bestTrail, dists)

    print "Initializing pheromone on trails"
    pheromones = colony.init_pheromones()

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
            print "%3d\t%d\t%d" %(bestLength, i, gain)

    print "\nBest trail found:"
    colony.display_trail(bestTrail)

    print "Ant Colony Optimization demo finished!"
    print "Elapsed Time: %.2f min(s)" %((time.time() - t1) / 60)


if __name__ == "__main__":
    if not(len(argv) == __EXPECTED_ARGS):
        print "Usage: python ./main.py numCities numAnts maxTime"

    else:
        PARAMS = (int(argv[1]), int(argv[2]), int(argv[3]))
        numCities, numAnts, maxTime = PARAMS

        __experiment(numCities, numAnts, maxTime)

