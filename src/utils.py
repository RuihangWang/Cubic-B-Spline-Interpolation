import os
from config import DATA_PATH, RESULT_PATH


def read_txt(filename):
    """ read a txt input file as a python list
    :param filename:
    :return:
    """
    content = []
    with open(os.path.join(DATA_PATH, filename), 'rt') as lines:
        for each in lines:
            each = map(float, each.strip().split(' '))
            content.append(tuple(each))
    return content


def save_txt(degree, control_points, knots_list, filename):
    """save the B-spline curve in txt
    :param degree:
    :param control_points:
    :param knots_list:
    :param filename:
    :return: degree, num of control points, knot sequence, x- and y-coordinates of the control points
    """
    with open(os.path.join(RESULT_PATH, filename[:-4]+'out.txt'), "wt") as f:
        f.write(str(degree)+'\n')
        f.write(str(len(control_points))+'\n')
        f.write('\n')
        for knots in knots_list:
            f.write(str(knots)+' ')
        f.write('\n')
        f.write('\n')
        for x, y in control_points:
            f.write(str(x)+" "+str(y)+'\n')
