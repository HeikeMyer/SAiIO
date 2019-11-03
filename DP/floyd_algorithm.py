import numpy as np


def iteration(t, D, R):
    D_ = np.copy(D)
    R_ = np.copy(R)

    cols = [j for j, d in enumerate(D[t]) if j != t and d != np.Inf]
    rows = [i for i, d in enumerate(D[:, t]) if i != t and d != np.Inf]

    for i in rows:
        for j in cols:
            if i == j:
                continue

            d = D[i][t] + D[t][j]
            if d < D[i][j]:
                D_[i][j] = d
                R_[i][j] = R[i][t]

    return D_, R_


def floyd(n, c):
    D = np.copy(c)
    R = np.empty((n, n), dtype=np.int32)

    for i in range(n):
        for j in range(n):
            R[i][j] = j

    for t in range(n):
        D, R = iteration(t, D, R)

    return D, R


def build_path(i0, j0, R):
    path = [i0]
    i = i0
    while i != j0:
        i = R[i][j0]
        path.append(i)

    return path


def main():
    # n = 4
    # c = np.array([
    #     [0, np.Inf, -2, np.Inf],
    #     [4, 0, 3, np.Inf],
    #     [np.Inf, np.Inf, 0, 2],
    #     [np.Inf, -1, np.Inf, 0]])

    n = 8
    c = np.array([
        [0, 9, np.Inf, 3, np.Inf, np.Inf, np.Inf, np.Inf],
        [9, 0, 2, np.Inf, 7, np.Inf, np.Inf, np.Inf],
        [np.Inf, 2, 0, 2, 4, 8, 6, np.Inf],
        [3, np.Inf, 2, 0, np.Inf, np.Inf, 5, np.Inf],
        [np.Inf, 7, 4, np.Inf, 0, 10, np.Inf, np.Inf],
        [np.Inf, np.Inf, 8, np.Inf, 10, 0, 7, np.Inf],
        [np.Inf, np.Inf, 6, 5, np.Inf, 7, 0, np.Inf],
        [np.Inf, np.Inf, np.Inf, np.Inf, 9, 12, 10, 0]
    ])

    D, R = floyd(n, c)
    print(f'D=\n{D}\nR=\n{R}')

    i0, j0 = 0, 4
    path = build_path(i0, j0, R)
    print(f'Shortest path from {i0} to {j0}: {path}')


if __name__ == '__main__':
    main()
