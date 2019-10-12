import math
import numpy as np
import numpy.linalg as la
import scipy.optimize
from dual_simplex_method import subtract, get_basis
from branch_and_bound_method import is_integer


EPSILON = 0.000001


def dual_simplex(A, b, c):
    result = scipy.optimize.linprog(-c, A, b)
    opt_plan = result.x
    Jb = get_Jb(opt_plan, A.shape[0], EPSILON)

    return opt_plan, Jb


def get_Jb(x, m, epsilon):
    basis = [index for index, component in enumerate(x) if component > epsilon]

    if len(basis) < m:
        raise Exception("aaaaaaaaaa")

    return basis


def get_decimal_part(number):
    integer_part = math.floor(number)
    return number - integer_part


def build_constraint(A, n, Jn, b, y):
    constraint = np.zeros(n + 1)
    for j in Jn:
        constraint[j] = -get_decimal_part(np.dot(y, A[:, j]))
    constraint[n] = 1

    b_i0 = -get_decimal_part(np.dot(y, b))

    return constraint, b_i0


def remove_extra_constraints(A, m_real, n_real, b, c):
    if A.shape[0] > n_real + 1:
        number_to_remove = A.shape[0] - m_real - 1
        print(A.shape, number_to_remove)
        while number_to_remove > 0:
            m_cur = A.shape[0]
            for k in range(m_real + 1, m_cur):
                for j in range(n_real):
                    A[k][j] -= A[k][n_real] * A[m_real][j]
                b[k] -= A[k][n_real] * b[m_real]

            A = np.delete(A, m_real, axis=0)
            A = np.delete(A, n_real, axis=1)
            b = np.delete(b, m_real, axis=0)

            number_to_remove -= 1

        c = c[:n_real]

    return A, b, c


def gomory_cut(A, b, c):
    m_real, n_real = A.shape
    epsilon = EPSILON

    while True:
        opt_plan, Jb = dual_simplex(A, b, c)
        is_int, i0 = is_integer(opt_plan, epsilon)
        if is_int:
            break

        A, b, c = remove_extra_constraints(A, m_real, n_real, b, c)
        m, n = A.shape
        J = range(n)
        Jn = subtract(J, Jb)
        Ab = get_basis(A, Jb)
        Ab_inv = la.inv(Ab)
        e_i0 = np.identity(m)[:, i0]
        y = np.dot(e_i0, Ab_inv)

        constraint, b_i0 = build_constraint(A, n, Jn, b, y)

        A = np.append(A, np.zeros((m, 1)), axis=1)
        A = np.append(A, np.array([constraint]), axis=0)
        b = np.append(b, b_i0)
        c = np.append(c, 0)

    return is_int, opt_plan, Jb


def main():
    # A = np.array([[1, 2, 3, 0, 0, 0], [5, 4, 5, 1, 0, 0], [3, 0, 2, 2, 1, 0], [8, 5, 4, 3, 2, 1]])
    # b = np.array([8, 2, 4, 3])
    # c = np.array([3, 3, 13, 0, 0, 0])
    # print(A, b, c)
    # A_new, b_new, c_new = remove_extra_constraints(A, 1, 3, b, c)
    # print('\n', A_new, b_new, c_new)

    A = np.array([[7, 4, 1]])
    b = np.array([13])
    c = np.array([21, 11, 0])

    is_int, opt_plan, Jb = gomory_cut(A, b, c)
    print(f'Has integer solutions: {is_int}')
    if is_int:
        print(f'Solution:\nx = {opt_plan},\nJb = {Jb}')


if __name__ == '__main__':
    main()
