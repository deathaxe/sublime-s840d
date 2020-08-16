# -*- encoding: utf-8 -*-

"""Publish only required classes to Sublime Text."""
import sublime

if int(sublime.version()) < 3153:
    print('CNC Sinumerik 840D requires ST3 3153+')

else:
    import sys

    __all__ = [
        'S840dBeautifyCommand',
        'S840dBumpVersion',
        'S840dGotoDefinitionCommand',
        'S840dMinifyCommand',
        'S840dProtectCommand',
        'S840dRenumberCommand',
        'S840dAwlLoadMergeCommand',
        'S840dAwlSaveSplitCommand',
        'S840dHmiEvents',
        'S840dNckViewEvents'
    ]

    prefix = __package__ + "."  # don't clear the base package
    for module_name in [
            module_name for module_name in sys.modules
            if module_name.startswith(prefix) and module_name != __name__]:
        del sys.modules[module_name]
    prefix = None

    # export commands
    from .gcode.commands.beautify import S840dBeautifyCommand
    from .gcode.commands.blockno import S840dRenumberCommand
    from .gcode.commands.goto import S840dGotoDefinitionCommand
    from .gcode.commands.minify import S840dMinifyCommand
    from .gcode.commands.protect import S840dProtectCommand
    from .gcode.commands.version import S840dBumpVersion
    from .plc.commands.merge import S840dAwlLoadMergeCommand
    from .plc.commands.split import S840dAwlSaveSplitCommand

    # export event handlers
    from .gcode.events import S840dNckViewEvents
    from .hmi.events import S840dHmiEvents

    def plugin_loaded():
        """Called by SublimeText after all plugins have been loaded."""
        from threading import Thread
        from .doc import database

        Thread(target=lambda: database.cache_init(False)).start()
