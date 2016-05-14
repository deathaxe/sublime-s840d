import sublime, sublime_plugin
import re

class S840dTextCommand(sublime_plugin.TextCommand):
  """
  Base class for all S840D text commands.

  This class handles some common operations of all SINUMERIK
  related text operations and is therefore the base class for all
  the other text command classes.

  Basically it is used to show the commands in the command pallet
  only, if an s840d file is open.
  """

  # API method
  def is_visible(self):
    """
    Show the command in command pallet only, if open document is
    a valid SINUMERIK 840D source file.
    """
    return self.is_scope_s840d()

  # private member
  def is_scope_s840d(self):
    return (self.view.scope_name(0).find('source.s840d') >= 0)


class S840dMinifyCommand(S840dTextCommand):
  """
  Shrink code code as small as possible.

  Remove all comments and block numbers as well as all unrequired
  whitespaces to make the code as small as possible.
  """

  # API method
  def run(self, edit):
    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      line = self.view.line(0)
      while (line.b <= self.view.size()):
        # line content without leading and tailing whitespaces
        text = self.view.substr(line).strip()
        # remove block numbers
        text = re.sub(r'^[Nn]\d+\s*', '', text)
        # remove comments
        text = re.sub(r'\s*;(?!\$PATH\=).*$', '', text)
        # no whitespaces around operators or seperators
        text = re.sub(r'\s*([-+*/=><,:\[\(\]\)]+)\s*', r'\1', text)
        # remove multi space
        text = re.sub(r'\s{2,}', ' ', text)
        if (len(text)>0):
          # replace line content by minified version
          self.view.replace(edit, line, text)
        else:
          # remove the whole line including the line feed
          line.b += 1
          self.view.erase(edit, line)
        # move on to the next line
        line = self.view.line(line.a + len(text) + 1)


class S840dBeautifyCommand(S840dTextCommand):
  """
  Make a minified code readable.

  Try to make the code more readable, by indending and inserting
  whitespaces by a fixed rule.
  """

  indents = 0
  tab_size = 1

  # API method
  def run(self, edit):
    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      line = self.view.line(0)
      self.tab_size = self.view.settings().get('tab_size')
      while (line.b <= self.view.size()):
        # line content without leading and tailing whitespaces
        text = self.beautify(self.view.substr(line))
        # replace line content by correctly indented one
        self.view.replace(edit, line, text)
        # move on to the next row
        line = self.view.line(line.a + len(text) + 1)

  # private member
  def beautify(self,text):
    # remove block numbers and leading spaces
    text = re.sub(r'(?i)^(?:\s*[Nn]\d+)?\s*', r'', text)
    # block start
    match = re.match("(?i)^(IF|FOR|LOOP|WHILE)", text)
    if (match):
      text = ' ' * self.indents + text
      if (text.find('GOTO') == -1):
        self.indents += self.tab_size
    else:
      # intermediate keyword
      match = re.match("(?i)^ELSE", text)
      if (match):
        text = ' ' * (self.indents - self.tab_size) + text
      else:
        # block end
        match = re.match("(?i)^END(IF|FOR|LOOP|UNTIL|WHILE)", text)
        if (match):
          self.indents = max(0, self.indents - self.tab_size)

        # don't indent block beginning with a label
        match = re.match("(?i)^\w+\:", text)
        if (not match):
          text = ' ' * self.indents + text

    # ignore comments
    if (not re.match('^\s*;', text)):
      # surround IF condition with parentheses
      # this is not required but looks better
      text = re.sub(r'\bIF\b\s*([\w\d\$].*?(?=GOTO|;|$))', r'IF (\1) ', text)
      # one whitespace before and after literal operators
      text = re.sub(r'(?i)\s*b(NOT)\b\s*', r' \1 ', text)
      # no whitespaces around ( or [
      text = re.sub(r'\s*([\[\(]+)\s*', r'\1', text)
      # one whitespace before and after literal operators
      text = re.sub(r'(?i)\s*\b(AND|OR|XOR|B_AND|B_OR|B_XOR|B_NOT|MOD|DIV)\b\s*', r' \1 ', text)
      # one whitespace after ) or ]
      text = re.sub(r'\s*([\]\):]+)\s*', r'\1 ', text)
      # no whitespace around unary operators
      text = re.sub(r'\s*([-+*/=><,]+)\s*', r'\1', text)
      # one whitespace after keyword
      text = re.sub(r'(?i)\b(IF|FOR|LOOP|WHILE)\s*', r'\1 ', text)


    return text


class S840dRenumberCommand(S840dTextCommand):
  """
  Add or update block numbers.

  Each CNC block normally starts with a block number for identification.
  After editing the numbers may be mixed up. This command helps to
  update the block numbers.
  """

  blockno = 1
  blockno_step = 10

  # API method
  def run(self, edit):
    view = self.view
    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      # calculate first blocknumber
      self.auto_blockstart()
      line = view.line(0)
      while (line.end() <= view.size()):
        # line content without leading and tailing whitespaces
        text = self.renumber(view.substr(line))
        # replace line content by correctly indented one
        view.replace(edit, line, text)
        # move on to the next row
        line = view.line(line.begin() + len(text) + 1)

  def auto_blockstart(self):
    """
    Calculate first block number from the number of rows in the file
    and the given step witdth so that the number of digits of each
    block number is always the same.
    """
    rows = self.view.rowcol(self.view.size() - 1)[0]
    self.blockno = 1
    while (rows * self.blockno_step >= 10):
      self.blockno *= 10
      rows /= 10

  # private member
  def renumber(self,text):
    # comment
    m = re.match('^\s*(?:[%;]|$)', text)
    if (not m):
      text = re.sub(r"^(\s*[Nn]\d+\s?)?", "N" + str(self.blockno) + " " , text)
      self.blockno += self.blockno_step

    return text
