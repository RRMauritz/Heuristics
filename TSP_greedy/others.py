import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


def compute_cost(dist, vis):
    cost = 0
    for c1, c2 in zip(vis[:-1], vis[1:]):
        cost += dist[c1, c2]
    # also add cost for closing the loop (first and last visited node)
    cost += dist[vis[0], vis[-1]]
    return cost


def compute_dist(xy):
    C = xy.shape[0]
    # Create a distance matrix for all city pairs based on the euclidean distance metric -> yields a symmetric matrix
    dist = np.zeros((C, C))
    for i in range(C):
        for j in range(C):
            dist[i, j] = sqrt((xy[j, 0] - xy[i, 0]) ** 2 + (xy[j, 1] - xy[i, 1]) ** 2)
    return dist


def show_route(xy, vis, dist):
    for c1, c2 in zip(vis[:-1], vis[1:]):
        # plot() needs the x coordinates and y coordinates in a separate list
        plt.plot([xy[c1, 0], xy[c2, 0]], [xy[c1, 1], xy[c2, 1]], 'ro-')
    c1 = vis[0]
    c2 = vis[-1]
    plt.plot([xy[c1, 0], xy[c2, 0]], [xy[c1, 1], xy[c2, 1]], 'bo-')
    for c in vis:
        plt.text(xy[c, 0], xy[c, 1], str(c))

    total_cost = compute_cost(dist, vis)
    plt.title('Total cost =' + str(int(total_cost)))
    plt.axis('off')
    plt.show()
