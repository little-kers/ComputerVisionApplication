import sys
import tensorflow as tf
import sklearn
import skimage
import cv2
import numpy as np
import matplotlib
import pandas as pd
import imagehash
import PIL


def show_env():
    """
    Print all packages of this project version.
    :return:
    """
    # print the python version and system information.
    print("Python version: {}".format(sys.version))
    for package in tf, sklearn, skimage, cv2, np, matplotlib, pd, imagehash, PIL:
        # print names and versions of these packages.
        print("{0} version: {1}".format(package.__name__, package.__version__).capitalize())


if __name__ == '__main__':
    show_env()
