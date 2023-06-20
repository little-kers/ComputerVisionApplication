from pandas import DataFrame
from matplotlib import pyplot as plt

from utils.check_directory_exits import check_directory_exits


def show_ret_by_bar(map_name, label_list, value_list, save_path=r"./rets"):
    check_directory_exits(save_path, create=True)
    plt.bar(label_list, value_list)
    plt.title(map_name)
    # plt.ylim(0, file_num)
    for k, v in zip(label_list, value_list):
        plt.annotate(str(v), xy=(k, v))
    plt.xticks(label_list, rotation=15)
    plt.savefig(f"{save_path}/{map_name}.png")
    plt.show()


def show_ret_by_plot(dict_data, map_name, save_path=r"./rets"):
    check_directory_exits(save_path, create=True)
    DataFrame(dict_data).plot()
    plt.grid(True)
    plt.title(map_name)
    plt.savefig(f"{save_path}/{map_name}")
    plt.show()

