import os

PATH = r"your/data/path"


# # 获取路径下所有文件名
# file_names = os.listdir('/your/dir/path')
#
# # 遍历文件并重命名
# for i, name in enumerate(file_names):
#     os.rename(os.path.join('/your/dir/path', name), os.path.join('/your/dir/path', 'new_name_{}.txt'.format(i + 1)))
def singular(word):
    """
    If the word ends with s, it will be removed.
    :param word:
    :return:
    """
    if word.endswith('s'):
        return word[:-1]
    else:
        return word


def file_is_formatted(file_name):
    """
    If the file base name is excepted type like file.0.type, it will do nothing.
    :param file_name:
    :return:
    """
    min_dot_index = file_name.find(".")
    max_dot_index = file_name.rfind(".")
    dot_index = max_dot_index - min_dot_index
    ret = False
    if dot_index == 0:
        ret = True
    return ret


def file_rename_for_project(path):
    for root, Dirs, FILES in os.walk(path):
        if FILES is None or len(FILES) == 0:
            continue
        for i, f in enumerate(FILES):
            if file_is_formatted(f):
                continue
            print("\r" + "Renaming: {0:.2f}%".format((FILES.index(f) + 1) / len(FILES) * 100), end="")
            src_file = os.path.join(root, f)
            dst_file = os.path.join(root,
                                    f"{singular(os.path.dirname(src_file)[-4:])}.{i}.{os.path.basename(f).split('.')[1]}")
            os.rename(src_file, dst_file)


file_rename_for_project(PATH)
print("\nRename success.")
