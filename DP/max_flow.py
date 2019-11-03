import numpy as np


def build_increasing_path(network_out, network_in, n, arc_flows):
    Ic, It, i, t = 0, 0, 0, n-1
    L = set([0])
    g, p = [''] * n, [-1] * n
    while True:
        straight_arcs = [j for j, d in network_out[i].items() if j not in L and arc_flows[i][j] < d]
        for j in straight_arcs:
            g[j] = i
            It += 1
            p[j] = It
            L.add(j)

        reverse_arcs = [j for j, d in network_in[i].items() if j not in L and arc_flows[j][i] > 0]
        for j in reverse_arcs:
            g[j] = -i
            It += 1
            p[j] = It
            L.add(j)

        if t in L:
            break

        Ic += 1

        try:
            i = p.index(Ic)
        except ValueError:
            print('Current plan is optimal')
            return False, None, None

    return True, g, L


def build_path(network, n, g, arc_flows):
    arcs = []

    i = n-1
    alpha = np.Inf
    while True:
        q = g[i]
        if q == 0:
            arcs.append((q, i, True))
            break

        if q > 0:
            delta = network[q][i] - arc_flows[q][i]
            arcs.append((q, i, True))
        else:
            q = -q
            delta = arc_flows[i][q]
            arcs.append((i, q, False))

        if delta < alpha:
            alpha = delta

        i = q

    return alpha, arcs


def update_arcs_flow(arcs_flow, increasing_arcs, alpha):
    for i, j, straight in increasing_arcs:
        if straight:
            arcs_flow[i][j] += alpha
        else:
            arcs_flow[i][j] -= alpha

    return arcs_flow


def find_max_flow(network_out, arc_flows=None):
    n = len(network_out)

    network_in = [{} for _ in range(n)]
    for i in range(n):
        for j, d in network_out[i].items():
            network_in[j][i] = d

    if arc_flows is None:
        arc_flows = [dict.fromkeys(network_out[i].keys(), 0) for i in range(n)]

    while True:
        can_increase, g, L = build_increasing_path(network_out, network_in, n, arc_flows)
        if can_increase:
            alpha, increasing_path = build_path(network_out, n, g, arc_flows)
            arc_flows = update_arcs_flow(arc_flows, increasing_path, alpha)
        else:
            break

    return arc_flows


def main():
    n = 7
    network_out = [
        {1: 4, 3: 9},
        {3: 2, 4: 4},
        {4: 1, 5: 10},
        {2: 1, 5: 6},
        {6: 2, 5: 1},
        {6: 9},
        {}
    ]
    print('len', len(network_out))

    network_in = [{} for _ in range(n)]
    for i in range(n):
        for j, d in network_out[i].items():
            network_in[j][i] = d

    # print(network_out)
    # print(network_in)

    arc_flows = [
        {1: 4, 3: 5},
        {3: 2, 4: 2},
        {4: 1, 5: 0},
        {2: 1, 5: 6},
        {6: 2, 5: 1},
        {6: 7},
        {}
    ]
    print(arc_flows)

    #arc_flows = [dict.fromkeys(network_out[i].keys(), 0) for i in range(n)]



    g = build_increasing_path(network_out, network_in, n, arc_flows)
    #print(res)

    alpha, path = build_path(network_out, n, g, arc_flows)
    # print(alpha)
    # print(path)

    arcs_flow = update_arcs_flow(arc_flows, path, alpha)
    # print(arc_flows)
    print(arcs_flow)


if __name__ == '__main__':
    main()