from functools import lru_cache

import cv2


@lru_cache(maxsize=None)
def image_hist_calc(image_path):
    image_array = cv2.imread(image_path)
    images = [image_array]
    ret = cv2.calcHist(images, [1], None, [256], [0, 256])  # 计算图直方图
    ret = cv2.normalize(ret, ret, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理
    return ret


def similarity_calculator(image1_path, image2_path):
    img1_H = image_hist_calc(image1_path)
    img2_H = image_hist_calc(image2_path)
    similar = cv2.compareHist(img1_H, img2_H, 0)  # 相似度比较
    # print(f'"{image1_path}"&&"{image2_path}"--similarity:', similar)
    # 0.98是阈值，可根据需求调整
    return similar > 0.98
