import math
import re
import sublime
import sublime_plugin
# import cProfile, pstats

REGEX_LABEL = re.compile(r'^(\w+:)')
REGEX_BLOCK_BEGIN = re.compile(r'(?i)^(?:IF|FOR|LOOP|REPEAT(?:\s*(?:;|$))|WHILE)\b')
REGEX_BLOCK_END = re.compile(r'(?i)^(?:END(?:IF|FOR|LOOP|WHILE)|UNTIL)\b')


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

        Show the command in command pallet only, if open document is
        a valid SINUMERIK 840D source file.
        """
        return self.is_scope_s840d()

    def is_scope_s840d(self):
        """Check if the current view shows a G-Code file."""
        return (self.view.scope_name(0).find('source.s840d_gcode') >= 0)


class S840dMinifyCommand(S840dTextCommand):
    """Shrink code code as small as possible.

    Remove all comments and block numbers as well as all unrequired
    whitespaces to make the code as small as possible.
    """

    def run(self, edit):
        """API entry point to run 's840d_minify' command."""

        # pr = cProfile.Profile()
        # pr.enable()

        # run only for SINUMERIK code
        if not self.is_scope_s840d():
            return
        view = self.view
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
        view.set_viewport_position([0, 0], False)

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

        # run only for SINUMERIK code
        if not self.is_scope_s840d():
            return
        view = self.view
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
        view.set_viewport_position([0, 0], False)

        # pr.disable()
        # sortby = 'cumulative'
        # ps = pstats.Stats(pr).sort_stats(sortby)
        # ps.print_stats()

    def __blockno(self, text):
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
            if 'ELSE' == text[:4].upper():
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

    def run(self, edit):
        """API entry point to run 's840d_renumber' command."""
        view = self.view
        settings = view.settings()
        increment = settings.get('s840d_block_increment', 10)
        selections = view.sel()
        visible = view.visible_region()

        # update the whole file
        if len(selections) == 1 and selections[0].empty():
            region = sublime.Region(0, view.size())
            self.renumber_region(edit, region, increment)
        else:
            # update selected regions
            for sel in selections:
                if not sel.empty():
                    self.renumber_region(edit, sel, increment)
        # restore visible region
        view.set_viewport_position(visible, False)

    def renumber_region(self, edit, region, increment):
        """Add or update block numbers for a region.

        Args:
            edit (Edit):     The edit control from Sublime API
            region (Region): The region to update
            increment (int): The increment

        Returns:
            Nothing
        """
        view = self.view
        # expand region to beginning of first line
        region.a = view.line(region.a).a
        # expand region to the end of the last line with one or more characters
        # being selected
        last = view.line(region.b)
        region.b = last.b if region.b > last.a else last.a - 1
        # create a list of lines
        lines = view.substr(region).splitlines()
        if len(lines) < 2:
            return
        # determine first block number so that all blocknumbers will have the
        # same amount of digits
        num_digits = int(math.log10(len(lines) * increment))
        blockno = 10 ** num_digits
        # Add block numbers to each line which is not empty or a comment. Try to
        # keep indented comments in position with blocks
        repl = ''
        for line in lines:
            # not an empty line
            if line:
                # unindented line comment
                if line[0] in ';%':
                    repl += line
                else:
                    i = 0
                    # skip leading white space
                    while line[i] in ' \t':
                        i += 1
                    # indented header
                    if line[i] == '%':
                        repl += line
                    # indented line comment
                    elif line[i] == ';':
                        # insert spaces instead of 'Nxxx '
                        repl += ' ' * (3 + num_digits) + line
                    # skip existing block number
                    elif line[i] in 'Nn' and line[i+1] in '0123456789':
                        i += 1
                        while line[i] >= '0' and line[i] <= '9':
                            i += 1
                        # skip one whitespace after block number
                        # as it will be added anyway in the next step
                        if line[i] == ' ':
                            i += 1
                        repl = ''.join([repl, 'N', str(blockno), ' ', line[i:]])
                        blockno += increment
                    # ordinary block
                    else:
                        repl = ''.join([repl, 'N', str(blockno), ' ', line])
                        blockno += increment
            # finalize the line
            repl += '\n'
        # replace view's content and keep the last empty line only
        view.replace(edit, region, repl.strip())
