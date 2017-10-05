import re
import os

import sublime
import sublime_plugin


class S840dAwlSaveSplitCommand(sublime_plugin.TextCommand):

    def is_visible(self):
        """API method to decide when to show the command.

        Show the command in command pallet only, if open document is a valid
        SINUMERIK 840D source file.
        """
        return self.view.match_selector(0, 'source.s7.awl')

    def run(self, edit):

        # create output path
        output_path, _ = os.path.splitext(self.view.file_name())
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        # prepare regex to extract block/file name
        pattern = re.compile(r"""(?x)
                             (?:
                                 DATA_BLOCK
                               | FUNCTION(?:_BLOCK)?
                               | ORGANIZATION_BLOCK
                               | TYPE
                             )
                             [ \t]+
                             \"?([\w ]+)\"?   # block name
                             """)
        # the scope names which identify the blocks to export
        selector = ('meta.block.ob | meta.block.fb | meta.block.fc | '
                    'meta.block.db | meta.block.udt')

        index = []
        for region in self.view.find_by_selector(selector):
            try:
                content = self.view.substr(region)
                file_name = pattern.search(content).group(1).strip() + '.awl'
                file_path = os.path.join(output_path, file_name)
                with open(file_path, 'w+', encoding='utf-8') as file:
                    file.write(content)
                    file.write('\n')
                index.append(file_name)
            except Exception as error:
                print(error)

        for file_name in os.listdir(output_path):
            if file_name not in index:
                try:
                    os.unlink(os.path.join(output_path, file_name))
                except Exception as error:
                    print(error)

        index_path = os.path.join(output_path, '.index')
        with open(index_path, 'w+', encoding='utf-8') as file:
            for line in index:
                file.write(line + '\n')

        sublime.status_message("AWL saved!")
