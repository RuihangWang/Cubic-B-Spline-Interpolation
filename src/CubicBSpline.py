from src.utils import log, zeros_matrix


def euclidean_distance(d1, d2):
    """calculates the distance between two data points
    :param d1: points 1
    :param d2: points 2
    :return: distance between two points
    """
    n = len(d1)
    sum_ = 0
    for i in range(n):
        sum_ += (d1[i] - d2[i])**2
    return (sum_)**0.5


def set_knots(param_list, degree=3):
    """sets the B-spline knots
    :param param_list:
    :param degree:
    :return:
    """
    t0 = [0.] * degree
    tn = [1.] * degree
    knots_list = t0 + param_list + tn
    return knots_list


def evaluate(t, u, i, j):
    """evaluates the element of the N basis matrix
    :param t:
    :param u:
    :param i:
    :param j: 
    :return: N value
    """
    val = 0.

    if u[j] <= t[i] <= u[j + 1] and (t[i] != u[j] or t[i] != u[j + 1]):
        try:
            val = (t[i] - u[j]) ** 3 / ((u[j + 1] - u[j]) * (u[j + 2] - u[j]) * (u[j + 3] - u[j]))
        except ZeroDivisionError:
            val = 0.

    elif u[j + 1] <= t[i] < u[j + 2]:
        try:
            val = ((t[i] - u[j]) ** 2 * (u[j + 2] - t[i])) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j]) * (u[j + 2] - u[j])) + \
                  ((u[j + 3] - t[i]) * (t[i] - u[j]) * (t[i] - u[j + 1])) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
                  ((u[j + 4] - t[i]) * ((t[i] - u[j + 1]) ** 2)) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1]))
        except ZeroDivisionError:
            val = 0.

    elif u[j + 2] <= t[i] < u[j + 3]:
        try:
            val = ((t[i] - u[j]) * (u[j + 3] - t[i]) ** 2) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
                  ((u[j + 4] - t[i]) * (u[j + 3] - t[i]) * (t[i] - u[j + 1])) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1])) + \
                  ((u[j + 4] - t[i]) ** 2 * (t[i] - u[j + 2])) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))
        except ZeroDivisionError:
            val = 0.

    elif u[j + 3] <= t[i] <= u[j + 4] and (t[i] != u[j + 3] or t[i] != u[j + 4]):
        try:
            val = (u[j + 4] - t[i]) ** 3 / (
                    (u[j + 4] - u[j + 3]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))
        except ZeroDivisionError:
            val = 0.

    return val


def endpoints(t, u, i, j):
    """endpoints conditions
    :param t:
    :param u:
    :param i:
    :param j:
    :return:
    """
    val_ = 0.

    if u[j] <= t[i] <= u[j + 1] and (t[i] != u[j] or t[i] != u[j + 1]):
        try:
            val_ = 6 * (t[i] - u[j]) / ((u[j + 1] - u[j]) * (u[j + 2] - u[j]) * (u[j + 3] - u[j]))
        except ZeroDivisionError:
            val_ = 0.

    elif u[j + 1] <= t[i] <= u[j + 2] and (t[i] != u[j + 1] or t[i] != u[j + 2]):
        try:
            val_ = (2 * (u[j + 2] - t[i]) - 4 * (t[i] - u[j])) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j]) * (u[j + 2] - u[j])) + \
                   (2 * u[j] - 6 * t[i] + 2 * u[j + 1] + 2 * u[j + 3]) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
                   (4 * u[j + 1] - 6 * t[i] + 2 * u[j + 4]) / (
                    (u[j + 2] - u[j + 1]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1]))
        except ZeroDivisionError:
            val_ = 0.

    elif u[j + 2] <= t[i] <= u[j + 3] and (t[i] != u[j + 2] or t[i] != u[j + 3]):
        try:
            val_ = (6 * t[i] - 2 * u[j] - 4 * u[j + 3]) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
                   (6 * t[i] - 2 * u[j + 1] - 2 * u[j + 3] - 2 * u[j + 4]) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1])) + \
                   (6 * t[i] - 2 * u[j + 2] - 4 * u[j + 4]) / (
                    (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))
        except ZeroDivisionError:
            val_ = 0.

    elif u[j + 3] <= t[i] <= u[j + 4] and (t[i] != u[j + 3] or t[i] != u[j + 4]):
        try:
            val_ = 6 * (u[j + 4] - t[i]) / (
                    (u[j + 4] - u[j + 3]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))
        except ZeroDivisionError:
            val_ = 0.

    return val_


