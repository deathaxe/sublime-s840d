import time

import sublime_plugin


class WhatInputHandler(sublime_plugin.ListInputHandler):

    def description(self, v, text):
        return "Bump version string to"

    def list_items(self):
        return ['major', 'minor', 'patch', 'hotfix']


class S840dBumpVersion(sublime_plugin.TextCommand):
    """docstring for BumpVersion"""

    def input(self, args):
        if 'what' not in args:
            return WhatInputHandler()
        return None

    def is_visible(self):
        """API method to decide when to show the command.

        Show the command in command pallet only, if open document is a valid
        SINUMERIK 840D source file.
        """
        return self.view.match_selector(0, 'source.s840d_gcode')

    def is_enabled(self):
        return self.find_version() is not None

    def run(self, edit, what):
        # find version string
        region = self.find_version()
        if not region:
            return

        # bump the version string
        major, minor, patch, hotfix = self.view.substr(region).split('.')
        if what == 'major':
            major = int(major) + 1
            minor = 0
            patch = 0
            hotfix = 0
        elif what == 'minor':
            minor = int(minor) + 1
            patch = 0
            hotfix = 0
        elif what == 'patch':
            patch = int(patch) + 1
            hotfix = 0
        elif what == 'hotfix':
            hotfix = int(hotfix) + 1
        else:
            return

        self.view.replace(edit, region, "{:0>2}.{:0>2}.{:0>2}.{:0>2}".format(
            major, minor, patch, hotfix))

        # look for a date string in the same line to replace with current date
        date_region = self.view.find(r'\b\d{2,4}-\d{1,2}-\d{1,2}\b', region.end())
        region = self.view.line(region)
        if region.contains(date_region):
            self.view.replace(edit, date_region, time.strftime('%Y-%m-%d'))

    def find_version(self):
        try:
            location = self.view.sel()[0].begin()
        except:
            return None

        found = None
        for region in self.view.find_by_selector(
                'constant.language.version.s840d_gcode'):
            # ignore declarations following the current cursor position
            if region.a > location:
                break
            # check whether we already caught a symbol with a lower distance
            if found and abs(found.a - location) < abs(region.a - location):
                continue
            # finally add the new symbol or update an existing one
            found = region
        return found
