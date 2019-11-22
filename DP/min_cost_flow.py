import numpy as np


def build_non_oriented_graph(network_out, n):
    graph = [[] for _ in range(n)]
    for i, arcs in enumerate(network_out):
        for j in arcs:
            graph[i].append(j)
            graph[j].append(i)

    return graph


def build_Un_out(network_out, Ub_out, n):
    Un_out = [[] for _ in range(n)]
    for i in range(n):
        for j in network_out[i].keys():
            if j not in Ub_out[i]:
                Un_out[i].append(j)

    return Un_out


def build_potentials(network_out, Ub, n):
    u = [None] * n
    u[0] = 0
    queue = [0]
    while queue:
        i = queue.pop()
        for j in Ub[i]:
            if u[j] is None:
                u[j] = u[i] - network_out[i][j] if j in network_out[i].keys() else u[i] + network_out[j][i]
                queue.append(j)

    return u


def is_optimal(network_out, Un_out, u):
    for i, arcs in enumerate(Un_out):
        for j in arcs:
            val = u[i] - u[j] - network_out[i][j]
            if val > 0:
                return False, i, j

    return True, -1, -1


def dfs_cycle(current, i0, j0, graph, visited, path):
    visited[current] = True
    for node in graph[current]:
        if node == i0 and visited[j0]:
            path[node] = current
            return True, current

        if not visited[node]:
            path[node] = current

            dfs_result = dfs_cycle(node, i0, j0, graph, visited, path)
            if dfs_result[0]:
                return dfs_result

    return False, -1


def find_cycle(i0, j0, graph, n):
    visited = [False] * n
    path = [-1] * n
    cycle_exists, start = dfs_cycle(i0, i0, j0, graph, visited, path)

    cycle = []
    j = start
    while True:
        cycle.append((j, path[j]))
        if j == i0:
            break

        j = path[j]

    return cycle


def solve(U_out, x, Ub_out, Un_out, n):
    while True:
        u = build_potentials(U_out, build_non_oriented_graph(Ub_out, n), n)

        is_opt, i0, j0 = is_optimal(U_out, Un_out, u)
        if is_opt:
            return True, x, Ub_out

        Ub_out[i0].append(j0)
        cycle = find_cycle(i0, j0, build_non_oriented_graph(Ub_out, n), n)

        teta0 = np.Inf
        i_min, j_min = -1, -1
        for i, j in cycle:
            if i in U_out[j].keys():
                if x[j][i] < teta0:
                    teta0 = x[j][i]
                    i_min, j_min = j, i

        if teta0 == np.Inf:
            return False, None, None

        for i, j in cycle:
            if j in U_out[i].keys():
                x[i][j] += teta0
            else:
                x[j][i] -= teta0

        Ub_out[i_min].remove(j_min)
        Un_out = build_Un_out(U_out, Ub_out, n)


def calculate_cost(network_out, x, n):
    cost = 0
    for i in range(n):
        for j, c in network_out[i].items():
            cost += c*x[i][j]

    return cost


def main():
    n = 6
    network_out = [
        {1: 5, 4: 1, 5: 5},
        {3: 10, 5: 3},
        {1: 3, 0: 1, 4: 2, 3: 6},
        {4: 3},
        {},
        {4: 4, 3: 2}
    ]

    x = [
        {1: 4, 4: 0, 5: 2},
        {3: 5, 5: 0},
        {1: 0, 0: 0, 4: 0, 3: 1},
        {4: 0},
        {},
        {4: 3, 3: 0}
    ]

    Ub_out = [
        [1, 5],
        [3],
        [3],
        [],
        [],
        [4]
    ]

    # n = 6
    #
    # network_out = [
    #     {1: 1},
    #     {5: 3},
    #     {1: 3, 3: 5},
    #     {},
    #     {2: 4, 3: 1},
    #     {0: -2, 2: 3, 4: 4}
    # ]
    #
    # x = [
    #     {1: 1},
    #     {5: 0},
    #     {1: 3, 3: 1},
    #     {},
    #     {2: 0, 3: 5},
    #     {0: 0, 2: 9, 4: 0}
    # ]
    #
    # Ub_out =[
    #     [1],
    #     [],
    #     [1, 3],
    #     [],
    #     [3],
    #     [2]
    # ]

    Un_out = build_Un_out(network_out, Ub_out, n)

    has_solutions, x_opt, Ub = solve(network_out, x, Ub_out, Un_out, n)
    if has_solutions:
        print(f'Min cost flow: {x_opt}\nCost: {calculate_cost(network_out, x_opt, n)}')


if __name__ == '__main__':
    main()
