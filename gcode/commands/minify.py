# -*- encoding: utf-8 -*-
import re
import sublime
from . import base


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


def remove_all(view, edit, pattern):
    """Remove every matching text without touching strings."""
    for region in reversed(view.find_all(pattern)):
        if not view.match_selector(region.begin(), "string"):
            view.erase(edit, region)


def replace_all(view, edit, pattern, fmt):
    """Replace every matching text without touching strings."""
    extractions = []
    regions = view.find_all(pattern, fmt=fmt, extractions=extractions)
    for region, text in zip(reversed(regions), reversed(extractions)):
        if not view.match_selector(region.begin(), "string"):
            view.replace(edit, region, text)


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
        # remove block numbers and indention
        remove_all(self.view, edit, r'^(?:\s*[Nn]\d+)?\s*')
        # remove whitespace around operators
        replace_all(self.view, edit, r'[\t ]*([-+*/=><,\:\[\(\]\)]+)[\t ]*', r'\1')
        # remove empty lines
        replace_all(self.view, edit, r'([\t ]*\n){2,}', '\n')
        # remove multiple whitespace
        remove_all(self.view, edit, r'[\t ]+(?=[\t ])')
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)
