import os

from log_cfg.log_config import log_init
from utils.check_directory_is_empty import check_directory_is_empty

FILE_NAME = "run"

CHECK_DIRECTORY_EXITS = "check directory exits"

# log_name = "run"
# log_save_path = r"./logs"
# os.makedirs(log_save_path, exist_ok=True)
# logger = MyLogger("check_directory_exits-run", file=f"{log_save_path}/{log_name}.log")
logger = log_init(name=("%s" % CHECK_DIRECTORY_EXITS), file_name=("%s" % FILE_NAME))


def clear_folder(directory_path):
    """
    It will format the directory.
    :param directory_path:
    :return: None
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                clear_folder(file_path)
                os.rmdir(file_path)
            if check_directory_is_empty(directory_path):
                logger.info(f"Format directory success: '{directory_path}'")
        except Exception as e:
            logger.error("Failed to delete {0}. Reason: {1}".format(file_path, e), exc_info=True, stack_info=True)
            raise Exception('Failed to delete {0}. Reason: {1}.'.format(file_path, e))


def check_directory_exits(dir_path, create=None, clear=False):
    """
    It will check this path is exits. If yes, it can return a result is true or
    format this path by argument 'clear' is true.
    If this path is not exiting, it can be created by argument 'create' is true.
    :param clear: It will be formatted.
    :param create: It will be created.
    :param dir_path:
    :return: Boolean
    """
    ret = True
    # Check the directory is exited.
    if os.path.exists(dir_path):
        # It will be formatted.
        if clear is True:
            clear_folder(dir_path)
            # Check the result after formatting.
            if os.listdir(dir_path) is None or len(os.listdir(dir_path)) == 0:
                print(f"Formatting folder successful: {dir_path}")
                logger.info(f"Formatting folder successful: {dir_path}")
        else:
            pass
    elif create is True:
        try:
            os.makedirs(dir_path)
            logger.info(f"Creating directory successful: '{dir_path}'")
            print(f"\rCreating directory successful: '{dir_path}'\n")
        except os.error as e:
            logger.error(f"An error occurred: {e}", exc_info=True, stack_info=True)
            raise OSError(f"Failed to create directory '{dir_path}'")
    else:
        logger.error(f"Directory '{dir_path}' does not exist", exc_info=True, stack_info=True)
        return False
    return ret
