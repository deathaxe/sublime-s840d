import math
import re
import sublime
import sublime_plugin
# import cProfile, pstats

REGEX_LABEL = re.compile(r'^(\w+:)')
REGEX_BLOCK_BEGIN = re.compile(r'(?i)^(?:IF|FOR|LOOP|REPEAT(?:\s*(?:;|$))|WHILE)\b')
REGEX_BLOCK_END = re.compile(r'(?i)^(?:END(?:IF|FOR|LOOP|WHILE)|UNTIL)\b')


def is_s840d_gcode(view):
    """Return True, if view shows G-Code."""
    return view.scope_name(0).find('source.s840d_gcode') >= 0


class S840dTextCommand(sublime_plugin.TextCommand):
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
        return is_s840d_gcode(self.view)

    def backup_viewport(self):
        """Backup cursor and viewport position."""
        _, vp_y = self.view.viewport_position()
        row, _ = self.view.rowcol(self.view.sel()[0].begin())
        return (row, vp_y)

    def restore_viewport(self, row, vp_y):
        """Restore cursor and viewport position."""
        self.view.sel().clear()
        self.view.sel().add(self.view.text_point(row, 0))
        # Use x=0.01 as workaround for a bug in ST3
        self.view.set_viewport_position(xy=(0.01, vp_y), animate=False)


class S840dMinifyCommand(S840dTextCommand):
    """Shrink code code as small as possible.

    Remove all comments and block numbers as well as all unrequired
    whitespaces to make the code as small as possible.
    """
    def run(self, edit):
        """API entry point to run 's840d_minify' command."""

        # pr = cProfile.Profile()
        # pr.enable()

        view = self.view
        # backup cursor and viewport position
        row, vp_y = self.backup_viewport()
        # get a copy of the file content
        region = sublime.Region(0, view.size())
        text = view.substr(region)
        # remove leading line spaces and block numbers
        text = re.sub(r'(?im)^(?:\s*N\d+)?\s*', '', text)
        # remove comments excluding some special header comments
        text = re.sub(r'(?im)\s*;(?!(?:\$PATH\=|DATE|VERSION|CHANGE|.*\")).*$', '', text)
        # no whitespaces around operators or seperators
        text = re.sub(r'[\t ]*([-+*/=><,\:\[\(\]\)]+)[\t ]*', r'\1', text)
        # remove multi space
        text = re.sub(r'[\t ]{2,}', ' ', text)
        # replace view's content
        view.replace(edit, region, text)
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)

        # pr.disable()
        # sortby = 'cumulative'
        # ps = pstats.Stats(pr).sort_stats(sortby)
        # ps.print_stats()


