# -*- encoding: utf-8 -*-
import re
import sublime
from . import base


class S840dBeautifyCommand(base.TextCommand):
    """Make a minified code readable.

    Try to make the code more readable, by indending and inserting whitespaces
    by a fixed rule.

    The basic intend of this function is to make standard cycles CYCLExxx
    readable again as they are released without comments and indention.
    """
    REGEX_LABEL = re.compile(r'^(\w+:)')
    REGEX_BLOCK_BEGIN = re.compile(
        r'(?i)^(?:IF|FOR|LOOP|REPEAT(?:\s*(?:;|$))|WHILE)\b')
    REGEX_BLOCK_END = re.compile(
        r'(?i)^(?:END(?:IF|FOR|LOOP|WHILE)|UNTIL)\b')

    def __init__(self, *args, **kwargs):
        """Initialize GitGutterCommand object."""
        super().__init__(*args, **kwargs)
        self.indents = 0
        self.tab_size = 2
        self.bln_size = 0

    def run(self, edit):
        """API entry point to run 's840d_beautify' command.

        Arguments:
            edit (Edit): The current edit token which groups this operation
        """
        # backup cursor and viewport position
        row, vp_y = self.backup_viewport()
        # read settings
        self.tab_size = self.view.settings().get('tab_size', 2)
        # get a copy of the file content
        view_region = sublime.Region(0, self.view.size())
        # replace tabs with spaces
        lines = self.view.substr(
            view_region).replace('\t', ' ' * self.tab_size).splitlines()
        # find longest block number
        self.bln_size = 0
        for line in lines:
            self.bln_size = max(self.bln_size, len(self.__blockno(line)))
        # reindent the code
        indented = []
        for line in lines:
            indented.append(self.__indentdify(line.strip()))
        del lines
        repl = '\n'.join(indented)
        # surround IF condition with parentheses
        # this is not required but looks better
        repl = re.sub(
            r'(?im)^([ ]*IF)\b[ ]*([\w\d\$].*?(?=GOTO|;|$))',
            r'\1 (\2) ', repl)
        # one whitespace before and after literal operators
        repl = re.sub(r'(?im)[ ]*\bNOT\b[ ]*', r' NOT ', repl)
        # no whitespaces around ( or [
        repl = re.sub(r'[ ]*([\[\(]+)[ ]*', r'\1', repl)
        # one whitespace before and after literal operators
        repl = re.sub(
            r'(?i)[ ]*\b(AND|OR|XOR|B_AND|B_OR|B_XOR|B_NOT|MOD|DIV)\b[ ]*',
            r' \1 ', repl)
        # one whitespace after ) or ]
        repl = re.sub(r'[ ]*([\]\)\:]+)[ ]*', r'\1 ', repl)
        # no whitespace around unary operators
        repl = re.sub(r'[ ]*([-+*/=><,]+)[ ]*', r'\1', repl)
        # one whitespace after keyword
        repl = re.sub(
            r'(?im)\b(IF|FOR|LOOP|UNTIL|WHILE)\b[ ]*', r'\1 ', repl)
        # replace view's content and keep the last empty line only
        self.view.replace(edit, view_region, repl.strip() + '\n')
        # restore cursor and viewport position
        self.restore_viewport(row, vp_y)

    @staticmethod
    def __blockno(text):
        """Extract the block number."""
        block_no = ''
        if text:
            if text[0] in 'Nn':
                col = 1
                while text[col] >= '0' and text[col] <= '9':
                    col += 1
                if col > 1:
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
        match = self.REGEX_LABEL.match(text)
        if match:
            col = len(match.group(1))
            label = text[:col] + ' '
            text = text[col:].lstrip()
        # block start
        if self.REGEX_BLOCK_BEGIN.match(text):
            indents = self.indents
            if text.upper().find('GOTO') == -1:
                self.indents += self.tab_size
        else:
            # intermediate keyword
            if text[:4].upper() == 'ELSE':
                indents = max(0, self.indents - self.tab_size)
            else:
                # block end
                if self.REGEX_BLOCK_END.match(text):
                    self.indents = max(0, self.indents - self.tab_size)
                indents = self.indents
        return ''.join(
            (block_no, label, ' ' * max(0, indents - len(label)), text))
