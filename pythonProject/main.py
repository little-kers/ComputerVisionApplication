import os
import random
import shutil

from keras.preprocessing.image import ImageDataGenerator

from log_cfg.log_config import MyLogger
from model_cfg import model_config
from utils.check_directory_exits import check_directory_exits
from utils.check_directory_is_empty import check_directory_is_empty
from utils.data_preprocessing import image_size_normalize, image_rotater, image_flipper, image_threshold, image_resizer, \
    image_median_blur
from utils.image_filter import illegal_image_filter, blurred_filter, similar_filter, single_channel_filter
from utils.image_similar_filter import compare_image_similarity
from utils.indicators_of_training_process_calculator import recall_calc, show_roc, precision, auc_calc
from utils.result_shower import show_ret_by_bar, show_ret_by_plot
from utils.show_environment_config import show_env


def data_filter(data_path=None):
    ret_label_list = []
    ret_value_list = []
    for func in illegal_image_filter, blurred_filter, compare_image_similarity, single_channel_filter:
        label = func.__name__
        ret = func(data_path)
        ret_label_list.append(label)
        ret_value_list.append(ret)
        print(f"{label}:{ret}")
    if ret_label_list is not None and ret_value_list is not None:
        show_ret_by_bar("Data filter", ret_label_list, ret_value_list, graph_save_path)


def size_normalizer(dir_path=None, normalized_path="./normalized_data"):
    check_directory_exits(normalized_path, create=True)
    for r, DIRS, FILES in os.walk(dir_path):
        if FILES is None or len(FILES) == 0:
            continue
        for f in FILES:
            image_path = os.path.join(r, f)
            # print(image_path, r)
            image_size_normalize(image_path, save_path=normalized_path, normalized_image_size=(128, 128))
            print("\r" + "Normalizing: {0:.2f}%".format((FILES.index(f) + 1) / len(FILES) * 100), end="")
    print("\n")
    return check_directory_exits(normalized_path) and os.listdir(normalized_path) is not None


def image_enhance_randomly(image_path, root):
    ret_dict = {}
    for func in image_rotater, image_flipper, image_threshold, image_resizer, image_median_blur:
        label = func.__name__
        var = func(image_path, root)
        ret_dict[func.__name__] = ret_dict.get(func.__name__, 0) + var
        print(f"{label}:{var}")
    return ret_dict


def train_test_spliter(original_path, classified_path):
    """

    :param original_path:
    :param classified_path:
    :return:
    """
    train_path = os.path.join(classified_path, "train")
    test_path = os.path.join(classified_path, "test")
    train_rate = 0.8
    check_directory_exits(train_path, create=True)
    check_directory_exits(test_path, create=True)

    for r, DIRS, FILES in os.walk(original_path):
        if FILES is None or len(FILES) == 0:
            continue
        random.shuffle(FILES)
        train_files = FILES[:int(len(FILES) * train_rate)]
        test_files = FILES[int(len(FILES) * train_rate):]
        for train_file in train_files:
            src_file = os.path.join(r, train_file)
            dst_file = os.path.join(train_path, train_file)
            shutil.copyfile(src_file, dst_file)
            print("\r" + "Split train data: {0:.2f}%".format(
                (train_files.index(train_file) + 1) / len(train_files) * 100), end="")
        print("\n")
        for test_file in test_files:
            src_file = os.path.join(r, test_file)
            dst_file = os.path.join(test_path, test_file)
            shutil.copyfile(src_file, dst_file)
            print("\r" + "Split test data: {0:.2f}%".format((test_files.index(test_file) + 1) / len(test_files) * 100),
                  end="")
        print("\n")
    if check_directory_exits(train_path) or os.listdir(train_path) is not None and check_directory_exits(
            test_path) or os.listdir(test_path) is not None:
        return train_path, test_path
    else:
        logger.critical(
            f"Failed to spilt data: Train directory is contain are {os.listdir(train_path)}, test directory is "
            f"contain are {os.listdir(test_path)}",
            exc_info=True, stack_info=True)
        raise OSError("Splitting data failed.")


def image_generator(train_directory=None, test_directory=None):
    train_directory = os.path.abspath(train_directory)
    test_directory = os.path.abspath(test_directory)
    train_datagen = ImageDataGenerator(rescale=1. / 255)
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(train_directory, target_size=(128, 128), batch_size=4,
                                                        class_mode="binary")
    validation_generator = test_datagen.flow_from_directory(test_directory, target_size=(128, 128), batch_size=4,
                                                            class_mode="binary")
    return train_generator, validation_generator