def tridiag_solver(a, b, c, d):
    """ Tri-diagonal matrix solver, a b c d can be NumPy array type or Python list type.
    refer to http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
    and to https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9
    :param a: lower diagonal
    :param b: main diagonal
    :param c: upper diagnoal
    :param d: right hand side of the system
    :return: solution of the system
    """
    nf = len(d)
    ac, bc, cc, dc = map(list, (a, b, c, d))
    for it in range(1, nf):
        mc = ac[it-1]/bc[it-1]
        bc[it] = bc[it] - mc*cc[it-1]
        dc[it] = dc[it] - mc*dc[it-1]

    xc = bc
    xc[-1] = dc[-1]/bc[-1]

    for il in range(nf-2, -1, -1):
        xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

    return xc


def parameterize(data_points, degree, type_='chord'):
    """assigns appropriate parameter values to data points
    :param data_points:
    :param degree:
    :param type_:
    :return:
    """
    log("{} parameterization of data points".format(type_))

    n = len(data_points)
    t = [0.] * n

    if type_ == 'chord':
        for i in range(1, n):
            numerator = 0
            denominator = 0
            for k in range(1, i + 1):
                numerator += euclidean_distance(data_points[k], data_points[k - 1])
            for k in range(1, n):
                denominator += euclidean_distance(data_points[k], data_points[k - 1])
            t[i] = numerator / denominator

    elif type_ == 'uniform':
        for i in range(1, n):
            t[i] = i / n

    else:
        msg = "Parameterization method doesn't exist"
        raise LookupError(msg)

    t[-1] = 1
    k = set_knots(t, degree)

    return t, k


def basis(params_list, knots_list):
    """Cubic B-spline basis
    :param params_list:
    :param knots_list:
    :return: basis matrix
    """
    log("Calculate B-Spline basis matrix")

    n = len(params_list) - 1
    cnt_num = n + 3  # control points
    basis_mat = zeros_matrix(cnt_num, cnt_num)

    for i in range(n + 1):
        for j in range(n + 3):
            basis_mat[i + 1][j] = evaluate(params_list, knots_list, i, j)
    for i in range(2):
        for j in range(n + 3):
            basis_mat[i * (n + 2)][j] = endpoints(params_list, knots_list, i * n, j)

    return basis_mat


def solver(basis_mat, data_points):
    """ solve the linear system
    :param basis_mat: basis matrix
    :param data_points: given data points
    :return: a list of control points of the B-Spline
    """
    control_points = []
    n = len(basis_mat[0])
    d0 = [(0, 0)]
    appended_data_points = d0 + data_points + d0
    x = [each[0] for each in appended_data_points]
    y = [each[1] for each in appended_data_points]

    # swap the 1st and 2nd rows, the n - 1 and n rows
    basis_mat[0], basis_mat[1] = basis_mat[1], basis_mat[0]
    basis_mat[n - 2], basis_mat[n - 1] = basis_mat[n - 1], basis_mat[n - 2]
    x[0], x[1] = x[1], x[0]
    x[n - 2], x[n - 1] = x[n - 1], x[n - 2]
    y[0], y[1] = y[1], y[0]
    y[n - 2], y[n - 1] = y[n - 1], y[n - 2]

    # extract diagonal
    lower_diag = [basis_mat[i + 1][i] for i in range(n - 1)]
    main_diag = [basis_mat[i][i] for i in range(n)]
    upper_diag = [basis_mat[i][i + 1] for i in range(n - 1)]

    x_control = tridiag_solver(lower_diag, main_diag, upper_diag, x)
    y_control = tridiag_solver(lower_diag, main_diag, upper_diag, y)

    log("Solve tri-diagnoal linear system")

    for i in range(n):
        control_points.append((x_control[i], y_control[i]))

    return control_points


def B(x, k, i, t):
    """recursive definition of B-Spline curve
    :param x:
    :param k:
    :param i:
    :param t:
    :return:
    """
    if k == 0:
        return 1.0 if t[i] <= x < t[i + 1] else 0.0
    if t[i + k] == t[i]:
        c1 = 0.0
    else:
        c1 = (x - t[i]) / (t[i + k] - t[i]) * B(x, k - 1, i, t)
    if t[i + k + 1] == t[i + 1]:
        c2 = 0.0
    else:
        c2 = (t[i + k + 1] - x) / (t[i + k + 1] - t[i + 1]) * B(x, k - 1, i + 1, t)
    return c1 + c2


def bspline(x, t, c, k):
    """evaluate B-Spline curve
    :param x:
    :param t:
    :param c:
    :param k:
    :return:
    """
    n = len(t) - k - 1
    assert (n >= k + 1) and (len(c) >= n)
    return sum(c[i] * B(x, k, i, t) for i in range(n))
