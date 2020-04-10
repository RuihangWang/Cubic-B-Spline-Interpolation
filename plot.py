import os
import numpy as np
import matplotlib.pyplot as plt
from src.cubicBSpline import bspline
from src.utils import read_in_txt, read_out_txt
from config import IN_FILENAME, OUT_FILENAME, RESULT_PATH


def plot():

    data_points, data_points_x, data_points_y = read_in_txt(IN_FILENAME)
    degree, cnt_num, knots_list, \
    control_points_x, control_points_y = read_out_txt(OUT_FILENAME)

    xx = np.linspace(0.01, 0.99, 100)

    fig, ax = plt.subplots()
    x = [bspline(x, knots_list, control_points_x , degree) for x in xx]
    y = [bspline(x, knots_list, control_points_y , degree) for x in xx]

    ax.plot(control_points_x, control_points_y, 'k--', marker='s',markerfacecolor='r', label='control points')
    ax.plot(data_points_x, data_points_y, ' ', marker='o', markerfacecolor='c', label='data points')
    ax.plot(x, y, 'g-', lw=2, label='B-Spline')
    ax.grid(True)
    ax.legend(loc='best')
    plt.savefig(os.path.join(RESULT_PATH, OUT_FILENAME[0:-4]+'png'))
    plt.show()


if __name__ == '__main__':
    plot()