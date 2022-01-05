import random

from math import inf


def NNH(xy, dist):
    """"
    Nearest Neighbourhood Heuristic for the TSP problem
    Starts with a random city, and picks a city from unvisited cities with the closest city to that city
    :param dist is given upfront to save computational time
    """

    C = xy.shape[0]
    vis = []
    unvis = [i for i in range(C)]
    c = random.choice(unvis)
    vis.append(c)
    unvis.remove(c)

    # pick the city with the smallest distance to n, cannot be n itself or a city that was already visited
    while len(unvis) > 0:
        min_dist = min(d for ind, d in enumerate(dist[c, :]) if ind != c and ind not in vis)
        c = list(dist[c, :]).index(min_dist)  # TODO ASSUMES THAT NO TWO CITIES HAVE THE SAME DISTANCE FROM N
        vis.append(c)
        unvis.remove(c)
    return vis


def NIH(xy, dist):
    """"
    Nearest Insertion Heuristic for the TSP problem
    Starts with two random cities, then repeatedly finds the city not already in the tour that is closest to any city in
    the tour, and places it between whichever two cities would cause the resulting tour to be the shortest possible.
    """
    C = xy.shape[0]
    vis = []
    unvis = [i for i in range(C)]
    cc = random.sample(unvis, 2)
    vis.extend(cc)
    unvis.remove(cc[0])
    unvis.remove(cc[1])

    while len(unvis) > 0:
        min_dist = inf
        nw = unvis[0]  # just an initialization
        for c1 in vis:
            for c2 in unvis:
                if dist[c1, c2] < min_dist:
                    min_dist = dist[c1, c2]
                    nw = c2
        # nw is the closest point to all points in the tour
        # Now this point needs to be inserted in between any two points from the tour so that the increase is minimal
        min_incr = inf
        for c1, c2 in zip(vis[:-1], vis[1:]):
            # cost increase is cost of path c1->nw->c2 minus cost of c1-> c2
            incr = dist[c1, nw] + dist[nw, c2] - dist[c1, c2]
            if incr < min_incr:
                min_incr = incr
                nw1 = c1
                nw2 = nw
        # Now insert nw2 in the vis list between nw1 and nw3 in the list + remove from unvis list
        idx = vis.index(nw1)
        vis.insert(idx + 1, nw2)
        unvis.remove(nw2)
    return vis


def RIH(xy, dist):
    """"
    Random Insertion Heuristic
    Similar to NIH, but at each step, it randomly (!) selects an unvisited city and inserts it inbetween two nodes such
    that the cost increase is minimal
    """
    C = xy.shape[0]
    vis = []
    unvis = [i for i in range(C)]
    cc = random.sample(unvis, 2)
    vis.extend(cc)
    unvis.remove(cc[0])
    unvis.remove(cc[1])
    while len(unvis) > 0:
        nw = random.choice(unvis)
        min_cost = inf
        for c1, c2 in zip(vis[:-1], vis[1:]):
            # cost increase is cost of path c1->nw->c2 minus cost of c1-> c2
            incr = dist[c1, nw] + dist[nw, c2] - dist[c1, c2]
            if incr < min_cost:
                min_cost = incr
                nw1 = c1
                nw2 = nw
        # Now insert nw2 in the vis list between nw1 and nw3 in the list + remove from unvis list
        idx = vis.index(nw1)
        vis.insert(idx + 1, nw2)
        unvis.remove(nw2)
    return vis
