# -*- coding: utf-8 -*-
#
# Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>
#
import random
import time

# Influence of pheromone on direction (alpha) and of
# adjacent node distances (beta)
_alpha = 3
_beta = 2

# Pheromone increase (rho) e decrease (Q) factors
_rho = 0.01
_Q = 2.0

def display_trail(trail):
    for i in range(len(trail)):
        if i % 20 == 0: print ""
        print "%3d" %trail[i],
    print "\n"

def move_probs(k, cityX, visited, pheromones, dists):
    numCities = len(pheromones)
    probs = [0.0 for i in range(numCities)]
    total = 0.0
    upperBoundFactor = 1.7976931348623157E+308 / (numCities * 100)
    lowerBoundFactor = 0.0001
    for i in range(len(probs)):
        if i == cityX or visited[i]:
            probs[i] = 0.0
        else:
            probs[i] = pow(pheromones[cityX][i], _alpha) \
                        * pow((1.0 / distance(cityX, i, dists)), _beta)
            if probs[i] < lowerBoundFactor:
                probs[i] = lowerBoundFactor
            elif probs[i] > upperBoundFactor:
                probs[i] = upperBoundFactor
        total += probs[i]

    return [(probs[i] / total) for i in range(numCities)]

def next_city(k, cityX, visited, pheromones, dists):
    probs = move_probs(k, cityX, visited, pheromones, dists)
    cumul = [0.0 for i in range(len(probs) + 1)]
    for i in range(len(probs)):
        cumul[i+1] = cumul[i] + probs[i]

    p = random.random() 
    for i in range(len(cumul)-1):
        if (p >= cumul[i] and p < cumul[i+1]):
            return i

def build_trail(k, start, pheromones, dists):
    numCities = len(pheromones)
    trail = [0 for i in range(numCities)]
    visited = [False for i in range(numCities)]

    trail[0] = start
    visited[start] = True
    for i in range(numCities-1):
        cityX = trail[i]
        nextCity = next_city(k, cityX, visited, pheromones, dists)
        trail[i+1] = nextCity
        visited[nextCity] = True

    return trail

def init_pheromones(numCities):
    """ Initializes a matrix representing the pheromones. """
    pheromones = [[0.0 for j in range(numCities)] for i in range(numCities)]
    for i in range(len(pheromones)):
        for j in range(len(pheromones)):
            pheromones[i][j] = 0.01

    return pheromones

def update_ants(ants, pheromones, dists):
    numCities = len(pheromones)
    for k in range(len(ants)):
        start = random.randint(0, numCities-1)
        newTrail = build_trail(k, start, pheromones, dists)
        ants[k] = newTrail

def update_pheromones(pheromones, ants, dists):
    for i in range(len(pheromones)):
        for j in range(i+1, len(pheromones[i])):
            for k in range(len(ants)):
                currLength = length(ants[k], dists)
                decrease = (1.0 - _rho) * pheromones[i][j]
                increase = 0.0
                if edge_in_trail(i, j, ants[k]):
                    increase = (_Q / currLength)
                pheromones[i][j] = decrease + increase
                if pheromones[i][j] < 0.001:
                    pheromones[i][j] = 0.001
                elif pheromones[i][j] > 100000.0:
                    pheromones[i][j] = 100000.0
                pheromones[j][i] = pheromones[i][j]

def edge_in_trail(cityX, cityY, trail):
    lastIndex = len(trail) - 1
    idx = trail.index(cityX)
    if (idx == 0 and trail[1] == cityY) \
            or (idx == 0 and trail[lastIndex] == cityY):
        return True

    elif idx == 0:
        return False

    elif (idx == lastIndex and trail[lastIndex - 1] == cityY) \
            or (idx == lastIndex and trail[0] == cityY):
        return True

    elif idx == lastIndex:
        return False

    elif trail[idx - 1] == cityY or trail[idx + 1] == cityY:
        return True

    return False

def best_trail(ants, dists):
    bestLength = length(ants[0], dists)
    idxBestLen = 0
    for k in range(1, len(ants)):
        otherLen = length(ants[k], dists)
        if otherLen < bestLength:
            bestLength = otherLen
            idxBestLen = k

    return ants[idxBestLen]

def distance(cityX, cityY, dists):
    return dists[cityX][cityY]

def length(trail, dists):
    result = 0.0
    for i in range(len(trail)-1):
        result += distance(trail[i], trail[i+1], dists)

    return result

def random_trail(start, numCities):
    trail = range(numCities)

    # Shuffle
    for i in range(numCities):
        r = random.randint(i, numCities-1)
        tmp = trail[r]
        trail[r] = trail[i]
        trail[i] = tmp

    # Start at 0
    idx = trail.index(start)
    tmp = trail[0]
    trail[0] = trail[idx]
    trail[idx] = tmp

    return trail

def init_ants(numAnts, numCities):
    ants = [[] for r in range(numAnts)]
    for k in range(numAnts):
        start = random.randint(0, numCities-1)
        ants[k] = random_trail(start, numCities)

    return ants

def show_ants(ants, dists):
    print ""
    for i in range(len(ants)):
        print i, ":[",
        for j in range(4):
            print "%3d" %ants[i][j],
        print "...",
        for j in range(len(ants[i])-4, len(ants[i])):
            print "%3d" %ants[i][j],
        print "] len =", length(ants[i], dists)
    print ""

def make_graph_distances(numCities):
    dists = [[] for r in range(numCities)]
    for i in range(len(dists)):
        dists[i] = [0 for k in range(numCities)]
    for i in range(len(dists)):
        for j in range(i+1, numCities):
            d = random.randint(1,8)
            dists[i][j] = d
            dists[j][i] = d

    return dists


def fact(n):
    """ Computes factorial.
    This is not used in the AOC problem.
    """
    if n == 1:
        return 1
    return n * fact(n - 1)

if __name__ == "__main__":
    t1 = time.time()
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
    print "Initializing pheromone on trails"
    pheromones = init_pheromones(numCities)

    print "Starting..."
    for i in range(maxTime):
        update_ants(ants, pheromones, dists)
        update_pheromones(pheromones, ants, dists)
        currentBestTrail = best_trail(ants, dists)
        currentBestLength = length(currentBestTrail, dists)
        if currentBestLength < bestLength:
            bestLength = currentBestLength
            bestTrail = currentBestTrail
            print "New best length of %3d at time %d" %(bestLength, i)

    print "Best trail found:"
    display_trail(bestTrail)
    print "Best length: %.2f\n" %(bestLength)

    print "Ant Colony Optimization demo finished!"
    print "Elapsed Time: %.2f min(s)" %((time.time() - t1) / 60)

    print ""
    print "Hypothetical super computer"
    print "1 * 10^60 possibilities per second"
    print "N = %d cities" %numCities
    tenTo60 = 1000000000000000000000000000000000000000000000000000000000000
    result = fact(numCities-1) >> 1
    print "(N-1)! / 2 = %d possibilities..." %(result)
    print "Elapsed time: %d Years!" %(result / tenTo60 / 30758400)
