# -*- encoding: utf-8 -*-
import sublime
from . import base


class S840dRenumberCommand(base.TextCommand):
    """Add or update block numbers.

    Each CNC block normally starts with a number for identification.
    After editing the numbers may be mixed up. This command helps to
    update the block numbers.
    """
    def run(self, edit, start=None, increment=None):
        """Load settings and add or update block numbers of selected regions.

        Argsuments:
            edit (Edit): The current edit token which groups this operation
            start (int): An optional number to start counting with
            increment(int): An optional step width to increment blocks with
        """
        if start is None:
            # Ask user for start block number.
            self.block_start_input(increment)
        else:
            # Renumber with provided start block number provided.
            self.renumber_selections(edit, start, increment)

    def block_start_input(self, increment):
        """Ask user to provide block number to start renumbering with."""
        block_start = self.view.settings().get('s840d_gcode_block_start', 0)

        def on_input_panel_done(input_text):
            """Check user input and call renumber."""
            try:
                # Try to overide default start by user input value.
                start = int(input_text)
            except ValueError:
                # Default setting is expected to be an integer.
                start = int(block_start)
            # Call renumber command asynchronous
            sublime.set_timeout_async(lambda: self.view.run_command(
                's840d_renumber', {'start': start, 'increment': increment}))

        # show quick panel to ask for start block
        self.view.window().show_input_panel(
            'First Block Number:', str(block_start) if block_start else '',
            on_input_panel_done, None, None)

    def renumber_selections(self, edit, start, increment):
        """Add or update block numbers to all selected regions.

        Arguments:
            edit (Edit): The current edit token which groups this operation
            start (int): The first block number
            increment (int): The block number increment
        """
        # validate parameters
        settings = self.view.settings()
        if not increment:
            increment = settings.get('s840d_gcode_block_increment', 10)

        # backup cursor and viewport position
        row, vp_y = self.backup_viewport()
        selections = self.view.sel()
        if len(selections) == 1 and selections[0].empty():
            # update the whole file
            region = sublime.Region(0, self.view.size())
            self.renumber_region(edit, region, start, increment)
        else:
            # update selected regions
            for selection in selections:
                if not selection.empty():
                    self.renumber_region(edit, selection, start, increment)

        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)

    def renumber_region(self, edit, region, start, increment):
        """Add or update block numbers for a region.

        Arguments:
            edit (Edit): The current edit token which groups this operation
            region (Region): The region to update
            start (int): The first block number
            increment (int): The block number increment
        """
        # expand region to beginning of first line
        region.a = self.view.line(region.a).a
        # expand region to the end of the last line with one or more characters
        # being selected
        last_line = self.view.line(region.b)
        region.b = last_line.b if region.b > last_line.a else last_line.a - 1
        # create a list of lines
        lines = self.view.substr(region).splitlines(keepends=True)
        line_count = len(lines)
        if line_count < 2:
            return
        # determine first block number so that all blocknumbers will have the
        # same amount of digits
        blockno = start if start else 10 ** (
            len(str(line_count * increment)) - 1)
        # Add block numbers to each line which is not empty or a comment.
        # Try to keep indented comments in position with blocks
        repl = []
        for line in lines:
            # empty line or unindented line comment
            if not line or line[0] in ';%\n':
                repl.append(line)
                continue
            i = 0
            # skip leading white space
            while line[i] in ' \t':
                i += 1
            # indented header or whitespace only line
            if line[i] == '%\n':
                repl.append(line)
            # indented line comment
            elif line[i] == ';':
                # insert spaces instead of 'Nxxx '
                repl.append(' ' * (3 + len(str(blockno))) + line)
            # skip existing block number
            elif line[i] in 'Nn' and line[i+1].isdigit():
                i += 1
                while line[i].isdigit():
                    i += 1
                # skip one whitespace after block number as it will be added
                # anyway in the next step
                if line[i] == ' ':
                    i += 1
                repl.append(''.join(['N', str(blockno), ' ', line[i:]]))
                blockno += increment
            # ordinary block
            else:
                repl.append(''.join(['N', str(blockno), ' ', line]))
                blockno += increment
        # replace view's content and keep the last empty line only
        self.view.replace(edit, region, ''.join(repl))
