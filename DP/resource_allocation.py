import numpy as np


def solve(c, n, fs):
    m = c + 1
    x0s = np.empty((n, m), dtype=np.int32)
    B = np.empty((n, m), dtype=np.int32)

    for x in range(m):
        x0s[0][x] = x
        B[0][x] = fs[0](x)

    for i in range(1, n):
        for x in range(m):
            max_income = -np.Inf
            x0 = 0
            for z in range(x+1):
                cur_income = fs[i](z) + B[i-1][x-z]
                if cur_income > max_income:
                    max_income = cur_income
                    x0 = z
            B[i][x] = max_income
            x0s[i][x] = x0

    opt_plan = []
    y = c
    for i in range(n-1, -1, -1):
        y_left = y-x0
        opt_plan.append(x0)
        x0 = x0s[i-1][y_left]
        y = y_left

    opt_plan.reverse()

    return max_income, opt_plan


def main():
    # c = 6
    # n = 3
    # income = np.array([[0, 3, 4, 5, 8, 9, 10], [0, 2, 3, 7, 9, 12, 13], [0, 1, 2, 6, 11, 11, 13]], dtype=np.int32)
    # f1 = lambda x: income[0][x]
    # f2 = lambda x: income[1][x]
    # f3 = lambda x: income[2][x]
    #
    # max_income, x0 = solve(c, n, [f1, f2, f3])

    c = 10
    n = 6
    income = np.array([
        [0, 1, 2, 2, 2, 3, 5, 8, 9, 13, 14],
        [0, 1, 3, 4, 5, 5, 7, 7, 10, 12, 12],
        [0, 2, 2, 3, 4,	6, 6, 8, 9,	11,	17],
        [0,	1, 1, 1, 2,	3, 9, 9, 11, 12, 15],
        [0,	2, 7, 7, 7,	9, 9, 10, 11, 12, 13],
        [0,	2, 5, 5, 5,	6, 6, 7, 12, 18, 22]], dtype=np.int32)

    fs = [
        lambda x: income[0][x],
        lambda x: income[1][x],
        lambda x: income[2][x],
        lambda x: income[3][x],
        lambda x: income[4][x],
        lambda x: income[5][x]
    ]

    max_income, x0 = solve(c, n, fs)
    print(f'Max income: {max_income}\nx0: {x0}')


if __name__ == '__main__':
    main()
