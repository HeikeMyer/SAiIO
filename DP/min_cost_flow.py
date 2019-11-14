import numpy as np


def dfs(current, i0, j0, graph, visited, path, prev):
    print(f'current={current}, prev={prev}, path={list(enumerate(path))}')# visited={visited}, path={path}')



    visited[current] = True
    for node in graph[current]:
        if node == i0 and path[j0] == i0:
            print(f'found current {current}, node {node}, prev={prev}')
            path[node] = current
            return True

        if not visited[node]:
            path[node] = current

            a = dfs(node, i0, j0, graph, visited, path, current)
            #print(f'cur ={current}, a={a}')
            if a:
                return a


def find_cycle(i0, j0, graph, n):
    visited = [False] * n
    path = [-1] * n
    print(path)
    dfs(i0, i0, j0, graph, visited, path, -1)

    print(f'path={path}')

    j = i0
    while True:
        print(j)

        if j == j0:
            break

        j = path[j]





def main():
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

    n = 12
    graph = [
        [1],
        [0, 3, 5],
        [3],
        [1, 2, 4],
        [3, 7],
        [1, 6],
        [10, 8, 7, 5],
        [4, 6],
        [6],
        [10],
        [6, 9, 11],
        [10]
    ]
    i0, j0 = 6, 7

    find_cycle(i0, j0, graph, n)

    print('fuck')


if __name__ == '__main__':
    main()