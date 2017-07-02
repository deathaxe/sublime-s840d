# -*- encoding: utf-8 -*-

"""The place of common base functions and classes.

This file keeps some common functions and base classes which are used by all
commands in this module.
"""
import sublime_plugin


class TextCommand(sublime_plugin.TextCommand):
    """Base class for all S840D text commands.

    This class handles some common operations of all SINUMERIK
    related text operations and is therefore the base class for all
    the other text command classes.

    Basically it is used to show the commands in the command pallet
    only, if an s840d file is open.
    """

    def is_visible(self):
        """API method to decide when to show the command.

        Show the command in command pallet only, if open document is a valid
        SINUMERIK 840D source file.
        """
        return self.view.match_selector(0, 'source.s840d_gcode')

    def backup_viewport(self):
        """Backup cursor and viewport position.

        Returns:
            tuple: (row, vp_y)
                Current cursor row, viewport position.
        """
        _, vp_y = self.view.viewport_position()
        row, _ = self.view.rowcol(self.view.sel()[0].begin())
        return (row, vp_y)

    def restore_viewport(self, row, vp_y):
        """Restore cursor and viewport position.

        Arguments:
            row (int): The row to set cursor position to.
            vp_y (float): The vertical viewport scroll position.
        """
        self.view.sel().clear()
        self.view.sel().add(self.view.text_point(row, 0))
        # Use x=0.01 as workaround for a bug in ST3 which causes the
        # viewport beeing horizontal scrolled to the right most column.
        self.view.set_viewport_position(xy=(0.01, vp_y), animate=False)
