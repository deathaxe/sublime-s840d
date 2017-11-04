# -*- encoding: utf-8 -*-
import multiprocessing

from . import database


def plugin_loaded():
    """Called by SublimeText after all plugins have been loaded."""
    multiprocessing.Process(target=lambda: database.cache_init(False)).run()
