import os

import numpy as np
import tsplib95
from TSP_IG import *
from Helper import compute_dist, compute_cost, show_route

# Change the working directory to the directory in which this file resides
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) + '\Data'
os.chdir(dname)

# Load a tsp problem
# Source: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/
problem = tsplib95.load('xqg237.tsp')

# For each city, store the xy coordinates in a np array
C = len(problem.node_coords.keys())
xy = np.zeros((C, 2))

c = 0
for city in problem.node_coords:
    xy[c, :] = problem.node_coords[city]
    c += 1

dist = compute_dist(xy)

vis = IG(xy, dist, RIH, 60, 100)
show_route(xy, vis, dist)
