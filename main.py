"""
The vpfr implements the cubic B-spline interpolation algorithm,
which accepts an input file that contains a set of 2D points, outputs
a cubic B-spline curve, and displays the B-spline curve as well.
"""

from src.CubicBSpline import parameterize, basis, solver
from config import filename
from src.utils import *


def cubicBSpline(filename, degree=3):
    # Read txt data point
    data_points = read_txt(filename)

    # Step 1: Parameterization
    params_list, knots_list = parameterize(data_points, degree)

    # Step 2: Find the B-Spline curve
    basis_mat = basis(params_list, knots_list)  # calculate basis matrix
    control_points = solver(basis_mat, data_points)  # solve the linear equation

    # save txt
    save_txt(degree, control_points, knots_list, filename)


def main():
    input_txt = filename
    cubicBSpline(input_txt)


if __name__ == '__main__':
    main()
