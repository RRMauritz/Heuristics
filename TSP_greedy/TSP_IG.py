import random
from math import inf
from Helper import compute_cost
from typing import Callable


# Implementation of an iterated greedy algorithm

def IG(xy, dist, construct: Callable, L, I):
    """"
    Iterated Greedy (IG) algorithm
    The algorithm consists of the following phases:
    1) INIT: An initial tour is constructed using RIH
    2) DESTRUCTION: L nodes are removed at random from the tour
    3) CONSTRUCTION: the removed nodes are again added via a heuristic such as RIH, NIH, NNH
    4) ACCEPTANCE: if the new solution is better than the old, keep it. Go back to 2) until the number of iterations
                   exceeds I
    :parameter construct: function that is used to construct a full solution, e.g. RIH, NIH, NNH
    """

    C = xy.shape[0]
    vis = []
    unvis = [i for i in range(C)]

    # INIT -------------------------------------------------------------------------------------------------------------
    # Initial solution (note: vis describes the solution)
    i = 0
    vis_old, unvis_old = RIH(dist, vis, unvis)
    # LOOP -------------------------------------------------------------------------------------------------------------
    while i < I:
        # Make a copy of vis_old and unvis_old, the copies serve as intermediaries
        vis = vis_old.copy()
        unvis = unvis_old.copy()
        i = i + 1
        # DESTRUCTION: randomly remove l elements from the previous solution vis
        for _ in range(L):
            x = random.choice(vis)
            vis.remove(x)
            unvis.append(x)
        # CONSTRUCTION: use heuristics to build up a new solution again
        vis_new, unvis_new = construct(dist, vis, unvis)
        # ACCEPTANCE: if the new solution has improved, update the incumbent to the new solution, otherwise keep old
        if compute_cost(dist, vis_new) < compute_cost(dist, vis_old):
            vis_old = vis_new
            unvis_old = unvis_new
        else:
            pass

    return vis_old


def RIH(dist, vis, unvis):
    """"
    Random Insertion Heuristic
    Similar to NIH, but at each step, it randomly (!) selects an unvisited city and inserts it in between two nodes such
    that the cost increase is minimal.
    :param dist = the distance matrix for the nodes
    :param vis = the starting list of the tour, specified by the ordering
    :param unvis = the remaining cities that have not been visited yet
    """

    # Special case when vis is empty
    # If empty or 1 node, there are no nodes to in between which a new node can be inserted
    # Therefore it should be initialized so that there are two nodes at the start

    # INIT
    if len(vis) == 0:
        cc = random.sample(unvis, 2)
        vis.extend(cc)
        unvis.remove(cc[0])
        unvis.remove(cc[1])
    elif len(vis) == 1:
        c = random.choice(unvis)
        vis.extend(c)
        unvis.remove(c)

    # LOOP
    while len(unvis) > 0:
        # pick a random node from the unvis list
        c = random.choice(unvis)
        min_cost = inf
        c_left = vis[0]  # init, will be possible overwritten below
        # INSERTION
        for c1, c2 in zip(vis[:-1], vis[1:]):
            # cost increase is cost of path c1->nw->c2 minus cost of c1-> c2
            incr = dist[c1, c] + dist[c, c2] - dist[c1, c2]
            if incr < min_cost:
                min_cost = incr
                c_left = c1
        # Now insert nw2 in the vis list between nw1 and nw3 in the list + remove from unvis list
        idx = vis.index(c_left)
        vis.insert(idx + 1, c)
        unvis.remove(c)
    return vis, unvis


def NIH(dist, vis, unvis):
    """"
    Nearest Insertion Heuristic for the TSP problem
    """

    # INIT
    if len(vis) == 0:
        cc = random.sample(unvis, 2)
        vis.extend(cc)
        unvis.remove(cc[0])
        unvis.remove(cc[1])
    elif len(vis) == 1:
        c = random.choice(unvis)
        vis.extend(c)
        unvis.remove(c)

    while len(unvis) > 0:
        min_dist = inf
        c = unvis[0]  # just an initialization, will probably be overwritten below
        # find the closest point (c) to all points that are currently in the tour
        for c1 in vis:
            for c2 in unvis:
                if dist[c1, c2] < min_dist:
                    min_dist = dist[c1, c2]
                    c = c2

        # Now this point needs to be inserted in between any two points from the tour so that the increase is minimal
        min_cost = inf
        c_left = vis[0]  # init, will be possible overwritten below
        # INSERTION
        for c1, c2 in zip(vis[:-1], vis[1:]):
            # cost increase is cost of path c1->nw->c2 minus cost of c1-> c2
            incr = dist[c1, c] + dist[c, c2] - dist[c1, c2]
            if incr < min_cost:
                min_cost = incr
                c_left = c1
        # Now insert nw2 in the vis list between nw1 and nw3 in the list + remove from unvis list
        idx = vis.index(c_left)
        vis.insert(idx + 1, c)
        unvis.remove(c)
    return vis, unvis


def NNH(dist, vis, unvis):  # TODO: does not work yet in the IG setting! Goes (?) wrong at min_dist line
    """"
    Nearest Neighbourhood Heuristic for the TSP problem
    """

    if len(vis) == 0:
        c = random.choice(unvis)
        vis.append(c)
        unvis.remove(c)

    # Take as reference point the last added city in the tour
    c = vis[-1]

    while len(unvis) > 0:
        # Find the closest unvisited city to the last added city in the tour
        dist_unvis = [dist[c, i] for i in unvis]
        c_new = [x for _, x in sorted(zip(dist_unvis, unvis))][0]
        vis.append(c_new)
        unvis.remove(c_new)
    return vis, unvis
