import numpy as np


def euclidean_distance(d1, d2):
    """calculate the distance between two data points
    :param d1: points 1
    :param d2: points 2
    :return: distance between two points
    """
    n = len(d1)
    sum_ = 0
    for i in range(n):
        sum_ += np.square(d1[i] - d2[i])
    return np.sqrt(sum_)


def set_knots(param_list, degree=3):
    """Set the B-spline knots
    :param param_list:
    :param degree:
    :return:
    """
    t0 = [0.] * degree
    tn = [1.] * degree
    knots_list = t0 + param_list + tn
    return knots_list


def evaluate(t, u, i, j):
    """evaluate the element of the N basis matrix
    :param t:
    :param u:
    :param i:
    :param j: 
    :return: N value
    """
    val = 0.

    if u[j] <= t[i] <= u[j + 1] and (t[i] != u[j] or t[i] != u[j + 1]):
        val = (t[i] - u[j]) ** 3 / ((u[j + 1] - u[j]) * (u[j + 2] - u[j]) * (u[j + 3] - u[j]))

    elif u[j + 1] <= t[i] < u[j + 2]:
        val = ((t[i] - u[j]) ** 2 * (u[j + 2] - t[i])) / (
                (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j]) * (u[j + 2] - u[j])) + \
            ((u[j + 3] - t[i]) * (t[i] - u[j]) * (t[i] - u[j + 1])) / (
                (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
            ((u[j + 4] - t[i]) * ((t[i] - u[j + 1]) ** 2)) / (
                (u[j + 2] - u[j + 1]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1]))

    elif u[j + 2] <= t[i] < u[j + 3]:
        val = ((t[i] - u[j]) * (u[j + 3] - t[i]) ** 2) / (
                (u[j + 3] - u[j + 2]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
            ((u[j + 4] - t[i]) * (u[j + 3] - t[i]) * (t[i] - u[j + 1])) / (
                (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1])) + \
            ((u[j + 4] - t[i]) ** 2 * (t[i] - u[j + 2])) / (
                (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))

    elif u[j + 3] <= t[i] <= u[j + 4] and (t[i] != u[j + 3] or t[i] != u[j + 4]):
        val = (u[j + 4] - t[i]) ** 3 / (
                (u[j + 4] - u[j + 3]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))

    if np.isnan(val) or np.isinf(val):
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
        val_ = 6 * (t[i] - u[j]) / ((u[j + 1] - u[j]) * (u[j + 2] - u[j]) * (u[j + 3] - u[j]))

    elif u[j + 1] <= t[i] <= u[j + 2] and (t[i] != u[j + 1] or t[i] != u[j + 2]):
        val_ = (2 * (u[j + 2] - t[i]) - 4 * (t[i] - u[j])) / (
                (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j]) * (u[j + 2] - u[j])) + \
             (2 * u[j] - 6 * t[i] + 2 * u[j + 1] + 2 * u[j + 3]) / (
                (u[j + 2] - u[j + 1]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
             (4 * u[j + 1] - 6 * t[i] + 2 * u[j + 4]) / (
                (u[j + 2] - u[j + 1]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1]))

    elif u[j + 2] <= t[i] <= u[j + 3] and (t[i] != u[j + 2] or t[i] != u[j + 3]):
        val_ = (6 * t[i] - 2 * u[j] - 4 * u[j + 3]) / (
                (u[j + 3] - u[j + 2]) * (u[j + 3] - u[j + 1]) * (u[j + 3] - u[j])) + \
             (6 * t[i] - 2 * u[j + 1] - 2 * u[j + 3] - 2 * u[j + 4]) / (
                (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 1]) * (u[j + 3] - u[j + 1])) + \
             (6 * t[i] - 2 * u[j + 2] - 4 * u[j + 4]) / (
                (u[j + 3] - u[j + 2]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))

    elif u[j + 3] <= t[i] <= u[j + 4] and (t[i] != u[j + 3] or t[i] != u[j + 4]):
        val_ = 6 * (u[j + 4] - t[i]) / (
                (u[j + 4] - u[j + 3]) * (u[j + 4] - u[j + 2]) * (u[j + 4] - u[j + 1]))

    if np.isnan(val_) or np.isinf(val_):
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
    ac, bc, cc, dc = map(np.array, (a, b, c, d))
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
    """assign appropriate parameter values to data points
    :param data_points:
    :param degree:
    :param type_:
    :return:
    """
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
            t[i] = 1. / n

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
    n = len(params_list) - 1
    num_deboors = n + 3
    params_array = np.asarray(params_list)
    knots_array = np.asarray(knots_list)
    basis_mat = np.zeros((num_deboors, num_deboors))

    for i in range(n + 1):
        for j in range(n + 3):
            basis_mat[i + 1][j] = evaluate(params_array, knots_array, i, j)
    for i in range(2):
        for j in range(n + 3):
            basis_mat[i * (n + 2)][j] = endpoints(params_array, knots_array, i * n, j)

    return basis_mat


def solver(basis_mat, data_points):
    """ solve the linear system
    :param basis_mat: basis matrix
    :param data_points: given data points
    :return: a list of control points of the B-Spline
    """
    control_points = []
    n = basis_mat.shape[0]
    d0 = [(0, 0)]
    appended_data_points = d0 + data_points + d0
    x = np.asarray(appended_data_points)[:, 0]
    y = np.asarray(appended_data_points)[:, 1]

    # swap the 1st and 2nd rows, the n - 1 and n rows
    basis_mat[[0, 1]] = basis_mat[[1, 0]]
    basis_mat[[n - 2, n - 1]] = basis_mat[[n - 1, n - 2]]
    x[[0, 1]] = x[[1, 0]]
    x[[n - 2, n - 1]] = x[[n - 1, n - 2]]
    y[[0, 1]] = y[[1, 0]]
    y[[n - 2, n - 1]] = y[[n - 1, n - 2]]

    # extract diagonal
    lower_diag = np.diag(basis_mat, k=-1)
    main_diag = np.diag(basis_mat)
    upper_diag = np.diag(basis_mat, k=1)

    x_control = tridiag_solver(lower_diag, main_diag, upper_diag, x)
    y_control = tridiag_solver(lower_diag, main_diag, upper_diag, y)

    for i in range(n):
        control_points.append((x_control[i], y_control[i]))

    return control_points
