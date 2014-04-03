# -*- coding: utf-8 -*-
#
# Contributors:
#     Jeanderson Candido <http://jeandersonbc.github.io>
#
import random

class AntColony:

    def __init__(self):
        # Pheromone properties
        self.__alpha = 3
        self.__beta = 2
        self.__rho = 0.01
        self.__Q = 2.0

    def show_properties(self):
        print "Pheromone influence (Alpha): %d" %(self.__alpha)
        print "Local node influence (Beta): %d" %(self.__beta)
        print "Pheromone evaporation coef (Rho): %.2f" %(self.__rho)
        print "Pheromone deposit factor (Q): %.2f\n" %(self.__Q)

    def display_trail(self, trail):
        for i in range(len(trail)):
            if i % 20 == 0: print ""
            print "%3d" %trail[i],
        print "\n"

    def move_probs(self, k, cityX, visited, pheromones, dists):
        numCities = len(pheromones)
        probs = [0.0 for i in range(numCities)]
        total = 0.0
        upperBoundFactor = 1.7976931348623157E+308 / (numCities * 100)
        lowerBoundFactor = 0.0001
        for i in range(len(probs)):
            if i == cityX or visited[i]:
                probs[i] = 0.0
            else:
                probs[i] = pow(pheromones[cityX][i], self.__alpha) \
                            * pow((1.0 / self.distance(cityX, i, dists)), self.__beta)
                if probs[i] < lowerBoundFactor:
                    probs[i] = lowerBoundFactor
                elif probs[i] > upperBoundFactor:
                    probs[i] = upperBoundFactor
            total += probs[i]

        return [(probs[i] / total) for i in range(numCities)]

    def next_city(self, k, cityX, visited, pheromones, dists):
        probs = self.move_probs(k, cityX, visited, pheromones, dists)
        cumul = [0.0 for i in range(len(probs) + 1)]
        for i in range(len(probs)):
            cumul[i+1] = cumul[i] + probs[i]

        p = random.random() 
        for i in range(len(cumul)-1):
            if (p >= cumul[i] and p < cumul[i+1]):
                return i

    def build_trail(self, k, start, pheromones, dists):
        numCities = len(pheromones)
        trail = [0 for i in range(numCities)]
        visited = [False for i in range(numCities)]

        trail[0] = start
        visited[start] = True
        for i in range(numCities-1):
            cityX = trail[i]
            nextCity = self.next_city(k, cityX, visited, pheromones, dists)
            trail[i+1] = nextCity
            visited[nextCity] = True

        return trail

    def init_pheromones(self, numCities):
        """ Initializes a matrix representing the pheromones. """
        pheromones = [[0.0 for j in range(numCities)] for i in range(numCities)]
        for i in range(len(pheromones)):
            for j in range(len(pheromones)):
                pheromones[i][j] = 0.01

        return pheromones

    def update_ants(self, ants, pheromones, dists):
        numCities = len(pheromones)
        for k in range(len(ants)):
            start = random.randint(0, numCities-1)
            newTrail = self.build_trail(k, start, pheromones, dists)
            ants[k] = newTrail

    def update_pheromones(self, pheromones, ants, dists):
        for i in range(len(pheromones)):
            for j in range(i+1, len(pheromones[i])):
                for k in range(len(ants)):
                    currLength = self.length(ants[k], dists)
                    decrease = (1.0 - self.__rho) * pheromones[i][j]
                    increase = 0.0
                    if self.edge_in_trail(i, j, ants[k]):
                        increase = (self.__Q / currLength)
                    pheromones[i][j] = decrease + increase
                    if pheromones[i][j] < 0.001:
                        pheromones[i][j] = 0.001
                    elif pheromones[i][j] > 100000.0:
                        pheromones[i][j] = 100000.0
                    pheromones[j][i] = pheromones[i][j]

    def edge_in_trail(self, cityX, cityY, trail):
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

    def best_trail(self, ants, dists):
        bestLength = self.length(ants[0], dists)
        idxBestLen = 0
        for k in range(1, len(ants)):
            otherLen = self.length(ants[k], dists)
            if otherLen < bestLength:
                bestLength = otherLen
                idxBestLen = k

        return ants[idxBestLen]

    def distance(self, cityX, cityY, dists):
        return dists[cityX][cityY]

    def length(self, trail, dists):
        result = 0.0
        for i in range(len(trail)-1):
            result += self.distance(trail[i], trail[i+1], dists)

        return result

    def random_trail(self, start, numCities):
        trail = range(numCities)

        # Shuffle
        for i in range(numCities):
            r = random.randint(i, numCities-1)
            trail[r], trail[i] = trail[i], trail[r]

        # Start at 0
        idx = trail.index(start)
        trail[idx], trail[0] = trail[0], trail[idx]

        return trail

    def init_ants(self, numAnts, numCities):
        ants = [[] for r in range(numAnts)]
        for k in range(numAnts):
            start = random.randint(0, numCities-1)
            ants[k] = self.random_trail(start, numCities)

        return ants

    def show_ants(self, ants, dists):
        print ""
        for i in range(len(ants)):
            print i, ":[",
            for j in range(4):
                print "%3d" %ants[i][j],
            print "...",
            for j in range(len(ants[i])-4, len(ants[i])):
                print "%3d" %ants[i][j],
            print "] len =", self.length(ants[i], dists)
        print ""

    def make_graph_distances(self, numCities, max_dist=8):
        dists = [[] for r in range(numCities)]
        for i in range(len(dists)):
            dists[i] = [0 for k in range(numCities)]
        for i in range(len(dists)):
            for j in range(i+1, numCities):
                d = random.randint(1, max_dist)
                dists[i][j] = dists[j][i] = d

        return dists
