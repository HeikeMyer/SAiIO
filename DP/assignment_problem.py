import numpy as np
import max_flow as mf


def reduce(c, n):
    for i in range(n):
        min_i = min(c[i])
        for j in range(n):
            c[i][j] -= min_i

    for j in range(n):
        min_j = min(c[:, j])
        for i in range(n):
            c[i][j] -= min_j

    return c


def build_network(c, n, network=None, arcs=None):
    if network is None:
        network_size = 2*n + 2
        network = [{} for _ in range(network_size)]
        arcs = set({})

        for i in range(1, n+1):
            network[0][i] = 1

        for i in range(n+1, network_size-1):
            network[i][network_size-1] = 1

    for i in range(n):
        for j in range(n):
            if c[i][j] == 0:
                arc = (i + 1, n + j + 1)
                if arc not in arcs:
                    arcs.add(arc)
                    network[arc[0]][arc[1]] = 2

    return network, arcs


def build_optimal_plan(c, n, arc_flows):
    opt_plan = []
    for i in range(n):
        for node, flow in arc_flows[i + 1].items():
            if flow == 1:
                opt_plan.append((i, node-n-1))

    min_cost = sum([c[i][j] for i, j in opt_plan])

    x = np.zeros((n, n))
    for i, j in opt_plan:
        x[i][j] = 1

    return opt_plan, min_cost, x


def solve(costs, n):
    c = np.copy(costs)

    c = reduce(c, n)

    network = None
    arcs = None
    while True:
        network, arcs = build_network(c, n, network, arcs)
        arc_flows, max_flow, L = mf.find_max_flow(network, arc_flows=None)

        if max_flow == n:
            return build_optimal_plan(costs, n, arc_flows)
        else:
            N1 = [i-1 for i in L if 1 <= i <= n]
            N2 = [i-n-1 for i in L if n+1 <= i <= 2*n]
            N2n = set(range(n)) - set(N2)

            alpha = np.Inf
            for i in N1:
                for j in N2n:
                    if c[i][j] < alpha:
                        alpha = c[i][j]

            for i in N1:
                for j in range(n):
                    c[i][j] -= alpha

            for j in N2:
                for i in range(n):
                    c[i][j] += alpha


def main():
    n = 4
    c = np.array([
        [2, 10, 9, 7],
        [15, 4, 14, 8],
        [13, 14, 16, 11],
        [4, 15, 13, 19]
    ])

    opt_plan, min_cost, x = solve(c, n)
    print(f'Optimal plan: {opt_plan}\nMin cost: {min_cost}\nX=\n{x}')


if __name__ == '__main__':
    main()
