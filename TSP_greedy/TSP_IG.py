import random
from math import inf
from others import compute_cost


def IG(xy, dist, L, I):
    """"
    RIH algorithm in an iterative greedy (IG) setting.
    The algorithm consists of the following phases:
    1) INIT: An initial tour is constructed using RIH
    2) DESTRUCTION: L nodes are removed at random from the tour
    3) CONSTRUCTION: the removed nodes are again added via RIH
    4) ACCEPTANCE: if the new solution is better than the old, keep it. Go back to 2) until the number of iterations
                   exceeds I
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
        # CONSTRUCTION: use RIH to build up a new solution again
        vis_new, unvis_new = RIH(dist, vis, unvis)
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

    # INIT (optional)
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
