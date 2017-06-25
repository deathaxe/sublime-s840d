# -*- encoding: utf-8 -*-
import os


def is_subdir(path, directory):
    """Check if path is a sub of directory.

    Arguments:
        path (string):
            the path to check
        direcotry (string):
            the path to use as relative starting point.
    Returns:
        bool: True if path is a sub of directory or False otherwise.
    """
    try:
        relative = os.path.relpath(path, directory)
        return not relative.startswith(os.pardir)
    except ValueError:
        # filename and folder are ondifferent mount points
        return False


def in_project(window, filename):
    for folder in window.folders():
        try:
            relative = os.path.relpath(filename, folder)
            if not relative.startswith(os.pardir):
                return os.path.join(os.path.basename(folder), relative)
        except ValueError:
            # filename and folder are ondifferent mount points
            pass
    return filename
