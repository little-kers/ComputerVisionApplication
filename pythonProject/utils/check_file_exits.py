import os

from log_cfg.log_config import log_init

FILE_NAME = "run"

CHECK_FILE_EXITS = "check file exits"

logger = log_init(name=("%s" % CHECK_FILE_EXITS), file_name=("%s" % FILE_NAME))


def check_file_exits(file_path):
    """
    Check the file is exit or not.
    :param file_path: File path
    :return: Boolean
    """
    file_directory = os.path.dirname(file_path)
    # print(file_directory)
    ret = False
    if os.path.exists(file_directory) and os.path.isfile(file_path):
        ret = True
    logger.info(f"File {file_directory} is exits: {ret}.")
    return ret
