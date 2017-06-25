# -*- encoding: utf-8 -*-

"""Publish only required classes to Sublime Text."""

import sublime

from .gcode.commands.beautify import S840dBeautifyCommand
from .gcode.commands.minify import S840dMinifyCommand
from .gcode.commands.blockno import S840dRenumberCommand


def plugin_loaded():
    """This function is called by ST3 after all plugins are loaded."""
    apply_essential_settings("s840d_arc")
    apply_essential_settings("s840d_gcode")
    apply_essential_settings("s840d_hmi")


def apply_essential_settings(syntax):
    """Apply essential settings from template to user file.

    This function loads the default values from a syntax settings file
    coming with this package as resource and copies all values to the
    /Packages/User/<syntax>.sublime-settings.
    """
    dirty = False
    file_name = "%s.sublime-settings" % syntax
    settings = sublime.load_settings(file_name)
    template = sublime.decode_value(sublime.load_resource(
        sublime.find_resources(file_name)[0]))
    for key in template.keys():
        value = template[key]
        # An essential setting was changed and needs update in the user syntax
        # settings file.
        if value != settings.get(key):
            dirty = True
            if value:
                # Apply essential settings.
                settings.set(key, value)
            else:
                # Keys to remove are marked with 'None' value.
                settings.erase(key)
    if dirty:
        # Save settings if at least one setting was changed.
        sublime.save_settings(file_name)
