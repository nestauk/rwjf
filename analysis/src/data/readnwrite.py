import os


def get_data_dir():
    dir = os.path.join(os.path.dirname( '__file__' ), '../../../../data')
    dir = os.path.abspath(dir)
    return dir
