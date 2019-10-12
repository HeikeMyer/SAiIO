import numpy as np
import numpy.linalg as linalg
#from simplex.matrix_inversion import inverse


def dual_simplex(A, b, c, Jb):
    n = len(c)
    m = len(Jb)

    A_t = A.transpose()
    Ab = A[:, Jb]
    Ab_inv = linalg.inv(Ab)
    cb = c[Jb]
    Jn = list(set(range(n)) - set(Jb))

    y = np.matmul(cb, Ab_inv)

    while True:
        kappa_b = np.matmul(Ab_inv, b)
        kappa = [0] * n
        for i, index in enumerate(Jb):
            kappa[index] = kappa_b[i]
        print(kappa, Jb)

        negative_basis_index = -1
        for i, index in enumerate(Jb):
            if kappa[index] < 0:
                negative_basis_index = i
                break
        else:
            return kappa, Jb

        delta_y = Ab_inv[negative_basis_index]

        mus = []
        for i in Jn:
            mus.append(np.matmul(delta_y, A[:, i]))

        deltas = []
        for i, mu in enumerate(mus):
            if mu < 0:
                deltas.append((Jn[i], (c[Jn[i]] - np.matmul(A_t[Jn[i]], y)) / mu))

        if not deltas:
            return None

        min_delta = min(deltas, key=lambda delta: delta[1])

        Jb[negative_basis_index] = min_delta[0]
        Jn = list(set(range(n)) - set(Jb))

        y = y + min_delta[1] * delta_y

        Ab = A[:, Jb]
        Ab_inv = linalg.inv(Ab)

    print(y)


def main():
    A = np.array([[7, 4, 1]])
    m = A.shape[0]
    n = A.shape[1]
    b = np.array([13])
    c = np.array([21, 11, 0])
    Jb = [2]

    dual_simplex(A, b, c, Jb)


if __name__ == '__main__':
    main()
