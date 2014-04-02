ants.march
==========

This is a demo for the Ant Colony Optimization algorithm to solve the
Travelling Salesman Problem.

## Dependencies

Nothing but Python 2.x is all you need to run the demo:
Type ``python ./main.py`` to see its usage.

## Running the Experiment

If you are on Windows, there's an automation script located into ``experiment``.
Run ``run.ps1`` from the command line using Windows Powershell to execute the experiment.

## Problem

Given 60 cities (assume you can reach all the other 59 cities from your location),
how long would you take to find the best path to visit all cities? Are you really up
to compute all possibilities?

* ``(N-1)! / 2`` is a very large number. Even if we had a computer capable to compute ``10^60``
**possibilites** in a second, we still wouldn't be able to find an optimal solution. 

* Elegant algorithms are still better than powerful computers.
