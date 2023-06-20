import os
import shutil

import cv2
import imagehash
from PIL import Image

from utils.check_directory_exits import check_directory_exits
from utils.check_file_exits import check_file_exits


# 定义一个函数，用于计算两个图像之间的汉明距离
def hamming_distance(hash1, hash2):
    return bin(int(hash1, 16) ^ int(hash2, 16)).count('1')


# 定义一个函数，用于比较图像之间的相似度并保存相似目标图像
def compare_image_similarity(data_folder, target_folder=r"valid_data/similar_images"):
    # target_folder = os.path.join(os.path.dirname(data_folder), "valid_data/similar_images")
    check_directory_exits(target_folder, create=True)
    # 获取所有图像的哈希值列表
    hashes = {}
    for r, DIRS, FILES in os.walk(data_folder):
        if FILES is None or len(FILES) == 0:
            continue
        for f in FILES:
            img_path = os.path.join(r, f)
            img = cv2.imread(img_path)
            hash_value = str(imagehash.phash(Image.fromarray(img)))
            hashes[img_path] = hash_value
            print("\r" + "Calculating image hash value: {0:.2f}%".format((FILES.index(f) + 1) / len(FILES) * 100),
                  end="")
    print("\n")
    # for filename in os.listdir(data_folder):
    #     img = cv2.imread(os.path.join(data_folder, filename))
    #     hash_value = str(imagehash.phash(Image.fromarray(img)))
    #     hashes[filename] = hash_value

    similar_image_num = 0
    # 比较图像之间的相似度并保存相似目标图像
    for filename, hash_value in hashes.items():
        max_similarity = 0
        max_filename = ''
        for ref_filename, ref_hash in hashes.items():
            if filename != ref_filename:
                distance = hamming_distance(ref_hash, hash_value)
                similarity = 1 - distance / 64.0
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_filename = ref_filename
        if max_filename:
            src_file = max_filename
            dst_path = target_folder
            # print(src_file, os.path.join(dst_path, os.path.basename(max_filename)))
            if check_file_exits(os.path.join(dst_path, os.path.basename(max_filename))):
                continue
            # print(src_file, dst_path)
            shutil.move(src_file, dst_path)
            similar_image_num += 1
        print("\r" + "Moving: {0:.2f}%".format((list(hashes.keys()).index(filename) + 1) / len(hashes.keys()) * 100), end="")
    print("\n")
    return similar_image_num
    # img = cv2.imread(os.path.join(data_folder, max_filename))
    # target_path = os.path.join(target_folder, filename)
    # cv2.imwrite(target_path, img)

# data_path = "../rawdata"
# compare_image_similarity(data_path)
