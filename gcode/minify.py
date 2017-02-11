# -*- encoding: utf-8 -*-
import re
import sublime
from . import base


class S840dMinifyCommand(base.TextCommand):
    """Shrink code code as small as possible.

    Remove all comments and block numbers as well as all unrequired
    whitespaces to make the code as small as possible.
    """
    def run(self, edit):
        """API entry point to run 's840d_minify' command.

        Arguments:
            edit (Edit): The current edit token which groups this operation
        """
        # backup cursor and viewport position
        row, vp_y = self.backup_viewport()
        # get a copy of the file content
        region = sublime.Region(0, self.view.size())
        text = self.view.substr(region)
        # remove leading line spaces and block numbers
        text = re.sub(r'(?im)^(?:\s*N\d+)?\s*', '', text)
        # remove comments excluding some special header comments
        text = re.sub(
            r'(?im)\s*;(?!(?:\$PATH\=|DATE|VERSION|CHANGE|.*\")).*$',
            '', text)
        # no whitespaces around operators or seperators
        text = re.sub(r'[\t ]*([-+*/=><,\:\[\(\]\)]+)[\t ]*', r'\1', text)
        # remove multi space
        text = re.sub(r'[\t ]{2,}', ' ', text)
        # replace view's content
        self.view.replace(edit, region, text)
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)
