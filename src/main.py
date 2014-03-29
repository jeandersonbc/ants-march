# -*- coding: utf-8 -*-
#
# Demo of Ant Colony Optimization (ACO) solving a Traveling Salesman Problem (TSP).
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>
#
import random

_alpha = 3
_beta = 2
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
    for i in range(len(probs)):
        if i == cityX or visited[i]:
            probs[i] = 0.0
        else:
            probs[i] = pow(pheromones[cityX][i], _alpha) \
                        * pow((1.0 / distance(cityX, i, dists)), _beta)
            if probs[i] < 0.0001:
                probs[i] = 0.0001
            elif probs[i] > (1.7976931348623157E+308 / (numCities * 100)):
                probs[i] = (1.7976931348623157E+308 / (numCities * 100))
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
    pass

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
        currentBestTrail = best_trail(ants, dists)
        currentBestLength = length(currentBestTrail, dists)
        if currentBestLength < bestLength:
            bestLength = currentBestLength
            bestTrail = currentBestTrail
            print "New best length of %.2f at time %d" %(bestLength, i)

    print "Best trail found:"
    display_trail(bestTrail)
    print "Best length: %.2f\n" %(bestLength)

    print "Ant Colony Optimization demo finished!"
