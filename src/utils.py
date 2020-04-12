import os
from config import DATA_PATH, RESULT_PATH


def read_in_txt(filename):
    """ read the input data points as a python list
    :param filename:
    :return:
    """
    content = []
    data_points_x = []
    data_points_y = []
    with open(os.path.join(DATA_PATH, filename), 'rt') as lines:
        for each in lines:
            data_point = list(map(float, each.strip().split(' ')))
            data_points_x.append(data_point[0])
            data_points_y.append(data_point[1])
            content.append(tuple(data_point))
    return content, data_points_x, data_points_y


def read_out_txt(filename):
    """read the output B-Spline curve file
    :param filename:
    :return: degree, num of control points, knots list, control points list x, y
    """
    control_point_x = []
    control_point_y = []
    with open(os.path.join(RESULT_PATH, filename), "rt") as output:
        for idx, line in enumerate(output.readlines()):
            line = line.strip('\n')
            if idx == 0:
                k = int(line.strip('\n'))
            elif idx == 1:
                cnt_num = int(line.strip('\n'))
            elif idx == 3:
                knots_list = line.strip().split(' ')
                knots_list = list(map(float, knots_list))
            elif idx >= 5:
                control_point = line.strip("\n").split(' ')
                control_point = list(map(float, control_point))
                control_point_x.append(control_point[0])
                control_point_y.append(control_point[1])
    return k, cnt_num, knots_list, control_point_x, control_point_y


def save_out_txt(degree, control_points, knots_list, filename):
    """save the B-spline curve in txt
    :param degree:
    :param control_points:
    :param knots_list:
    :param filename:
    :return: degree, num of control points, knot sequence, x- and y-coordinates of the control points
    """
    with open(os.path.join(RESULT_PATH, filename[:-4]+'outuni.txt'), "wt") as f:
        f.write(str(degree)+'\n')
        f.write(str(len(control_points))+'\n')
        f.write('\n')
        for knots in knots_list:
            f.write(str(knots)+' ')
        f.write('\n')
        f.write('\n')
        for x, y in control_points:
            f.write(str(x)+" "+str(y)+'\n')

    log("Export cubic B-Spline file successfully")


def log(*args, **kwargs):
    print('log:', *args, **kwargs)