class S840dBeautifyCommand(S840dTextCommand):
    """Make a minified code readable.

    Try to make the code more readable, by indending and inserting whitespaces
    by a fixed rule.

    The basic intend of this function is to make standard cycles CYCLExxx
    readable again as they are released without comments and indention.
    """

    indents = 0
    tab_size = 2
    bln_size = 0

    def run(self, edit):
        """API entry point to run 's840d_beautify' command."""

        # pr = cProfile.Profile()
        # pr.enable()

        view = self.view
        # backup cursor and viewport position
        row, vp_y = self.backup_viewport()
        # read settings
        self.tab_size = view.settings().get('tab_size', 2)
        # get a copy of the file content
        view_region = sublime.Region(0, view.size())
        # replace tabs with spaces
        lines = view.substr(view_region).replace('\t', ' ' * self.tab_size).split('\n')
        # find longest block number
        self.bln_size = 0
        for line in lines:
            self.bln_size = max(self.bln_size, len(self.__blockno(line)))
        # reindent the code
        repl = ''
        for line in lines:
            repl += self.__indentdify(line.strip()) + '\n'
        # surround IF condition with parentheses
        # this is not required but looks better
        repl = re.sub(r'(?im)^([ ]*IF)\b[ ]*([\w\d\$].*?(?=GOTO|;|$))', r'\1 (\2) ', repl)
        # one whitespace before and after literal operators
        repl = re.sub(r'(?im)[ ]*\bNOT\b[ ]*', r' NOT ', repl)
        # no whitespaces around ( or [
        repl = re.sub(r'[ ]*([\[\(]+)[ ]*', r'\1', repl)
        # one whitespace before and after literal operators
        repl = re.sub(r'(?i)[ ]*\b(AND|OR|XOR|B_AND|B_OR|B_XOR|B_NOT|MOD|DIV)\b[ ]*', r' \1 ', repl)
        # one whitespace after ) or ]
        repl = re.sub(r'[ ]*([\]\)\:]+)[ ]*', r'\1 ', repl)
        # no whitespace around unary operators
        repl = re.sub(r'[ ]*([-+*/=><,]+)[ ]*', r'\1', repl)
        # one whitespace after keyword
        repl = re.sub(r'(?im)\b(IF|FOR|LOOP|UNTIL|WHILE)\b[ ]*', r'\1 ', repl)
        # replace view's content and keep the last empty line only
        view.replace(edit, view_region, repl.strip() + '\n')
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)

        # pr.disable()
        # sortby = 'cumulative'
        # ps = pstats.Stats(pr).sort_stats(sortby)
        # ps.print_stats()

    @staticmethod
    def __blockno(text):
        """Extract the block number."""
        block_no = ''
        if text:
            if text[0] in 'Nn':
                col = 1
                while text[col] >= '0' and text[col] <= '9':
                    col += 1
                block_no = text[:col]
        return block_no

    def __indentdify(self, text):
        """Indent the code.

        This is basically what the built-in function 'reident' does,
        with the help of the indent.tmPreferences, but a little bit faster
        and with regard of lines beginning with a block number (e.g. N1240).
        """
        if not text:
            return ''
        indents = 0
        # block number
        block_no = self.__blockno(text)
        if block_no:
            col = len(block_no)
            block_no += ' ' * (1 + max(0, self.bln_size - col))
            text = text[col+1:].lstrip()
        else:
            block_no = ' ' * self.bln_size
        # goto label
        label = ''
        match = REGEX_LABEL.match(text)
        if match:
            col = len(match.group(1))
            label = text[:col] + ' '
            text = text[col:].lstrip()
        # block start
        if REGEX_BLOCK_BEGIN.match(text):
            indents = self.indents
            if text.upper().find('GOTO') == -1:
                self.indents += self.tab_size
        else:
            # intermediate keyword
            if text[:4].upper() == 'ELSE':
                indents = max(0, self.indents - self.tab_size)
            else:
                # block end
                if REGEX_BLOCK_END.match(text):
                    self.indents = max(0, self.indents - self.tab_size)
                indents = self.indents
        return block_no + label + ' ' * max(0, indents - len(label)) + text


class S840dRenumberCommand(S840dTextCommand):
    """Add or update block numbers.

    Each CNC block normally starts with a number for identification.
    After editing the numbers may be mixed up. This command helps to
    update the block numbers.
    """
    def run(self, edit, start=None, increment=None):
        """Load settings and add or update block numbers of selected regions.

        Args:
            edit (Edit): The current edit token
            start (int): An optional number to start counting with
            increment(int): An optional step width to increment blocks with

        Returns:
            None
        """
        # load settings if start is not provided by command
        if not start:
            start = self.view.settings().get(
                's840d_gcode_block_start', 0)
        if not increment:
            increment = self.view.settings().get(
                's840d_gcode_block_increment', 10)

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

        Args:
            edit (Edit):     The edit control from Sublime API
            region (Region): The region to update
            increment (int): The increment

        Returns:
            Nothing
        """
        # expand region to beginning of first line
        region.a = self.view.line(region.a).a
        # expand region to the end of the last line with one or more characters
        # being selected
        last = self.view.line(region.b)
        region.b = last.b if region.b > last.a else last.a - 1
        # create a list of lines
        lines = self.view.substr(region).splitlines(keepends=True)
        line_count = len(lines)
        if line_count < 2:
            return
        # determine first block number so that all blocknumbers will have the
        # same amount of digits
        blockno = start if start else 10 ** int(
            math.log10(line_count * increment))
        # Add block numbers to each line which is not empty or a comment. Try to
        # keep indented comments in position with blocks
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
                repl.append(' ' * (3 + len(blockno)) + line)
            # skip existing block number
            elif line[i] in 'Nn' and line[i+1].isdigit():
                i += 1
                while line[i].isdigit():
                    i += 1
                # skip one whitespace after block number as it will be added anyway
                # in the next step
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


class S840dRenumberInputCommand(sublime_plugin.WindowCommand):
    """Sublime Text Window Command to invoke renumbering."""

    def is_visible(self):
        """API method to decide when to show the command.

        Show the command in command pallet only, if open document is a valid
        SINUMERIK 840D source file.
        """
        return is_s840d_gcode(self.window.active_view())

    def run(self):
        """Show input panel to enter first block number."""
        self.window.show_input_panel(
            'First Block Number:',
            self.window.active_view().settings().get(
                's840d_gcode_block_start', ''),
            self.on_done, None, None)

    def on_done(self, start_block):
        """Check user input and call renumber."""
        try:
            start_block = int(start_block)
        except ValueError:
            start_block = 0
        self.window.active_view().run_command(
            's840d_renumber', {'start': start_block})
