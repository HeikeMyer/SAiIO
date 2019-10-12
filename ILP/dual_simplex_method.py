import numpy as np
import numpy.linalg as la


class LinearProgrammingProblem:
    def __init__(self, A, m, n, b, c, bounds):
        self.A = A
        self.b = b
        self.c = c
        self.bounds = bounds
        self.m = m
        self.n = n
        self.J = list(range(n))


def subtract(x, y):
    return list(set(x) - set(y))


def get_basis(array, Jb):
    shape = array.shape
    if len(shape) == 1:
        return array[Jb]
    else:
        m = array.shape[0]
        rows = list(range(m))
        return array[rows][:, Jb]


def get_initial_delta(lpp, Jb, B):
    cb = get_basis(lpp.c, Jb)
    y = np.matmul(cb, B)
    delta = [np.dot(y, lpp.A[:, [j]]).item() - lpp.c[j] for j in lpp.J]

    return delta


def get_kappa(lpp, Jb, Jn, Jn_plus, Jn_minus, B):
    kappa = np.empty(lpp.n)
    for j in Jn_plus:
        kappa[j] = lpp.bounds[j][0]
    for j in Jn_minus:
        kappa[j] = lpp.bounds[j][1]

    temp = sum([np.dot(lpp.A[:, j], kappa[j]) for j in Jn])
    kappa_b = np.matmul(B, lpp.b - temp)

    for index, j in enumerate(Jb):
        kappa[j] = kappa_b[index]

    return kappa


def is_optimal(lpp, Jb, kappa):
    for index, j in enumerate(Jb):
        if lpp.bounds[j][0] <= kappa[j] <= lpp.bounds[j][1]:
            continue
        else:
            return False, j, index

    return True, -1, -1


def get_sigma0(lpp, Jn, Jn_plus, Jn_minus, B, kappa, jk, k, delta):
    mu = np.empty(lpp.n)

    mu[jk] = 1 if kappa[jk] < lpp.bounds[jk][0] else -1

    e_k = np.identity(lpp.m)[:, k]
    a = np.matmul(e_k, B)
    delta_y = mu[jk] * a
    sigma0 = np.Inf
    j0 = -1
    for j in Jn:
        mu[j] = np.matmul(delta_y, lpp.A[:, j])
        if j in Jn_plus and mu[j] < 0 or j in Jn_minus and mu[j] > 0:
            sigma = - delta[j] / mu[j]
            if sigma < sigma0:
                sigma0 = sigma
                j0 = j

    return sigma0 < np.inf, sigma0, j0, mu


def rebuild_coplan(lpp, Jb, Jn, sigma0, mu, jk, delta):
    delta_new = np.empty(lpp.n)

    for j in Jb:
        delta_new[j] = 0

    for j in Jn:
        delta_new[j] = delta[j] + sigma0 * mu[j]

    delta_new[jk] = delta[jk] + sigma0 * mu[jk]

    return delta_new


def rebuild_B(lpp, B, k, j0):
    z = np.dot(B, lpp.A[:, j0])
    zk = z[k]
    z[k] = -1
    d = np.multiply(z, -1 / zk)
    M = np.identity(lpp.m)
    for i in range(lpp.m):
        M[i][k] = d[i]

    B_new = np.matmul(M, B)

    return B_new


def dual_simplex(lpp, Jb):
    Ab = get_basis(lpp.A, Jb)
    B = la.inv(Ab)
    delta = get_initial_delta(lpp, Jb, B)
    Jn = subtract(lpp.J, Jb)
    Jn_plus = [j for j in Jn if delta[j] >= 0]
    Jn_minus = subtract(Jn, Jn_plus)

    has_feasible_plans = True
    while True:
        kappa = get_kappa(lpp, Jb, Jn, Jn_plus, Jn_minus, B)

        is_opt, jk, k = is_optimal(lpp, Jb, kappa)
        if is_opt:
            break

        has_feasible_plans, sigma_0, j_0, mu = get_sigma0(lpp, Jn, Jn_plus, Jn_minus, B, kappa, jk, k, delta)
        if not has_feasible_plans:
            break

        delta = rebuild_coplan(lpp, Jb, Jn, sigma_0, mu, jk, delta)

        Jb[k] = j_0
        Jn = subtract(lpp.J, Jb)
        B = rebuild_B(lpp, B, k, j_0)

        if j_0 in Jn_plus:
            Jn_plus.remove(j_0)

        if mu[jk] == 1:
            Jn_plus.append(jk)

        Jn_minus = subtract(Jn, Jn_plus)

    return has_feasible_plans, kappa, Jb


def main():
    A = np.array([[-3, 6, 7], [6, -3, 7]])
    m = A.shape[0]
    n = A.shape[1]
    b = np.array([8, 8])
    c = np.array([3, 3, 13])
    bounds = [(0, 5), (0, 5), (0, 5)]
    Jb = [0, 2]

    lpp = LinearProgrammingProblem(A, m, n, b, c, bounds)

    has_feasible_plans, kappa_opt, Jb_opt = dual_simplex(lpp, Jb)

    print(f'Has feasible plans: {has_feasible_plans}')
    if has_feasible_plans:
        print(f'Solution: kappa_opt = {kappa_opt}, Jb = {Jb_opt}')


if __name__ == "__main__":
    main()
