import os

from log_cfg.log_config import log_init

FILE_NAME = "run"

CHECK_DIRECTORY_IS_EMPTY = "check directory is empty"

logger = log_init(name=("%s" % CHECK_DIRECTORY_IS_EMPTY), file_name=("%s" % FILE_NAME))


def check_directory_is_empty(dir_path=None):
    """
    It will check the directory is empty and return a result and the type is boolean.
    :param dir_path:
    :return: Boolean
    """
    files = os.listdir(dir_path)
    is_empty = True
    if len(files) != 0 or files is not None:
        is_empty = False
    else:
        pass
    # print(f"{dir_path} is empty: {is_empty}.")
    logger.info(f"Dir {dir_path} is empty: {is_empty}.")

    return is_empty
