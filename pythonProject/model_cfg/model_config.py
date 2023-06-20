import os
from datetime import datetime

import tensorflow as tf
from keras.engine.sequential import Sequential
from keras.engine.functional import Functional

from log_cfg.log_config import MyLogger
from utils.check_directory_exits import check_directory_exits


# tf.compat.v1.disable_eager_execution()


def log_init():
    """

    :return:
    """
    path = r"./logs"
    log_name = "model_cfg-run"
    # create the directory as the log saved path
    os.makedirs(os.path.abspath(path), exist_ok=True)
    # if this path exits, the function bellow will be running
    if check_directory_exits(path):
        l = MyLogger(name=log_name, file=f"{path}/run.log")
    else:
        raise OSError(f"Fail to create {path}.")
    return l


logger = log_init()


def model_init():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  metrics=['accuracy'], run_eagerly=True)
    model.summary()
    return model


def model_save(model, name="debug", model_save_path="./mods"):
    """

    :param model: target model
    :param name: save model by this name
    :param model_save_path:
    :return:
    """
    model_target_type = Sequential
    if not isinstance(model, model_target_type):
        logger.error(f"Fail to save model: except type is {model_target_type}, but received type is {type(model)}.")
        return False
    model_name = f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}_{name}.h5'
    check_directory_exits(model_save_path, True)
    model_save_path = os.path.join(model_save_path, model_name)
    model.save(model_save_path)
    logger.info(f"Save model success: {model_save_path}")
    return True
