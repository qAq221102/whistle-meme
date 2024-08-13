import os


"""
Find the File's Path
"""


def D2F(D='', F=''):
    """
    In the current directory, find a target file which in a certain directory
    argument:
        D: name of certain directory, use ',' to separate the dir name
        F: name of target file
    return:
        path of target file if exists, or 'None'
    """
    current_dir = os.getcwd()
    if not D:
        target_dir = current_dir
    else:
        dirs = [dir.strip() for dir in D.split(',')]
        target_dir = os.path.join(current_dir, *dirs)
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        for file_name in os.listdir(target_dir):
            if os.path.isfile(os.path.join(target_dir, file_name)) and file_name == F:
                return os.path.join(target_dir, file_name)
    return 'None'


def FBW(F=''):
    """
    Find the path of target file by os.walk()
    argument:
        F: name of target file
    return:
        path of target file if exists, or 'None'
    """
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        if F in files:
            return os.path.join(root, F)
    return None