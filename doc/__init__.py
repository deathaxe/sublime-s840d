# -*- encoding: utf-8 -*-
import sublime

from . import database


def plugin_loaded():
    """Called by SublimeText after all plugins have been loaded."""
    sublime.set_timeout_async(lambda: database.cache_init(False), 5000)
