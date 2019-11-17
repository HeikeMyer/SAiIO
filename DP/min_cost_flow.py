import numpy as np


def build_potentials(Ustr, Ub, n):
    # print(Ustr, Ub_str, n)
    u = [None] * n
    u[0] = 0

    queue = [0]
    print('qy=ueue',queue)

    while queue:
        i = queue.pop()
        print(f'i={i}, u={u}')
        for j in Ub[i]:
            if u[j] is None:
                print(f'\ti={i}, j={j} u[i]={u[i]}')
                u[j] = u[i] - Ustr[i][j] if j in Ustr[i].keys() else u[i] + Ustr[j][i]
                queue.append(j)

    return u



def build_potentials2(Ustr, Ub, n):
    #print(Ustr, Ub_str, n)


    u = [None] * n
    u[0] = 0
    for i in range(n):
        print(f'i={i}, u={u}')
        for j in Ub[i]:
            if u[j] is None:
                print(f'\ti={i}, j={j} u[i]={u[i]}')
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


def is_optimal(U_str, Un_str, u):
    for i, arcs in enumerate(Un_str):
        for j in arcs:
            val = u[i] - u[j] - U_str[i][j]
            if val > 0:
                return False, i, j

    return True, -1, -1


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


def solve(U_str, x, Ub_str, Un_str, n):
    #print(U_str, x, Ub_str, Un_str, n)
    t = 0
    while True:
        print(f't={t}')
        print(f'Ub={Ub_str}')
        u = build_potentials(U_str, build_graph(Ub_str, n), n)
        print(f'u={u}')
        is_opt, i0, j0 = is_optimal(U_str, Un_str, u)
        if is_opt:
            return True, x, Ub_str

        Ub_str[i0].append(j0)
        cycle = find_cycle(i0, j0, build_graph(Ub_str, n), n)

        teta0 = np.Inf
        i_min, j_min = -1, -1
        for i, j in cycle:
            if i in U_str[j].keys():
                if x[j][i] < teta0:
                    teta0 = x[j][i]
                    i_min, j_min = j, i

        if teta0 == np.Inf:
            return False, None, None

        for i, j in cycle:
            if j in U_str[i].keys():
                x[i][j] += teta0
            else:
                x[j][i] -= teta0

        Ub_str[i_min].remove(j_min)

        Un_str = build_Un(U_str, Ub_str, n)
        t+=1


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

    has_solutions, min_flow, Ub = solve(network_out, arc_flows, Ub_str, Un_str, n)
    print(has_solutions, min_flow, '\n', Ub)

    # u = build_potentials(network_out, build_graph(Ub_str, n), n)
    # #print(u)
    #
    # i0, j0 = build_delta(network_out, Un_str, u, n)
    # #print(i0, j0)
    #
    # Ub_str[i0].append(j0)
    #
    # cycle = find_cycle(i0, j0, build_graph(Ub_str, n), n)
    #
    # #print(cycle)
    #
    # min_flow = np.Inf
    # min_arc = None
    # for i, j in cycle:
    #     if i in network_out[j].keys():
    #         val = arc_flows[j][i];
    #         if val < min_flow:
    #             min_flow = val
    #             min_arc = (j, i)
    #
    # #print(min_flow, min_arc)
    #
    # #rebuild flows
    # for i, j in cycle:
    #     if j in network_out[i].keys():
    #         arc_flows[i][j] += min_flow
    #     else:
    #         arc_flows[j][i] -= min_flow
    #
    # #print(arc_flows)
    #
    # print(Ub_str)
    # Ub_str[min_arc[0]].remove(min_arc[1])
    # print(Ub_str)


    # print(network_out)
    # print(intensities)


if __name__ == '__main__':
    main()
