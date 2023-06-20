import numpy as np
from keras.utils import load_img, img_to_array
import tensorflow as tf

from log_cfg.log_config import log_init


def preprocess_image(img_path):
    # 加载图片
    img = load_img(img_path, target_size=(128, 128))
    # 将图片转换为数组
    img_array = img_to_array(img)
    # 将像素值缩放到 0 到 1 之间
    img_array /= 255.0
    # 添加一个维度，将图片的形状变为 (1, 128, 128, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def get_label(prediction):
    if prediction > 0.5:
        return 'dog'
    else:
        return 'cat'


image_path = r"./test_model_data/cats/cat.0.jpg"
model_path = r".\models\2023-05-25 06-15-57_debug.h5"
pre_image = preprocess_image(image_path)

model = tf.keras.models.load_model(model_path)

output = model.predict(pre_image)

print(output)

label = get_label(output[0][0])

print(label)

logger = log_init(name="test model", file_name="run")
logger.debug(f"The animal in the {image_path} is a {label}.")
