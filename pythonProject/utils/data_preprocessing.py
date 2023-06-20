import os
import random
from datetime import datetime

import cv2
from skimage.transform import resize

from log_cfg.log_config import log_init
from utils.check_directory_exits import check_directory_exits
from utils.check_file_exits import check_file_exits

FILE_NAME = "run"

IMAGE_PREPROCESSING = "image preprocessing"

# def log_init():
#     """
#     It will initialize a logger that can using in this file.
#     :return: Logger
#     """
#     path = r"./logs"
#     log_name = "image_enhancer-run"
#     # create the directory as the log saved path
#     os.makedirs(os.path.abspath(path), exist_ok=True)
#     # if this path exits, the function bellow will be running
#     if check_directory_exits(path):
#         l = MyLogger(name=log_name, file=f"{path}/run.log")
#     else:
#         raise OSError(f"Fail to create {path}.")
#     return l


logger = log_init(name=("%s" % IMAGE_PREPROCESSING), file_name=("%s" % FILE_NAME))


def image_size_normalize(image_path, save_path=None, normalized_image_size=(512, 512)):
    """
    It will resize the image and save it in the expected directory.
    You can set 'normalized_image_size' this element by a tuple to change resized image size.
    :param normalized_image_size:
    :param save_path:
    :param image_path: The image file path
    :return:
    """
    # check the normalizing data path is exited, if not it will be created.
    check_directory_exits(save_path, create=True)
    # create the data-saved path.
    normalize_path = os.path.join(save_path, os.path.dirname(image_path).split("\\")[-1])
    check_directory_exits(normalize_path, create=True)
    # make the image path transfer to the absolut path.
    image_path = os.path.abspath(image_path)
    # get the min index of dot in the image path.
    dot_min_index = image_path.find(".")
    # get the max index of dot in the image path.
    dot_max_index = image_path.rfind(".")
    # if the image path has more one dot, it will be replaced first dot to '_'.
    # if not, it will be split by dot and return a list that contains file name.just index of 0.
    is_single_dot = dot_max_index - dot_min_index
    # print(f"image path{image_path},is single dot:{is_single_dot}")
    if is_single_dot > 0:
        image_name = f"{normalize_path}" \
                     f"/{os.path.basename(image_path).replace('.', '_', 1).split('.')[0]}" \
                     f"_normalized.jpg"
    else:
        image_name = f"{normalize_path}" \
                     f"/{os.path.basename(image_path).split('.')[0]}" \
                     f"_normalized.jpg"
    # read the image.
    image = cv2.imread(image_path)
    # resize the image and size is (128,128).
    image_normalized = resize(image, normalized_image_size)

    # check the file is already exit, if not, it will be saved.
    if check_file_exits(image_name):
        logger.debug(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return
    else:
        image_normalized = cv2.convertScaleAbs(image_normalized, alpha=255.0)
        image_normalized = cv2.cvtColor(image_normalized, cv2.COLOR_BGR2RGB)
        cv2.imwrite(image_name, image_normalized)
        if check_file_exits(image_name):
            logger.info(f"Save image '{image_name}' successful.")
        else:
            logger.debug(f"Fail to save image {image_name}.")


def random_angle():
    """
    It will return a number between 0 and 360.
    :return:
    """
    num_of_angles = 5
    # get a number with range is 0-4 as index.
    random_index = int(datetime.now().timestamp()) % num_of_angles
    # create a list that contains 5 numbers and all small 360 and larger than 0.
    list_of_angles = [random.randint(0, 361) for _ in range(num_of_angles)]
    # return the angle that indexed in the list.
    return list_of_angles[random_index]


def four_random_number():
    """
    It will return a number between 0 and 3.
    :return:
    """
    return int(datetime.now().timestamp()) % 4


def image_rotater(image_path, save_path):
    """
    It will randomly rotate the image and save it in the expected directory.
    :param image_path: The image path.
    :param save_path: The expected directory path.
    :return: A number between 0 and 1 that this image is rotated or not.
    """
    # check the image file is already exits. if not, this function will be ending.
    if check_file_exits(image_path):
        image = cv2.imread(image_path)
    else:
        logger.error(f"No such file named: {os.path.basename(image_path)} in {image_path}",
                     exc_info=True, stack_info=True)
        print(f"No such file named: {image_path}")
        return 0
    # check if the target file already exits, if so, this function will terminate.
    image_name = f"{save_path}" \
                 f"/{os.path.basename(image_path)[:os.path.basename(image_path).index('.')]}" \
                 f"_rotated.jpg"
    if check_file_exits(image_name):
        logger.debug(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return 0
    random_number = four_random_number()
    if random_number == 0 or random_number == 2:
        return 0
    (h, w) = image.shape[:2]
    # get a random angle
    rotate_angel = random_angle()
    # calculate the matrix of rotate
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rotate_angel, 1.0)
    # rotating the image and filling the border color.
    rotated_image = cv2.warpAffine(image, M, (w, h), borderValue=cv2.BORDER_REPLICATE)
    logger.debug(f"image rotate angle is: {rotate_angel}, save path is: {image_name}")
    rotated_image *= 255
    rotated_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_name, rotated_image)
    return 1


