import os

import sublime
import sublime_plugin


class S840dAwlLoadMergeCommand(sublime_plugin.TextCommand):

    def is_visible(self):
        """API method to decide when to show the command.

        Show the command in command pallet only, if open document is a valid
        SINUMERIK 840D source file.
        """
        return self.view.match_selector(0, 'source.s7.awl')

    def run(self, edit):

        # create output path
        input_path, _ = os.path.splitext(self.view.file_name())
        if not os.path.isdir(input_path):
            return

        self.view.erase(edit, sublime.Region(0, self.view.size()))
        print('Loading %s' % input_path)
        for file_name in os.listdir(input_path):
            if file_name[-4:].lower() == '.awl':
                file_path = os.path.join(input_path, file_name)
                with open(file_path, 'r') as file:
                    self.view.insert(edit, self.view.size(),
                                     file.read().strip() + '\n\n\n')
