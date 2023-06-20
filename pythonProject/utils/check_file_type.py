def check_file_type(file_name, type_list):
    """
    Check the file type is image file or not.
    :param file_name: File name
    :param type_list: The target file types tuple
    :return: Boolean
    """
    if file_name.lower().endswith(tuple(type_list)):
        ret = True
    else:
        ret = False
    return ret
