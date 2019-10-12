import math
import scipy.optimize
from dual_simplex_method import *


def is_integer(x, epsilon):
    result = True
    for i, component in enumerate(x):
        decimal_part = abs(component - math.floor(component))
        if epsilon <= decimal_part <= 1 - epsilon:
            result = False
            break

    return result, i


def branch_and_bound(A, m, n, b, c, bounds):
    bounds_list = [bounds]
    t = 1
    r0 = 0
    has_int_plans = False
    opt_int_plan = np.zeros(range(n))
    while bounds_list:
        current_bounds = bounds_list.pop(0)

        result = scipy.optimize.linprog(-c, A, b, bounds=current_bounds)
        has_solution = result.success
        current_opt_plan = result.x

        r = np.dot(c, current_opt_plan) if has_solution else -np.Inf

        if not has_solution or r <= r0:
            t += 1
            continue

        is_int, j0 = is_integer(current_opt_plan, 0.0001)
        if is_int:
            opt_int_plan = current_opt_plan
            has_int_plans = True
            r0 = r
            t += 1
            continue

        x0 = current_opt_plan[j0]
        l0_int = math.floor(x0)

        bounds1 = list(current_bounds)
        bounds1[j0] = (current_bounds[j0][0], l0_int)
        bounds_list.append(bounds1)

        bounds2 = list(current_bounds)
        bounds2[j0] = (l0_int + 1, current_bounds[j0][1])
        bounds_list.append(bounds2)

        t += 1

    return has_int_plans, opt_int_plan


def main():
    A = np.array([[-3, 6, 7], [6, -3, 7]])
    m = A.shape[0]
    n = A.shape[1]
    b = np.array([8, 8])
    c = np.array([3, 3, 13])
    bounds = [(0, 5), (0, 5), (0, 5)]

    has_int_plans, opt_int_plan = branch_and_bound(A, m, n, b, c, bounds)

    print(f'Has integer solutions: {has_int_plans}')
    if has_int_plans:
        print(f'Solution: x = {opt_int_plan}')


if __name__ == "__main__":
    main()
