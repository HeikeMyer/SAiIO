import numpy as np


def build_potentials(Ustr, Ub, n):
    u = [None] * n
    u[0] = 0
    for i in range(n):
        for j in Ub[i]:
            if u[j] is None:
                u[j] = u[i] - Ustr[i][j] if j in Ustr[i].keys() else u[i] + Ustr[j][i]

    return u


def build_Un(U_str, Ub_str, n):
    Un_str = [[] for _ in range(n)]
    for i in range(n):
        for j in U_str[i].keys():
            if j not in Ub_str[i]:
                Un_str[i].append(j)

    #print(Un_str)
    return Un_str


def build_delta(U_str, Un_str, u, n):
    delta = {}
    #print(U_str)
    #print(u)
    for i, arcs in enumerate(Un_str):
        for j in arcs:
            val = u[i] - u[j] - U_str[i][j]
            if val > 0:
                return i, j
            delta[(i, j)] = val
            #print('\t', u[i], u[j], U_str[i][j])

    return -1, -1
    #print(delta)


def build_graph(U_str, n):
    graph = [[] for _ in range(n)]
    for i, arcs in enumerate(U_str):
        for j in arcs:
            graph[i].append(j)
            graph[j].append(i)

    #print(graph)

    return graph



def dfs(current, i0, j0, graph, visited, path, prev):
    visited[current] = True
    for node in graph[current]:
        if node == i0 and visited[j0]:
            path[node] = current
            return True, current

        if not visited[node]:
            path[node] = current

            cycle_detected = dfs(node, i0, j0, graph, visited, path, current)
            if cycle_detected[0]:
                return cycle_detected

    return False, -1


def find_cycle(i0, j0, graph, n):
    visited = [False] * n
    path = [-1] * n
    b, cur = dfs(i0, i0, j0, graph, visited, path, -1)

    #print(f'path={path}', b, cur)

    cycle = []
    j = cur
    while True:
        cycle.append((j, path[j]))
        #print(j)

        if j == i0:
            break

        j = path[j]

    #print(cycle)

    return cycle



def main():
    n = 6


    network_out = [
        {1: 1},
        {5: 3},
        {1: 3, 3: 5},
        {},
        {2: 4, 3: 1},
        {0: -2, 2: 3, 4: 4}
    ]

    arc_flows = [
        {1: 1},
        {5: 0},
        {1: 3, 3: 1},
        {},
        {2: 0, 3: 5},
        {0: 0, 2: 9, 4: 0}
    ]
    #print(network_out)

    network_in = [{} for _ in range(n)]
    for i in range(n):
        for j, d in network_out[i].items():
            network_in[j][i] = d

    #print(network_in)

    intensities = [1, -4, -5, -6, 5, 9]

    Ub_str =[
        [1],
        [],
        [1, 3],
        [],
        [3],
        [2]
    ]

    Un_str = build_Un(network_out, Ub_str, n)

    u = build_potentials(network_out, build_graph(Ub_str, n), n)
    #print(u)

    i0, j0 = build_delta(network_out, Un_str, u, n)
    #print(i0, j0)

    Ub_str[i0].append(j0)

    cycle = find_cycle(i0, j0, build_graph(Ub_str, n), n)

    #print(cycle)

    min_flow = np.Inf
    min_arc = None
    for i, j in cycle:
        if i in network_out[j].keys():
            val = arc_flows[j][i];
            if val < min_flow:
                min_flow = val
                min_arc = (j, i)

    #print(min_flow, min_arc)

    #rebuild flows
    for i, j in cycle:
        if j in network_out[i].keys():
            arc_flows[i][j] += min_flow
        else:
            arc_flows[j][i] -= min_flow

    #print(arc_flows)

    print(Ub_str)
    Ub_str[min_arc[0]].remove(min_arc[1])
    print(Ub_str)


    # print(network_out)
    # print(intensities)






#def main():
    # n = 9
    # graph = [
    #     [1],
    #     [0, 2, 5],
    #     [1, 3, 4],
    #     [2],
    #     [2, 5],
    #     [1, 4, 6, 8],
    #     [5, 7],
    #     [6],
    #     [5]
    # ]
    # i0, j0 = 1, 5

    # n = 12
    # graph = [
    #     [1],
    #     [0, 3, 5],
    #     [3],
    #     [1, 2, 4],
    #     [3, 7],
    #     [1, 6],
    #     [10, 8, 7, 5],
    #     [4, 6],
    #     [6],
    #     [10],
    #     [6, 9, 11],
    #     [10]
    # ]
    # i0, j0 = 6, 7

    # find_cycle(i0, j0, graph, n)
    #
    # print('fuck')


if __name__ == '__main__':
    main()