import numpy as np
import max_flow as mf


def solve(c_st, n):
    c = np.copy(c_st)

    for i in range(n):
        min_i = min(c[i])
        for j in range(n):
            c[i][j] -= min_i

    #print(c)

    for j in range(n):
        min_j = min(c[:, j])
        for i in range(n):
            c[i][j] -= min_j

    #print(c)

    network_out, arcs = build_network(c, n)

    while True:
        arc_flows, max_flow, L = mf.find_max_flow(network_out, arc_flows=None)
        print(max_flow)
        print(L)

        if max_flow == n:
            return True, arc_flows

        else:
            N1 = [i-1 for i in L if 1 <= i <= n]
            N2 = [i-n-1 for i in L if n+1 <= i <= 2*n]
            print(f'N1={N1}')
            print(f'N2={N2}')
            N2n = set(range(n)) - set(N2)
            print(N2n)

            alpha = np.Inf
            for i in N1:
                for j in N2n:
                    if c[i][j] < alpha:
                        alpha = c[i][j]

            print(alpha)

            for i in N1:
                for j in range(n):
                    c[i][j] -= alpha

            for j in N2:
                for i in range(n):
                    c[i][j] += alpha

            print(c)

            network_out, arcs = rebuild_network(network_out, arcs, c, n)



def rebuild_network(network, arcs, c, n):
    for i in range(n):
        for j in range(n):
            if c[i][j] == 0:
                if (i+1, n+j+1) not in arcs:
                    arcs.add((i+1, n+j+1))
                    network[i+1][n+j+1] = 2

    return network, arcs


def build_network(c, n):
    arcs = set({})

    size = 2*n + 2
    network_out = [{} for _ in range(size)]
    for i in range(1, n+1):
        network_out[0][i] = 1

    for i in range(n+1, size-1):
        network_out[i][size-1] = 1

    for i in range(n):
        for j in range(n):
            if c[i][j] == 0:
                arcs.add((i+1, n+j+1))
                network_out[i+1][n+j+1] = 2

    print(network_out)

    return network_out, arcs


def build_optimal_plan(arc_flows, n):
    x = np.zeros((n, n))
    for i in range(n):
        keys = [item[0] for item in arc_flows[i+1].items() if item[1] == 1]
        for key in keys:
            x[i][key-n-1] = 1

    return x



    #arc_flows = [dict.fromkeys(network_out[i].keys(), 0) for i in range(n)]
# network_out = [
#     {1: 4, 3: 9},
#     {3: 2, 4: 4},
#     {4: 1, 5: 10},
#     {2: 1, 5: 6},
#     {6: 2, 5: 1},
#     {6: 9},
#     {}
# ]


def main():
    n = 4
    c = np.array([
        [2, 10, 9, 7],
        [15, 4, 14, 8],
        [13, 14, 16, 11],
        [4, 15, 13, 19]
    ])

    has_solution, arc_flows = solve(c, n)
    print(arc_flows)

    x = build_optimal_plan(arc_flows, n)
    print(x)
    print('fuck you all')


if __name__ == '__main__':
    main()
