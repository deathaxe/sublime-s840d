# -*- encoding: utf-8 -*-
import re
import sublime
from . import base


def minify_code(text):
    # remove leading line spaces and block numbers
    text = re.sub(r'(?im)^(?:\s*N\d+)?\s*', '', text)
    # remove whitespaces after double colon if not preceded by quots
    text = re.sub(r'(?im)(^[^""]*?\:+?)[\t ]*', r'\1', text)
    # remove whitespaces around operators or seperators
    text = re.sub(r'[\t ]*([-+*/=><,\[\(\]\)]+)[\t ]*', r'\1', text)
    # remove empty or blank lines
    text = re.sub(r'(\s*\n){2,}', '\n', text)
    # ensure newline at eof
    return text + '\n'


def replace_comment(view, edit, region, protected):
    """Ensure not to delete a comment if it contains protected.

    Cycle through all regions and check whether they contain a protected
    region. If so, replace region by the content of the contained protected one
    and return True to indicate that. Return False if no protected region is
    contained in the region.
    """
    for p in protected:
        if region.contains(p):
            view.replace(edit, region, view.substr(p))
            protected.remove(p)
            return True
    return False


def remove_comments(view, edit):
    """Remove all but some special comments.

    Remove comments by scope as ; can be part of a string which makes it
    hard and error prone to handle via regexp only.
    """
    versions = view.find_all(r"^;VERSION:.*?\n")
    paths = view.find_all(r";\$PATH=.*?\n")
    for region in reversed(view.find_by_selector("comment.line - meta.eol")):
        if replace_comment(view, edit, region, versions):
            continue
        if replace_comment(view, edit, region, paths):
            continue
        view.erase(edit, region)


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

        remove_comments(self.view, edit)

        # get a copy of the file content
        region = sublime.Region(0, self.view.size())
        # replace view's content
        self.view.replace(edit, region, minify_code(self.view.substr(region)))
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)
