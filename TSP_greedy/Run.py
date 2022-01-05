import os
from math import sqrt, inf
from numpy import genfromtxt
from TSP_greedy import NNH, NIH, RIH
from TSP_IG import IG
from Helper import compute_dist, compute_cost, show_route

# Change the working directory to the directory in which this file resides
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# For each city, the x and y coordinates
xy = genfromtxt('att48.csv', delimiter=',')
dist = compute_dist(xy)

# Experiments ----------------------------------------------------------------------------------------------------------
best_cost_nih = inf
best_cost_rih = inf
best_cost_nnh = inf
best_cost_ig = inf

best_vis_nih = []
best_vis_rih = []
best_vis_nnh = []
best_vis_ig = []

while best_cost_ig > 33524: # ~33,523+ is the optimal solution
    vis_nih = NIH(xy, dist)
    vis_rih = RIH(xy, dist)
    vis_nnh = NNH(xy, dist)
    vis_ig = IG(xy, dist, 20, 100) # delete 20 during the destruction step, 100 iterations in the IG algorithm
    cost_nih = compute_cost(dist, vis_nih)
    cost_rih = compute_cost(dist, vis_rih)
    cost_nnh = compute_cost(dist, vis_nnh)
    cost_ig = compute_cost(dist, vis_ig)

    if cost_nih < best_cost_nih:
        best_cost_nih = cost_nih
        best_vis_nih = vis_nih

    if cost_rih < best_cost_rih:
        best_cost_rih = cost_rih
        best_vis_rih = vis_rih

    if cost_nnh < best_cost_nnh:
        best_cost_nnh = cost_nnh
        best_vis_nnh = vis_nnh

    if cost_ig < best_cost_ig:
        best_cost_ig = cost_ig
        best_vis_ig = vis_ig
        print('Best cost for the IG algorithm', best_cost_ig)

print('Best costs: ')
print(' NIH = ', best_cost_nih)
print(' RIH = ', best_cost_rih)
print(' NNH = ', best_cost_nnh)
print(' IG =  ', best_cost_ig)

show_route(xy, best_vis_ig, dist)
