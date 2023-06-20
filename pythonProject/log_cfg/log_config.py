import logging
import os


class MyLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO, file=None):
        super(MyLogger, self).__init__(name, level)
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if file:
            file_handle = logging.FileHandler(file, encoding="utf-8")
            file_handle.setFormatter(logging.Formatter(log_format))
            self.addHandler(file_handle)
        else:
            terminal_handle = logging.StreamHandler()
            terminal_handle.setFormatter(logging.Formatter(log_format))
            self.addHandler(terminal_handle)


def log_init(name="per log name", file_name="debug", path=r"./logs"):
    """
    It will initialize a logger that can using in this file.
    :return: Logger
    """
    # path = r"./logs"
    # log_name = "image_filter-run"
    # create the directory as the log saved path
    os.makedirs(os.path.abspath(path), exist_ok=True)
    # if this path exits, the function bellow will be running
    l = MyLogger(name=name, file=f"{path}/{file_name}.log")
    return l


if __name__ == '__main__':
    logger = MyLogger("yyy")
    logger.info("this is terminal info log.")