def reclassify_data(data_path_tuple):
    if not isinstance(data_path_tuple, tuple):
        logger.error(f"Type error: expect type is tuple, but received type is {type(data_path_tuple)}")
        return
    classed_path = ""
    for PATH in data_path_tuple:
        for r, DIRS, FILES in os.walk(PATH):
            if FILES is None or len(FILES) == 0:
                continue
            for f in FILES:
                classed_path = os.path.join(r, os.path.basename(f).split("_")[0])
                check_directory_exits(classed_path, create=True)
                src_file = os.path.join(r, f)
                dst_path = classed_path
                shutil.move(src_file, dst_path)
                print("\r" + "Moving: {0:.2f}%".format((FILES.index(f) + 1) / len(FILES) * 100), end="")
    print("\n")


if __name__ == '__main__':
    # Showing the environment config.
    show_env()
    # Create log file.
    log_name = "run"
    log_save_path = r"./logs"
    check_directory_exits(log_save_path, create=True)
    logger = MyLogger("main-run", file=f"{log_save_path}/{log_name}.log")
    # Data directory path.
    # Make this path to your data path.
    data_path = r"./rawdata"
    # Initialize the filter data save paths.
    preprocessed_data_save_path = "./preprocessed_data"
    normalized_data_save_path = "./normalized_data"
    split_testing_and_training_data_save_path = r"./divided_training_and_testing_data"
    # Initialize the result file save paths.
    model_save_path = "./models"
    graph_save_path = r"./graph_rets"

    # Filter the data.
    data_filter(data_path)
    # Normalizing image previously so that to accelerate the data processing.
    if size_normalizer(data_path, preprocessed_data_save_path):
        image_transformations = {}
        for root, dirs, files in os.walk(preprocessed_data_save_path):
            if len(files) == 0 or files is None:
                continue
            for f in files:
                image_path = os.path.join(root, f)
                # Randomly transform images to create more data to training.
                tmp_dict = image_enhance_randomly(image_path, root)
                # Count the number and type of image transformations.
                for key in tmp_dict:
                    if key in image_transformations:
                        image_transformations[key] += tmp_dict[key]
                    else:
                        image_transformations[key] = tmp_dict[key]
        logger.info(f"The image transform is: {image_transformations}")
        print(f"Transformations: {image_transformations}")
        label_list = list(image_transformations.keys())
        value_list = list(image_transformations.values())
        # Show image transformation as bar
        show_ret_by_bar("Image enhanced", label_list, value_list, graph_save_path)
        # Normalizing image so that model training.
        size_normalizer(preprocessed_data_save_path, normalized_data_save_path)
    path = train_test_spliter(normalized_data_save_path, split_testing_and_training_data_save_path)
    reclassify_data(path)
    # path = (r"E:\pythonProject\split_data\test", r"E:\pythonProject\split_data\train")
    train_dir_path, test_dir_path = path

    train_gen, validation_gen = image_generator(train_directory=train_dir_path, test_directory=test_dir_path)
    # Create a model to fit.
    model = model_config.model_init()
    history = model.fit(train_gen, steps_per_epoch=int(train_gen.samples / train_gen.batch_size), epochs=15,
                        validation_data=validation_gen,
                        validation_steps=int(validation_gen.samples / validation_gen.batch_size))
    history = history.history
    show_ret_by_plot(history, "Indicators of the training process", graph_save_path)

    loss, accuracy = model.evaluate(validation_gen, steps=int(validation_gen.samples / validation_gen.batch_size))
    print('Test Accuracy:', accuracy)
    print('Test Loss:', loss)
    logger.info(f"Test accuracy: {accuracy}, test loss: {loss}")

    # prediction = model.predict(validation_gen)
    # pre_true = validation_gen.classes
    # pre_labels = validation_gen.labels
    # # Show this model precisions.
    # precisions = precision(prediction, pre_labels)
    # print(f"precision: {precisions}")
    # logger.info(f"Precision: {precisions}")
    # # Show this model recall.
    # Recall = recall_calc(pre_labels, prediction)
    # print(f"Recall: {Recall}")
    # logger.info(f"Recall: {Recall}")
    # # Show this model ROC by plot.
    # roc_auc, fpr, tpr = auc_calc(validation_gen.labels, prediction)
    # show_roc(roc_auc, fpr, tpr, save_path=graph_save_path)
    # Save model.
    print("Saving model.")
    model_config.model_save(model=model, name="run", model_save_path=model_save_path)
    if not check_directory_is_empty(model_save_path):
        print("Saving model success.")
        logger.info(f"Saving model success, path: {model_save_path}.")
