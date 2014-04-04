ants.march
==========

This is a demo for the Ant Colony Optimization algorithm to solve the
Travelling Salesman Problem.

### Dependencies

Nothing but Python 2.x is all you need to run the demo:
Type ``python ./main.py`` to see its usage.

### Problem

Given 60 cities (assume you can reach all the other 59 cities from your location),
how long would you take to find the best path to visit all cities? Are you really up
to compute all possibilities?

* ``(N-1)! / 2`` is a very large number. Even if we had a computer capable to compute **10^60
possibilites in a second**, we still wouldn't be able to find an optimal solution. 

### The Experiment

There is an automated experiment into ``experiment`` to study the behavior of our implementation
of the Ant Colony Optimization algorithm. We define 2 factors (i.e. population size and number of
nodes in the graph) to analyze how they are related to the length of the sub-optimal solution and
the whole execution. We repeat this experiment 5 times and log files have the following standard:
``population-nodes-repetition.txt``. For instance, ``1-10-2.txt`` means this was executed with 1
ant, 10 nodes, and it was the 2nd repetition.
