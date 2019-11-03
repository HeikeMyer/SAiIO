import numpy as np


def iteration(t, D, R, n):
    D_ = np.copy(D)
    R_ = np.copy(R)

    cols = [j for j, d in enumerate(D[t]) if j != t and d != np.Inf]
    #print('cols', cols)

    rows = [i for i, d in enumerate(D[:, t]) if i != t and d != np.Inf]
    #print('rows', rows)

    for i in rows:
        for j in cols:
            d1 = D[i][j]
            d2 = D[i][t] + D[t][j]
            d = d1 if d1 < d2 else d2
            D_[i][j] = d
            if d2 > d1:
                R_[i][j] = R[i][t]

    return D_, R_


def floyd(n, c):
    D = np.copy(c)
    R = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            R[i][j] = j

    for t in range(n):
        print(f'\n\tt={t}')
        D, R = iteration(t, D, R, n)
        print(D)
        print(R)







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

    print(c)
    print()
    floyd(n, c)



if __name__ == '__main__':
    main()