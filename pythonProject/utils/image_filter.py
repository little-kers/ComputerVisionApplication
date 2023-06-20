import os
import shutil

import cv2
import numpy as np

from log_cfg.log_config import log_init
from utils.check_directory_exits import check_directory_exits
from utils.check_file_type import check_file_type
from utils.image_similarity_calculator import similarity_calculator

FILE_NAME = "run"

IMAGE_FILTER = "image filter"

VALID_DATA = "valid_data"

# def log_init(path=r"./logs"):
#     """
#     It will initialize a logger that can using in this file.
#     :return: Logger
#     """
#     # path = r"./logs"
#     log_name = "image_filter-run"
#     # create the directory as the log saved path
#     os.makedirs(os.path.abspath(path), exist_ok=True)
#     # if this path exits, the function bellow will be running
#     if check_directory_exits(path):
#         l = MyLogger(name=log_name, file=f"{path}/run.log")
#     else:
#         raise OSError(f"Fail to create {path}.")
#     return l


logger = log_init(name=("%s" % IMAGE_FILTER), file_name=("%s" % FILE_NAME))


def single_channel_filter(dir_path=None):
    """
    It will filter the image that channel is single and move it to the expected directory.
    :param dir_path: The path of images
    :return: A number of single channel pictures
    """

    filter_path = os.path.join(os.path.dirname(dir_path), "%s/single_channel_images" % VALID_DATA)
    check_directory_exits(filter_path, create=True)
    single_channel_list = []
    for root, dirs, files in os.walk(dir_path):
        if files is None or len(files) == 0:
            continue
        for f in files:
            file_path = os.path.join(root, f)
            # image = Image.open(file_path)
            image = cv2.imread(file_path)
            image_channels = image.shape[2]
            # 2为单通道
            if image_channels == 1:
                single_channel_list.append(f)
                shutil.move(file_path, filter_path)
    logger.info(f"Single channel image is: {single_channel_list}")
    return len(single_channel_list)


def similar_filter(dir_path=None):
    """
    It will filter the too similar image, and one to move to the excepted directory.
    :param dir_path:
    :return: A number of similar image files
    """
    filter_dir = os.path.join(os.path.dirname(dir_path), "%s/similar_images" % VALID_DATA)
    check_directory_exits(filter_dir, create=True)
    similar_list = []
    for root, dirs, files in os.walk(dir_path):
        if files is None or len(files) == 0:
            continue
        for i in range(len(files)):
            if files[i] in similar_list:
                continue
            for j in range(i + 1, len(files)):
                if files[j] in similar_list:
                    continue
                image1_path = os.path.join(root, files[i])
                image2_path = os.path.join(root, files[j])
                if similarity_calculator(image1_path, image2_path):
                    similar_list.append(image2_path)
                    print("\r" + "Comparing: {0:.2f}%".format((i + 1) / len(files) * 100), end="")
    logger.info(f"Similar image is: {similar_list}")
    for f in similar_list:
        shutil.move(f, filter_dir)
        print("\r" + "Moving: {0:.2f}%".format((similar_list.index(f) + 1) / len(similar_list) * 100), end="")
    print("\n")
    return len(similar_list)


def blurred_filter(dir_path=None):
    """
    It will filter the image that too blurs and move it to the expected directory.
    :param dir_path:
    :return: A number of blurry images
    """
    filter_dir = os.path.join(os.path.dirname(dir_path), "%s/blur_images" % VALID_DATA)
    check_directory_exits(filter_dir, create=True)
    blur_list = []
    for root, dirs, files in os.walk(dir_path):
        if files is None or len(files) == 0:
            continue
        for f in files:
            if f in blur_list:
                continue
            image_path = os.path.join(root, f)
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
            img_var = cv2.Laplacian(image, cv2.CV_64F).var()
            if img_var < 100:
                blur_list.append(f)
                shutil.move(image_path, filter_dir)
    logger.info(f"Blurry image is: {blur_list}")
    return len(blur_list)


def illegal_image_filter(dir_path):
    """
    It will filter the image data basely, including the image is damaged or is untouchable.
    Moving it to the expected directory.
    :param dir_path: File the path
    :return: A number of damaged or untouchable image files
    """

    valid_path = os.path.join(os.path.dirname(dir_path), "%s/Damaged_or_untouchable_images" % VALID_DATA)
    # print(valid_path)
    check_directory_exits(valid_path, create=True)
    size = 0
    bad_list = []
    number = 0
    for root, dirs, files in os.walk(dir_path):
        number += len(files)
        if len(files) == 0 or files is None:
            continue
        for f in files:
            file_path = os.path.join(root, f)
            size += os.path.getsize(file_path)
            # print(file_path)
            if check_file_type(f, type_list=['jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif']):
                image = cv2.imread(file_path)
                # remove can't load image to another directory
                if image is None:
                    bad_list.append(file_path)
                else:
                    continue
            else:
                bad_list.append(file_path)
    for f in bad_list:
        shutil.move(f, valid_path)
        print("\r" + "Moving: {0:.2f}%".format((bad_list.index(f) + 1) / len(bad_list) * 100), end="")
    logger.info(
        f"The directory memory is: {size / 1024 / 1024}MB\t"
        f"The directory contain file number is: {number}\t"
        f"Damaged or untouchable image is: {bad_list}")
    return len(bad_list)