def image_flipper(image_path, save_path):
    """
    It will randomly flip the image with vertical or horizontal and save it in the expected directory.
    :param image_path:
    :param save_path:
    :return: A number between 0 and 1 that this image is flipped or not.
    """
    if check_file_exits(image_path):
        image = cv2.imread(image_path)
    else:
        logger.error(f"An error occurred: No such file named {os.path.basename(image_path)} in {image_path}",
                     exc_info=True, stack_info=True)
        print(f"No such file named {image_path}")
        return 0
    flipped_image = None
    image_name = f"{save_path}" \
                 f"/{os.path.basename(image_path)[:os.path.basename(image_path).index('.')]}" \
                 f"_flipped.jpg"
    if check_file_exits(image_name):
        logger.info(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return 0
    image_operation = None
    # Run this function randomly.
    random_number = four_random_number()
    if random_number == 0:
        return 0
    elif random_number == 1:
        image_operation = "flipping the image with horizontal"
        # Flipping the image with horizontal
        flipped_image = cv2.flip(image, 1)
    elif random_number == 2:
        image_operation = "flipping the image with vertical"
        # Flipping the image with vertical
        flipped_image = cv2.flip(image, 0)
    elif random_number == 3:
        image_operation = "flipping the image with horizontal and vertical"
        # Flipping the image with horizontal and vertical
        flipped_image = cv2.flip(image, -1)
    logger.info(f"Image: {image_name}, image operation name is: {image_operation}")
    if flipped_image is None:
        logger.error(f"An error occurred: flipped_image is {flipped_image} in function image_flipper!", exc_info=True,
                     stack_info=True)
        raise OSError(f"An error occurred: flipped_image is {flipped_image} in function image_flipper!")
    flipped_image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_name, flipped_image)
    return 1


def image_threshold(image_path, save_path):
    """
    It will randomly to maek a threshold image by input image and save it in the expected directory.
    :param image_path:
    :param save_path:
    :return: A number between 0 and 1 that this image is a threshold or not.
    """
    if check_file_exits(image_path):
        image = cv2.imread(image_path)
    else:
        logger.error(f"An error occurred: No such file named {os.path.basename(image_path)} in {image_path}",
                     exc_info=True, stack_info=True)
        print(f"No such file named {image_path}")
        return 0
    image_name = f"{save_path}" \
                 f"/{os.path.basename(image_path)[:os.path.basename(image_path).index('.')]}" \
                 f"_threshold.jpg"
    if check_file_exits(image_name):
        logger.info(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return 0
    # operating image randomly.
    random_number = four_random_number()
    if random_number == 0 or random_number == 2:
        return 0
    threshed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, binary) = cv2.threshold(threshed_image, 127, 255, cv2.THRESH_BINARY)
    logger.info(f"Image: {image_name}, image is threshold.")
    cv2.imwrite(image_name, binary)
    return 1


def image_resizer(image_path, save_path):
    """
    It will randomly to resizing the image size and save it in the expected directory.
    :param image_path:
    :param save_path:
    :return: A number between 0 and 1 that this image is resized or not.
    """
    if check_file_exits(image_path):
        image = cv2.imread(image_path)
    else:
        logger.error(f"No such file named {os.path.basename(image_path)} in {image_path}",
                     exc_info=True, stack_info=True)
        print(f"No such file named {image_path}")
        return 0
    operation_name = "enlarge"
    # Initialize this element rate is 1, it will be not change image size.
    operation_rate = 1
    resized_image = None
    # Randomly running this function.
    random_number = four_random_number()
    if random_number == 0 or random_number == 3:
        return 0
    if random_number == 1:
        # Shrink the size of image.
        operation_name = "shrink"
        operation_rate = random.randint(1, 10) / 10
        # Operate_rage is a number that between 0.1 and 1.
        resized_image = cv2.resize(image, dsize=None, fx=operation_rate, fy=operation_rate,
                                   interpolation=cv2.INTER_AREA)
    if random_number == 2:
        # Enlarge the size of number.
        operation_rate = random.randint(1, 10) / 10 + 1
        # Operate_rate is a number that between 1.1 and 2
        resized_image = cv2.resize(image, dsize=None, fx=operation_rate, fy=operation_rate,
                                   interpolation=cv2.INTER_AREA)
    image_name = f"{save_path}" \
                 f"/{os.path.basename(image_path)[:os.path.basename(image_path).index('.')]}" \
                 f"_{operation_name}.jpg"
    if check_file_exits(image_name):
        logger.info(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return 0
    logger.info(f"Image: {image_path}, The image operation name is {operation_name} and rate is {operation_rate}")
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_name, resized_image)
    return 1


def image_median_blur(image_path, save_path, is_random=True):
    """
    It will blur the image and save it in the except directory.
    Randomly to do blur by argument 'is_random' is true.
    :param image_path:
    :param save_path:
    :param is_random:
    :return: A number between 0 and 1 that this image is blurred or not.
    """
    if check_file_exits(image_path):
        image = cv2.imread(image_path)
    else:
        logger.error(f"No such file named {os.path.basename(image_path)} in {image_path}",
                     exc_info=True, stack_info=True)
        print(f"No such file named {image_path}")
        return 0
    image_name = f"{save_path}" \
                 f"/{os.path.basename(image_path)[:os.path.basename(image_path).index('.')]}" \
                 f"_median_blured.jpg"
    if check_file_exits(image_name):
        logger.info(f"'{image_name}' File already exits in: {os.path.dirname(image_name)}")
        return 0
    # print(image_name)
    if is_random:
        random_number = four_random_number()
        if random_number == 0 or random_number == 2:
            return 0
    else:
        pass
    image_median_blured = cv2.medianBlur(image, 5)
    logger.info(f"Image: {image_path}, image is median blured.")
    image_median_blured = cv2.cvtColor(image_median_blured, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_name, image_median_blured)
    return 1
